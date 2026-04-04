from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from scheduler.models import IncidentList, Cycle, DecisionRecord
from scheduler.services import run_cycle
from scheduler.serializers.detail import IncidentListSerializer, CycleSerializer, DecisionRecordSerializer
from Disaster_Intelligence.core.permissions import RoleBasedPermission

class SchedulerViewSet(viewsets.ViewSet):
  serializer_class = CycleSerializer
  queryset = Cycle.objects.all()
  permission_classes = [RoleBasedPermission]
  allowed_roles = ['admin', 'authority']
  
  def get_queryset(self):
      user = self.request.user
      if user.is_admin:
        return self.queryset
      return self.queryset
  
  @action(detail=False, methods=['post'])
  def run(self, request):
    cycle = run_cycle()
    return Response({'message': 'the sched. is exec.', 'cycle_id': cycle.id})

  @action(detail=False, methods=['get'])
  def List(self, request):
    data = IncidentList.objects.all().order_by('position')
    serializer = IncidentListSerializer(data, many=True)
    return Response(serializer.data)

  @action(detail=False, methods=['get'])
  def cycles(self, request):
    data = Cycle.objects.all()
    serializer = CycleSerializer(data, many=True)
    return Response(serializer.data)

  @action(detail=False, methods=['get'])
  def decisions(self, request):
    data = DecisionRecord.objects.all()
    serializer = DecisionRecordSerializer(data, many=True)
    return Response(serializer.data)
