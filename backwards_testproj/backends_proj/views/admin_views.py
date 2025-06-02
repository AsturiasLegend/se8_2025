from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from datetime import datetime, timedelta
from ..models import Department, DoctorDepartment, DepartmentSchedule, SystemMetrics, User
from ..serializers import (
    DepartmentSerializer, DoctorDepartmentSerializer,
    DepartmentScheduleSerializer, SystemMetricsSerializer
)

class DepartmentViewSet(viewsets.ModelViewSet):
    """科室管理视图集"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DoctorDepartmentViewSet(viewsets.ModelViewSet):
    """医生科室管理视图集"""
    queryset = DoctorDepartment.objects.all()
    serializer_class = DoctorDepartmentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        department_id = self.request.query_params.get('department_id')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset

class DepartmentScheduleViewSet(viewsets.ModelViewSet):
    """科室排班管理视图集"""
    queryset = DepartmentSchedule.objects.all()
    serializer_class = DepartmentScheduleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        department_id = self.request.query_params.get('department_id')
        date = self.request.query_params.get('date')
        
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        if date:
            queryset = queryset.filter(date=date)
        return queryset

    @action(detail=False, methods=['post'])
    def batch_create(self, request):
        """批量创建排班"""
        department_id = request.data.get('department_id')
        date = request.data.get('date')
        time_slots = request.data.get('time_slots', [])
        total_quota = request.data.get('total_quota', 20)

        if not all([department_id, date, time_slots]):
            return Response(
                {'error': '缺少必要参数'},
                status=status.HTTP_400_BAD_REQUEST
            )

        schedules = []
        for time_slot in time_slots:
            schedule = DepartmentSchedule(
                department_id=department_id,
                date=date,
                time_slot=time_slot,
                total_quota=total_quota,
                remaining_quota=total_quota
            )
            schedules.append(schedule)

        DepartmentSchedule.objects.bulk_create(schedules)
        return Response({'message': '批量创建成功'})

class SystemMetricsViewSet(viewsets.ModelViewSet):
    """系统指标视图集"""
    queryset = SystemMetrics.objects.all()
    serializer_class = SystemMetricsSerializer

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """获取仪表盘数据"""
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)

        # 获取最近7天的数据
        metrics = self.queryset.filter(date__gte=week_ago, date__lte=today)
        
        # 计算总体指标
        total_appointments = metrics.aggregate(
            total=Count('total_appointments'),
            completed=Count('completed_appointments'),
            canceled=Count('canceled_appointments'),
            no_show=Count('no_show_appointments')
        )

        # 获取科室预约统计
        department_stats = DepartmentSchedule.objects.filter(
            date__gte=week_ago,
            date__lte=today
        ).values(
            'department__name'
        ).annotate(
            total=Count('id'),
            remaining=Count('remaining_quota')
        )

        return Response({
            'overall_metrics': total_appointments,
            'department_stats': department_stats,
            'daily_metrics': self.serializer_class(metrics, many=True).data
        }) 