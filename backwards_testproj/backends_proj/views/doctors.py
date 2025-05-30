# backends_proj/views/doctors.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from backends_proj.models import RegistrationOrder, User, AppointmentSlot
from django.utils import timezone
import json, uuid

@require_http_methods(["POST"])
def doctor_dashboard(request):
    """修改挂号单状态（仅医生角色可操作）"""
    try:
        # 验证用户身份
        if not request.user.is_authenticated or request.user.role != 'doctor':
            return JsonResponse({'code': 403, 'message': '仅允许医生操作'})

        # 解析请求数据
        data = json.loads(request.body)
        order_id = data.get('order_id')
        new_status = data.get('status')

        # 校验参数
        if not order_id or not new_status:
            return JsonResponse({'code': 400, 'message': '参数缺失'})

        if new_status not in ['pending', 'completed', 'canceled']:
            return JsonResponse({'code': 400, 'message': '无效状态值'})

        # 查询并更新挂号单
        try:
            order = RegistrationOrder.objects.get(order_id=order_id)
        except RegistrationOrder.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '挂号单不存在'})

        # 检查医生权限（仅处理自己号源的订单）
        if order.slot.doctor != request.user:
            return JsonResponse({'code': 403, 'message': '无权操作其他医生的订单'})

        # 更新状态
        order.status = new_status
        order.save()

        return JsonResponse({'code': 200, 'message': '状态更新成功'})

    except Exception as e:
        return JsonResponse({'code': 500, 'message': f'服务器错误: {str(e)}'})
    

# 新增号源功能
@require_http_methods(["POST"])
def create_appointment_slot(request):
    """创建号源（仅医生角色可操作）"""
    try:
        # 验证用户身份
        if not request.user.is_authenticated or request.user.role != 'doctor':
            return JsonResponse({'code': 403, 'message': '仅允许医生操作'}, status=403)

        # 解析请求数据
        data = json.loads(request.body)
        time_slot = data.get('time_slot')
        total_quota = data.get('total_quota', 20)

        # 校验参数
        if not time_slot:
            return JsonResponse({'code': 400, 'message': '必须提供时间段'}, status=400)
        
        # 时间格式验证（示例：假设前端传递 ISO 8601 格式）
        try:
            parsed_time = timezone.datetime.fromisoformat(time_slot)
            if parsed_time <= timezone.now():
                return JsonResponse({'code': 400, 'message': '时间段必须为未来时间'}, status=400)
        except ValueError:
            return JsonResponse({'code': 400, 'message': '时间格式无效'}, status=400)

        # 创建号源
        slot = AppointmentSlot.objects.create(
            doctor=request.user,
            time_slot=parsed_time,
            total_quota=total_quota,
            remaining_quota=total_quota  # 初始剩余号量等于总号量
        )

        return JsonResponse({
            'code': 200,
            'message': '号源创建成功',
            'slot_id': str(slot.id)
        })

    except Exception as e:
        return JsonResponse({'code': 500, 'message': f'服务器错误: {str(e)}'}, status=500)


# 取消号源功能
@require_http_methods(["POST"])
def cancel_appointment_slot(request):
    """取消号源（连带处理关联挂号单）"""
    try:
        # 验证用户身份
        if not request.user.is_authenticated or request.user.role != 'doctor':
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