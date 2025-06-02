# backends_proj/views/patients.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from backends_proj.models import RegistrationOrder, User, AppointmentSlot, DoctorProfile, PatientInfo
from datetime import datetime, date
from django.utils import timezone
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from dateutil.parser import isoparse
from django.utils.timezone import make_aware
import traceback
import json
import uuid

# 前置工作1：获取医生列表
@api_view(['GET'])
def get_doctors_by_department(request):
    """根据科室ID获取该科室的医生列表"""
    try:
        #user_id = request.GET.get('user_id')
        #role = request.GET.get('role')
        department = request.GET.get('department')
        
        if not department:
            return JsonResponse({'code': 400, 'message': '必须提供科室信息'}, status=400)
        
        # 获取该科室的医生
        doctor_profiles = DoctorProfile.objects.filter(
            department=department,
            user__is_active=True
        ).select_related('user')
        
        # 构造返回数据
        doctors_data = []
        for profile in doctor_profiles:
            doctot_info = {
                'id': profile.user.id,  # 注意：前端使用的是 'id'，不是 'doctor_id'
                'doctor_id': profile.user.id,
                'real_name': profile.user.real_name,  # 注意：前端使用的是 'real_name'
                'doctor_name': profile.user.real_name,
                'biography': profile.biography or '',
                'department': profile.department or ''
            }
            
            doctors_data.append(doctot_info)
        
        return JsonResponse({
            'code': 200,
            'message': '成功获取医生列表',
            'data': doctors_data
        })
        
    except Exception as e:
        print("查询科室医生发生异常：", str(e))
        traceback.print_exc()
        return JsonResponse({'code': 500, 'message': f'服务器错误: {str(e)}'}, status=500)


# 前置工作2：根据医生和日期获取号源
@api_view(['GET'])
def get_slots_by_doctor_and_date(request):
    """根据医生ID和日期获取号源列表"""
    try:
        doctor_id = request.GET.get('doctor_id')
        date_str = request.GET.get('date')  # 格式: YYYY-MM-DD
        
        print(f"查询医生号源 - doctor_id: {doctor_id}, date: {date_str}")
        
        if not doctor_id:
            return JsonResponse({'code': 400, 'message': '必须提供医生ID'}, status=400)
        
        # 验证医生是否存在
        try:
            doctor = User.objects.get(id=doctor_id, role='doctor', is_active=True)
            print(f"找到医生: {doctor.real_name}, ID: {doctor.id}")
        except User.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '医生不存在或已停用'}, status=404)
        
        # 调试：查看该医生的所有号源
        all_doctor_slots = AppointmentSlot.objects.filter(doctor=doctor)
        #print(f"该医生总共有 {all_doctor_slots.count()} 个号源")
        #for slot in all_doctor_slots:
        #    print(f"  号源ID: {slot.id}, 时间: {slot.time_start} - {slot.time_end}, 剩余配额: {slot.remaining_quota}")

        # 构建查询条件
        query_filters = {
            'doctor': doctor,
            #'time_start__gt': timezone.now(),  # 未来时间
            'remaining_quota__gt': 0  # 有剩余配额
        }
        
        # 如果提供了日期，按日期筛选
        if date_str:
            try:
                if 'T' in date_str:
                    # ISO 格式
                    from dateutil.parser import parse
                    parsed_date_time = parse(date_str)
                    target_date = parsed_date_time.date()
                    print(f"解析ISO格式日期: {date_str} -> {target_date}")
                else:
                    # 简单格式: 2025-06-03
                    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    print(f"解析简单格式日期: {date_str} -> {target_date}")

                # 查询该日期的号源
                #query_filters['time_start__date'] = target_date
                # 使用时间范围查询，避免时区问题
                from django.utils import timezone
                from datetime import datetime, timedelta
                
                # 创建当天的开始和结束时间（UTC）
                start_of_day = timezone.make_aware(datetime.combine(target_date, datetime.min.time()))
                end_of_day = start_of_day + timedelta(days=1)
                
                print(f"时间范围查询: {start_of_day} 到 {end_of_day}")
                
                # 使用时间范围查询
                query_filters['time_start__gte'] = start_of_day
                query_filters['time_start__lt'] = end_of_day
                
                print(f"查询条件: {query_filters}")

                
                # 调试：分步查询
                date_slots = AppointmentSlot.objects.filter(
                    doctor=doctor,
                    time_start__gte=start_of_day,
                    time_start__lt=end_of_day
                )
                print(f"该医生在 {target_date} 的号源: {date_slots.count()} 个")
                for slot in date_slots:
                    print(f"  日期号源 - ID: {slot.id}, 时间: {slot.time_start}, 剩余: {slot.remaining_quota}")




            except ValueError:
                return JsonResponse({'code': 400, 'message': '日期格式错误，请使用YYYY-MM-DD格式'}, status=400)
        
        # 获取号源
        slots = AppointmentSlot.objects.filter(**query_filters).order_by('time_start')
        
        print(f"查询到的号源数量: {slots.count()}")

        # 构造返回数据
        slots_data = []
        for slot in slots:
            slots_data.append({
                'slot_id': slot.id,
                #'doctor_name': slot.doctor.real_name,
                #'doctor_id': slot.doctor.id,
                #'date': slot.time_start.strftime('%Y-%m-%d'),
                #'time_start': slot.time_start.strftime('%H:%M'),
                #'time_end': slot.time_end.strftime('%H:%M'),
                'start': slot.time_start.strftime('%H:%M'),
                'end': slot.time_end.strftime('%H:%M'),
                #'time_range': f"{slot.time_start.strftime('%H:%M')}-{slot.time_end.strftime('%H:%M')}",
                #'remaining_quota': slot.remaining_quota,
                #'total_quota': slot.total_quota
            })
        
        return JsonResponse({
            'code': 200,
            'message': '成功获取号源列表',
            'data': slots_data
        })
        
    except Exception as e:
        print("查询医生号源发生异常：", str(e))
        traceback.print_exc()
        return JsonResponse({'code': 500, 'message': f'服务器错误: {str(e)}'}, status=500)



