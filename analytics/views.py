from rest_framework import viewsets
from rest_framework.decorators import action
from analytics.models import ResponseRecord, ResourceEfficiency, ResponderPerformance
from django.db.models import Avg, Sum, Count
from rest_framework.response import Response
from incidents.models import Incident
from Disaster_Intelligence.core.permissions import LogisticsPermission, AdminUserPermission
from Disaster_Intelligence.core.system_services import recal_all_analy, rebalance_resos
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

class AnalyticsViewSet(viewsets.ViewSet):
  permission_classes = [LogisticsPermission]
  
  @method_decorator(cache_page(60 * 2, key_prefix = 'analytics_resp'))
  @action(detail=False, methods=['get'])
  def resp_time(self, request):
    data = ResponseRecord.objects.aggregate(avg_dispatch=Avg('disp_time_sec'), 
      avg_resolution=Avg('total_reso_time'))

    avg_dispatch = data['avg_dispatch']
    if avg_dispatch is None:
      avg_dispatch = 0
    avg_resolution = data['avg_resolution']
    if avg_resolution is None:
      avg_resolution = 0
    total_incidents = ResponseRecord.objects.count()

    return Response({'average_dispatch_seconds': avg_dispatch, 'average_resolution_seconds': avg_resolution,
      'total_incidents_analyzed': total_incidents})
  
  @method_decorator(cache_page(60 * 2, key_prefix = 'analytics_reso'))
  @action(detail=False, methods=['get'])
  def reso_use(self, request):
    usage = ResourceEfficiency.objects.values('reso_kind__name').annotate(total_allocations=Sum('alloca_count'),
      total_failures=Sum('failure_count')).order_by('-total_allocations')
    return Response(usage)

  @action(detail=False, methods=['get'])
  def incid_load(self, request):
    load = Incident.objects.values('status').annotate(count=Count('id')).order_by('-count')
    return Response({'current_load': load, 'total_active_incidents': Incident.objects.filter(status = 'active').count()})
  
  @method_decorator(cache_page(60 * 2, key_prefix = 'analytics_perf'))
  @action(detail=False, methods=['get'])
  def respond_performance(self, request):
    performance = ResponderPerformance.objects.values('responder__user__username').annotate(total_handled=Sum('incid_handl'),
      total_successes=Sum('succ_exec'), avg_peak_load=Avg('avg_peak_load')).order_by('-total_successes')
    return Response(performance)

class SystemViewSet(viewsets.ViewSet):
  permission_classes = [AdminUserPermission]
  
  @action(detail=False, methods=['post'])
  def recal_all(self, request):
    result = recal_all_analy()
    cache.clear()
    return Response({'status': 'success', 'message': 'the system analy are resync.', 'details': result}, status=200)

  @action(detail=False, methods=['post'])
  def rebalance(self, request):
    force_refresh = request.query_params.get('force')
    if force_refresh == 'true':
      cache.delete('system_rebalance_data')
    check_data = rebalance_resos()
    return Response({'status': 'success', 'message': 'the reso. rebal is done', 'results': check_data}, status=200)
