from rest_framework import viewsets
from execution.serializers.detail import ExecutionSerializer, ExecutionRecordSerializer, FailureRecordSerializer
from execution.models import Execution
from Disaster_Intelligence.core.permissions import FieldOperationPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from execution.services import start_exec, update_exec, complete_exec, fail_exec

# Create your views here.
class ExecutionViewset(viewsets.ModelViewSet):
  serializer_class = ExecutionSerializer
  queryset = Execution.objects.all()
  permission_classes = [FieldOperationPermission]
  allowed_roles = ['admin', 'authority', 'responder']
  
  def get_queryset(self):
    user = self.request.user
    if user.is_admin:
      return self.queryset
    role = user.profile.control
    
    if role == 'authority':
      return self.queryset
    if role == 'responder': 
      check = self.queryset.filter(incident__loads__responder__user=user)
      check = check.distinct()
    return self.queryset.none()
  
  @action(detail=True, methods=['post'])
  def start(self, request, pk=None):
    exec_obj = start_exec(pk)
    return Response({'message': 'the exec. is started', 'status': exec_obj.status}, status=200)

  @action(detail=True, methods=['post'])
  def update_exec(self, request, pk=None):
    message = request.data.get('message')
    if not message:
      return Response({'error': 'the message is need.'}, status=400)
    exec_obj = update_exec(pk, message)
    return Response({'message': 'the exec. is updat', 'status': exec_obj.status}, status=200)

  @action(detail=True, methods=['post'])
  def complete(self, request, pk=None):
    exec_obj = complete_exec(pk)
    return Response({'message': 'the exec. is comple.', 'status': exec_obj.status}, status=200)

  @action(detail=True, methods=['post'])
  def fail(self, request, pk=None):
    reason = request.data.get('reason')
    if not reason:
      return Response({'err': 'reason is required'}, status=400)
    exec_obj = fail_exec(pk, reason)
    return Response({'message': 'the exec has failed', 'status': exec_obj.status}, status=200)

  @action(detail=True, methods=['get'])
  def records_exec(self, request, pk=None):
    exec_obj = self.get_object()
    recs = exec_obj.exe_records.all()
    serializer = ExecutionRecordSerializer(recs, many=True)
    return Response(serializer.data)

  @action(detail=True, methods=['get'])
  def failures(self, request, pk=None):
    exec_obj = self.get_object()
    fails = exec_obj.failures.all()
    serializer = FailureRecordSerializer(fails, many=True)
    return Response(serializer.data)