# 功能1：创建挂号
@api_view(['POST'])
def create_registration(request):
    """患者创建挂号（预约）"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        role = data.get('role')
        slot_id = data.get('slot_id')
        
        print(f"接收到创建挂号请求 - user_id: {user_id}, role: {role}, slot_id: {slot_id}")
        
        # 基础校验
        if not user_id or role != 'patient':
            return JsonResponse({'code': 403, 'message': '仅患者可预约挂号'}, status=403)
        
        if not slot_id:
            return JsonResponse({'code': 400, 'message': '必须提供号源ID'}, status=400)
        
        # 获取患者对象
        try:
            patient = User.objects.get(id=user_id, role='patient')
        except User.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '患者用户不存在'}, status=404)
        
        # 获取号源对象
        try:
            slot = AppointmentSlot.objects.get(id=slot_id)
        except AppointmentSlot.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '号源不存在'}, status=404)
        
        # 检查号源时间是否有效（未过期）
        if slot.time_start <= timezone.now():
            return JsonResponse({'code': 400, 'message': '该号源已过期，无法预约'}, status=400)
        
        # 检查剩余配额
        if slot.remaining_quota <= 0:
            return JsonResponse({'code': 400, 'message': '该号源已满，无法预约'}, status=400)
        
        # 检查患者是否已预约该号源
        existing_order = RegistrationOrder.objects.filter(
            patient=patient, 
            slot=slot, 
            status__in=['pending', 'diagnosing']
        ).first()
        
        if existing_order:
            return JsonResponse({'code': 400, 'message': '您已预约该号源，请勿重复预约'}, status=400)
        
        # 检查患者在同一时间段是否有其他预约
        conflicting_orders = RegistrationOrder.objects.filter(
            patient=patient,
            slot__time_start__lt=slot.time_end,
            slot__time_end__gt=slot.time_start,
            status__in=['pending', 'diagnosing']
        )
        
        if conflicting_orders.exists():
            return JsonResponse({'code': 400, 'message': '该时间段您已有其他预约，请选择其他时间'}, status=400)
        
        # 创建挂号单
        order = RegistrationOrder.objects.create(
            #order_id=str(uuid.uuid4()),
            patient=patient,
            slot=slot,
            status='pending',
            #created_at=timezone.now()
        )
        
        # 减少号源剩余配额
        slot.remaining_quota -= 1
        slot.save()
        
        return JsonResponse({
            'code': 200,
            'message': '挂号成功',
            'data': {
                'order_id': order.order_id,
                'doctor_name': slot.doctor.real_name,
                'appointment_time': slot.time_start.strftime('%Y-%m-%d %H:%M'),
                'status': order.status
            }
        })
        
    except Exception as e:
        print("创建挂号发生异常：", str(e))
        traceback.print_exc()
        return JsonResponse({'code': 500, 'message': f'服务器错误: {str(e)}'}, status=500)


# 功能2：查询可用号源（供患者选择）
@api_view(['GET'])
def get_available_slots(request):
    """获取可用号源列表"""
    try:
        user_id = request.GET.get('user_id')
        role = request.GET.get('role')
        
        print(f"查询可用号源 - user_id: {user_id}, role: {role}")
        
        # 基础校验
        if not user_id or role != 'patient':
            return JsonResponse({'code': 403, 'message': '仅患者可查看'}, status=403)
        
        # 获取患者对象（验证身份）
        try:
            patient = User.objects.get(id=user_id, role='patient')
        except User.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '患者用户不存在'}, status=404)
        
        # 获取未来的可用号源
        current_time = timezone.now()
        available_slots = AppointmentSlot.objects.filter(
            time_start__gt=current_time,  # 未来时间
            remaining_quota__gt=0  # 有剩余配额
        ).order_by('time_start')
        
        # 构造返回数据
        slots_data = []
        for slot in available_slots:
            slots_data.append({
                'slot_id': slot.id,
                'doctor_name': slot.doctor.real_name,
                'doctor_id': slot.doctor.id,
                'time_start': slot.time_start.strftime('%Y-%m-%d %H:%M'),
                'time_end': slot.time_end.strftime('%Y-%m-%d %H:%M'),
                'remaining_quota': slot.remaining_quota,
                'total_quota': slot.total_quota
            })
        
        return JsonResponse({
            'code': 200,
            'message': '成功获取可用号源',
            'data': slots_data
        })
        
    except Exception as e:
        print("查询号源发生异常：", str(e))
        traceback.print_exc()
        return JsonResponse({'code': 500, 'message': f'服务器错误: {str(e)}'}, status=500)

# 功能2：查询个人挂号记录
@api_view(['GET'])
def get_patient_orders(request):
    """查询患者的个人挂号记录"""
    try:
        user_id = request.GET.get('user_id')
        role = request.GET.get('role')
        status_filter = request.GET.get('status')  # 可选：按状态筛选
        
        print(f"查询挂号记录 - user_id: {user_id}, role: {role}, status: {status_filter}")
        
        # 基础校验
        if not user_id or role != 'patient':
            return JsonResponse({'code': 403, 'message': '仅患者可查看个人挂号记录'}, status=403)
        
        # 获取患者对象
        try:
            patient = User.objects.get(id=user_id, role='patient')
            print(f"找到患者: {patient.real_name}, ID: {patient.id}")
        except User.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '患者用户不存在'}, status=404)
        
        # 构建查询条件
        query_filters = {'patient': patient}
        if status_filter and status_filter in ['pending', 'diagnosing', 'completed', 'cancelled']:
            query_filters['status'] = status_filter
        
        # 查询挂号记录，按创建时间倒序
        orders = RegistrationOrder.objects.filter(**query_filters).order_by('-timestamp')
        
        print(f"查询条件: {query_filters}")
        print(f"查询到的挂号记录数量: {orders.count()}")

        # 打印具体的挂号记录信息（调试用）
        for order in orders:
            print(f"挂号记录: ID={order.order_id}, 患者={order.patient.real_name}, 医生={order.slot.doctor.real_name}, 状态={order.status}, 时间={order.slot.time_start}")


        # 构造返回数据
        orders_data = []
        for order in orders:
            # 获取挂号状态的中文描述
            status_map = {
                'pending': '待就诊',
                'diagnosing': '就诊中', 
                'completed': '已完成',
                'cancelled': '已取消'
            }
            
            # 判断是否可以取消（只有pending状态且未过就诊时间的可以取消）
            can_cancel = (order.status == 'pending' and 
                         order.slot.time_start > timezone.now())
            
            # 根据 doctor_id 从 DoctorProfile 表中获取科室名称
            try:
                doctor_profile = DoctorProfile.objects.get(user=order.slot.doctor)
                print(f"{doctor_profile}")
                department = doctor_profile.department
            except DoctorProfile.DoesNotExist:
                department = '未知科室'
            print(f"科室名称: {department}")

            order_data = {
                'order_id': order.order_id,
                'slot_id': order.slot.id,
                'department': department,
                'doctor_name': order.slot.doctor.real_name,
                'doctor_id': order.slot.doctor.id,
                'appointment_time': order.slot.time_start.strftime('%Y-%m-%d %H:%M'),
                'appointment_end_time': order.slot.time_end.strftime('%Y-%m-%d %H:%M'),
                'status': order.status,
                'status_display': status_map.get(order.status, order.status),
                'can_cancel': can_cancel,
                #'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                #'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S') if order.updated_at else None
                'timestamp': order.timestamp.strftime('%Y-%m-%d %H:%M:%S') if order.timestamp else None
            }
            orders_data.append(order_data)
            print(f"构造的订单数据: {order_data}")            

        response_data = {
            'code': 200,
            'message': '成功获取挂号记录',
            #'data': {
            #    'total_count': len(orders_data),
            #    'orders': orders_data
            #}
            'data': orders_data
        }

        print(f"返回数据: {response_data}")

        return JsonResponse(response_data)
        
    except Exception as e:
        print("查询挂号记录发生异常：", str(e))
        traceback.print_exc()
        return JsonResponse({'code': 500, 'message': f'服务器错误: {str(e)}'}, status=500)


# 功能2扩展：取消挂号
@api_view(['POST'])
def cancel_registration(request):
    """患者取消挂号"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        role = data.get('role')
        order_id = data.get('order_id')
        
        print(f"取消挂号请求 - user_id: {user_id}, role: {role}, order_id: {order_id}")
        
        # 基础校验
        if not user_id or role != 'patient':
            return JsonResponse({'code': 403, 'message': '仅患者可取消挂号'}, status=403)
        
        if not order_id:
            return JsonResponse({'code': 400, 'message': '必须提供挂号单ID'}, status=400)
        
        # 获取患者对象
        try:
            patient = User.objects.get(id=user_id, role='patient')
        except User.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '患者用户不存在'}, status=404)
        
        # 获取挂号单
        try:
            order = RegistrationOrder.objects.get(order_id=int(order_id), patient=patient)
        except RegistrationOrder.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '挂号单不存在或不属于当前患者'}, status=404)
        
        # 检查是否可以取消
        if order.status != 'pending':
            return JsonResponse({'code': 400, 'message': '只有待就诊状态的挂号可以取消'}, status=400)
        
        # 检查是否已过就诊时间
        if order.slot.time_start <= timezone.now():
            return JsonResponse({'code': 400, 'message': '就诊时间已过，无法取消'}, status=400)
        
        # 执行取消操作
        order.status = 'cancelled'
        #order.updated_at = timezone.now()
        order.save()
        
        # 恢复号源配额
        slot = order.slot
        slot.remaining_quota += 1
        slot.save()
        
        return JsonResponse({
            'code': 200,
            'message': '挂号取消成功',
            'data': {
                'order_id': order.order_id,
                'status': order.status
            }
        })
        
    except Exception as e:
        print("取消挂号发生异常：", str(e))
        traceback.print_exc()
        return JsonResponse({'code': 500, 'message': f'服务器错误: {str(e)}'}, status=500)


