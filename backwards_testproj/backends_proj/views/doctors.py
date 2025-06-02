# backends_proj/views/doctors.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from backends_proj.models import RegistrationOrder, User, AppointmentSlot
from django.utils import timezone
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from dateutil.parser import isoparse
from django.utils.timezone import make_aware
from backends_proj.models import User, DoctorProfile
import traceback
import json, uuid

@api_view(['GET', 'POST'])
def doctor_dashboard(request):
    user_id = request.GET.get('user_id') or request.data.get('user_id')
    role = request.GET.get('role') or request.data.get('role')

    # 打印日志查看
    print("接收到的 user_id：", user_id, "role：", role)

    if not user_id or role != 'doctor':
        return Response({'code': 403, 'message': '仅医生可访问'}, status=403)

    # 获取用户实例
    try:
        user = User.objects.get(id=int(user_id))  # 👈 强制转换为整数
    except (User.DoesNotExist, ValueError, TypeError):
        return Response({'code': 404, 'message': '医生用户不存在'}, status=404)

    if request.method == 'GET':
        # 查询该医生的挂号记录
        orders = RegistrationOrder.objects.filter(slot__doctor=user).order_by('slot__time_start')
        data = [{
            'order_id': order.order_id,
            'patient_name': order.patient.real_name,
            'status': order.status,
            'time': order.slot.time_start.strftime('%m-%d %H:%M')
        } for order in orders]
        return Response({'code': 200, 'data': data})

    elif request.method == 'POST':
        order_id = request.data.get('order_id')
        new_status = request.data.get('status')
        # 打印日志查看
        print("接收到的 order_id：", order_id, "new_status：", new_status)

        if not order_id or new_status not in ['pending', 'completed', 'canceled', 'exception', 'diagnosing']:
            return Response({'code': 400, 'message': '参数错误'}, status=400)

        try:
            order = RegistrationOrder.objects.get(order_id=order_id)
            if order.slot.doctor != user:
                return Response({'code': 403, 'message': '无权操作其他医生订单'})
            order.status = new_status
            order.save()
            return Response({'code': 200, 'message': '状态更新成功'})
        except RegistrationOrder.DoesNotExist:
            return Response({'code': 404, 'message': '挂号单不存在'})
    

# 新增号源功能
@api_view(["POST"])
def create_appointment_slot(request):
    """创建号源（前端传 user_id 和 role）"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        role = data.get('role')
        time_start = data.get('time_start')
        time_end = data.get('time_end')
        total_quota = data.get('total_quota', 20)

        print(f"接收到 user_id: {user_id}, role: {role}, time_start: {time_start}, time_end: {time_end}")

        # 基础校验
        if not user_id or role != 'doctor':
            return JsonResponse({'code': 403, 'message': '仅医生可设置号源'}, status=403)

        # 获取医生对象
        try:
            doctor = User.objects.get(id=user_id, role='doctor')
        except User.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '医生用户不存在'}, status=404)

        # 参数检查
        if not time_start or not time_end:
            return JsonResponse({'code': 400, 'message': '起始时间或结束时间缺失'}, status=400)

        try:
            parsed_start_time = isoparse(time_start)
            parsed_end_time = isoparse(time_end)
            parsed_start_time = timezone.make_aware(parsed_start_time)
            parsed_end_time = timezone.make_aware(parsed_end_time)

            if parsed_end_time <= parsed_start_time:
                return JsonResponse({'code': 400, 'message': '结束时间必须晚于开始时间'}, status=400)
            if parsed_start_time <= timezone.now():
                return JsonResponse({'code': 400, 'message': '开始时间必须是未来时间'}, status=400)
        except ValueError:
            return JsonResponse({'code': 400, 'message': '时间格式无效'}, status=400)

        # 创建号源记录
        slot = AppointmentSlot.objects.create(
            doctor=doctor,
            time_start=parsed_start_time,
            time_end=parsed_end_time,
            total_quota=total_quota,
            remaining_quota=int(total_quota * 0.9)
        )

        return JsonResponse({
            'code': 200,
            'message': '号源创建成功',
            'slot_id': slot.id
        })

    except Exception as e:
        print("发生异常：", str(e))
        traceback.print_exc()
        return JsonResponse({'code': 500, 'message': f'服务器错误: {str(e)}'}, status=500)


# 取消号源功能
@require_http_methods(["POST"])
def cancel_appointment_slot(request):
    """取消号源（连带处理关联挂号单）"""
    try:
        # 验证用户身份
        if request.user.role != 'doctor':
            return JsonResponse({'code': 403, 'message': '仅允许医生操作'}, status=403)

        # 解析请求数据
        data = json.loads(request.body)
        slot_id = data.get('slot_id')

        # 校验参数
        if not slot_id:
            return JsonResponse({'code': 400, 'message': '必须提供号源ID'}, status=400)

        # 查询号源并验证归属
        try:
            slot = AppointmentSlot.objects.get(id=slot_id)
        except AppointmentSlot.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '号源不存在'}, status=404)
        
        if slot.doctor != request.user:
            return JsonResponse({'code': 403, 'message': '无权操作其他医生的号源'}, status=403)

        # 取消关联的挂号单（可选逻辑：自动标记为已取消）
        pending_orders = RegistrationOrder.objects.filter(slot=slot, status='pending')
        for order in pending_orders:
            order.status = 'canceled'
            order.save()

        # 删除号源
        slot.delete()

        return JsonResponse({'code': 200, 'message': '号源已取消'})

    except Exception as e:
        return JsonResponse({'code': 500, 'message': f'服务器错误: {str(e)}'}, status=500)

@api_view(["GET"])
def get_doctor_profile(request):
    try:
        user_id = request.GET.get("user_id")
        role = request.GET.get("role")

        print("获取医生简介: ", user_id, role)

        if not user_id or role != "doctor":
            return JsonResponse({"code": 403, "message": "仅医生可查看"}, status=403)

        try:
            doctor = User.objects.get(id=user_id, role="doctor")
        except User.DoesNotExist:
            return JsonResponse({"code": 404, "message": "医生不存在"}, status=404)

        profile, _ = DoctorProfile.objects.get_or_create(user=doctor)

        return JsonResponse({
            "code": 200,
            "message": "成功获取医生简介",
            "data": {
                "biography": profile.biography or "",
                "department": profile.department or ""
            }
        })

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"code": 500, "message": f"服务器错误: {str(e)}"}, status=500)


# 更新医生简介（根据 user_id 和 role）
@api_view(["POST"])
def update_doctor_profile(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        role = data.get("role")
        biography = data.get("biography", "")

        print("更新医生简介: ", user_id, role, biography)

        if not user_id or role != "doctor":
            return JsonResponse({"code": 403, "message": "仅医生可修改"}, status=403)

        try:
            doctor = User.objects.get(id=user_id, role="doctor")
        except User.DoesNotExist:
            return JsonResponse({"code": 404, "message": "医生不存在"}, status=404)

        profile, _ = DoctorProfile.objects.get_or_create(user=doctor)
        profile.biography = biography
        profile.save()

        return JsonResponse({
            "code": 200,
            "message": "医生简介更新成功",
            "data": {
                "biography": profile.biography
            }
        })

    except Exception as e:
        return JsonResponse({"code": 500, "message": f"服务器错误: {str(e)}"}, status=500)