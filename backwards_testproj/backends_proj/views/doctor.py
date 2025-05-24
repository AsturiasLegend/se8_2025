# backends_proj/views/doctors.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from backends_proj.models import RegistrationOrder, User
import json

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