# 功能2扩展：获取挂号详情
@api_view(['GET'])
def get_order_detail(request):
    """获取单个挂号单的详细信息"""
    try:
        user_id = request.GET.get('user_id')
        role = request.GET.get('role')
        order_id = request.GET.get('order_id')
        
        print(f"查询挂号详情 - user_id: {user_id}, role: {role}, order_id: {order_id}")
        
        # 基础校验
        if not user_id or role != 'patient':
            return JsonResponse({'code': 403, 'message': '仅患者可查看挂号详情'}, status=403)
        
        if not order_id:
            return JsonResponse({'code': 400, 'message': '必须提供挂号单ID'}, status=400)
        
        # 获取患者对象
        try:
            patient = User.objects.get(id=user_id, role='patient')
        except User.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '患者用户不存在'}, status=404)
        
        # 获取挂号单详情
        try:
            order = RegistrationOrder.objects.get(order_id=int(order_id), patient=patient)
        except RegistrationOrder.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '挂号单不存在或不属于当前患者'}, status=404)
        
        # 状态映射
        status_map = {
            'pending': '待就诊',
            'diagnosing': '就诊中',
            'completed': '已完成', 
            'cancelled': '已取消'
        }
        
        # 判断是否可以取消
        can_cancel = (order.status == 'pending' and 
                     order.slot.time_start > timezone.now())
        
        # 构造详细数据
        order_detail = {
            'order_id': order.order_id,
            'patient_name': order.patient.real_name,
            'doctor_name': order.slot.doctor.real_name,
            'doctor_id': order.slot.doctor.id,
            'appointment_date': order.slot.time_start.strftime('%Y-%m-%d'),
            'appointment_time': order.slot.time_start.strftime('%H:%M'),
            'appointment_end_time': order.slot.time_end.strftime('%H:%M'),
            'status': order.status,
            'status_display': status_map.get(order.status, order.status),
            'can_cancel': can_cancel,
            #'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            #'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S') if order.updated_at else None
            'timestamp': order.timestamp.strftime('%Y-%m-%d %H:%M:%S') if order.timestamp else None
        }
        
        return JsonResponse({
            'code': 200,
            'message': '成功获取挂号详情',
            'data': order_detail
        })
        
    except Exception as e:
        print("查询挂号详情发生异常：", str(e))
        traceback.print_exc()
        return JsonResponse({'code': 500, 'message': f'服务器错误: {str(e)}'}, status=500)
    
# 功能3：获取患者个人信息
@api_view(['GET'])
def get_patient_profile(request):
    """获取患者的基本信息"""
    try:
        user_id = request.GET.get('user_id')
        role = request.GET.get('role')
        
        print(f"查询患者信息 - user_id: {user_id}, role: {role}")
        
        # 基础校验
        if not user_id or role != 'patient':
            return JsonResponse({'code': 403, 'message': '仅患者可查看个人信息'}, status=403)
        
        # 获取患者对象
        try:
            patient = User.objects.get(id=user_id, role='patient', is_active=True)
            print(f"找到患者: {patient.real_name}, ID: {patient.id}")
        except User.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '患者用户不存在或已停用'}, status=404)
        
        # 尝试获取患者扩展信息
        patient_info = None
        try:
            patient_info = PatientInfo.objects.get(user=patient)
            print(f"找到患者扩展信息: {patient_info}")
        except PatientInfo.DoesNotExist:
            print(f"患者 {patient.real_name} 没有扩展信息")
        
        account_state = '正常' if patient.is_active else '停用'

        # 构造返回数据
        profile_data = {
            'user_id': patient.id,
            'username': patient.username,
            'real_name': patient.real_name,
            'phone': patient.phone,
            'id_card': patient.id_card or '',
            'age': patient.age,
            'gender': patient.get_gender_display(),  # 获取性别的显示名称
            'gender_code': patient.gender,  # 性别代码
            'role': patient.role,
            'account_state': account_state,
        }
        
        # 如果有扩展信息，添加到返回数据中
        if patient_info:
            profile_data.update({
                'message': patient_info.message or '',
                'medical_history': patient_info.medical_history or '',
                'allergies': patient_info.allergies or '',
                'emergency_contact': patient_info.emergency_contact or '',
                'emergency_phone': patient_info.emergency_phone or ''
            })
        else:
            # 如果没有扩展信息，设置默认值
            profile_data.update({
                'message': '',
                'medical_history': '',
                'allergies': '',
                'emergency_contact': '',
                'emergency_phone': ''
            })
        
        print(f"返回的患者信息: {profile_data}")
        
        return JsonResponse({
            'code': 200,
            'message': '成功获取患者信息',
            'data': profile_data
        })
        
    except Exception as e:
        print("查询患者信息发生异常：", str(e))
        traceback.print_exc()
        return JsonResponse({'code': 500, 'message': f'服务器错误: {str(e)}'}, status=500)