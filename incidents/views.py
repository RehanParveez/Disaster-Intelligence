from rest_framework import viewsets
from incidents.models import Incident, IncidentReport, IncidentGroup, AllocationDecision
from incidents.serializers.detail import IncidentSerializer, IncidentReportSerializer, IncidentGroupSerializer
from incidents.serializers.basic import IncidentReportCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from incidents.services.inc_ser import inc_report, verifiy_inc, reject_inc, group_incid, cal_prior
from resources.services import allocate_unit_serv, return_unit_serv
from django.db import transaction
from Disaster_Intelligence.core.permissions import IncidentActorPermission, RolePermission

# Create your views here.
class IncidentViewset(viewsets.ModelViewSet):
  serializer_class = IncidentSerializer
  queryset = Incident.objects.all()
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  
  # filtering fields
  search_fields = ['title', 'description']
  ordering_fields = ['created_at', 'severity']
  filterset_fields = ['location', 'severity', 'status', 'created_at']
  permission_classes = [IncidentActorPermission, RolePermission]
  allowed_roles = ['admin', 'responder', 'authority']
  
  def get_queryset(self):
    user = self.request.user
    role = getattr(user.profile, 'control', None)

    if user.is_admin:
      return self.queryset
    if role == 'authority':
      return self.queryset

    if role == 'responder':
      verified = self.queryset.filter(status = 'verified')
      own = self.queryset.filter(created_by=user)
      return verified | own

    if role == 'citizen':
      verified = Incident.objects.filter(status = 'verified')
      own = Incident.objects.filter(created_by=user)
      return verified | own
    return self.queryset
  
  @action(detail=False, methods=['post'])
  def report(self, request):
    serializer = IncidentReportCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    incid = inc_report(serializer.validated_data, request.user)
    return Response({'message': 'the incid is reported', 'incident_id': incid.id}, status=201)
  
  @action(detail=True, methods=['post'])
  def verify(self, request, pk=None):
    verifiy_inc(pk, request.user)
    return Response({'message': 'the incid is verified'})
  
  @action(detail=True, methods=['post'])
  def reject(self, request, pk=None):
    reject_inc(pk, request.user)
    return Response({'message': 'the incid is rejected'})
 
  @action(detail=True, methods=['post'])
  def group(self, request, pk=None):
    group = group_incid(pk)
    return Response({'message': 'grouped', 'group_id': group.id})
 
  @action(detail=True, methods=['post'])
  def recal_prior(self, request, pk=None):
    incid = cal_prior(pk)
    return Response({'message': 'the prior is updated', 'prior': incid.prior})
  
  @action(detail=False, methods=['get'])
  def prior_list(self, request):
    incidents = Incident.objects.all().order_by('-prior')
    serializer = self.get_serializer(incidents, many=True)
    return Response(serializer.data)
  
  @action(detail=True, methods=['post'])
  @transaction.atomic
  def allocate_unit(self, request, pk=None):
    incident = self.get_object()
    unit_id = request.data.get('unit_id')
    inventory_id = request.data.get('inventory_id')
    reason = request.data.get('reason')

    if not unit_id:
      return Response({'err': 'the unit_id is need.'}, status=400)
    avail = allocate_unit_serv(unit_id=unit_id, inventory_id=inventory_id, user=request.user, reason=reason)
    AllocationDecision.objects.create(unit_id=unit_id, incident=incident, allocated_by=request.user,
     inventory_id=inventory_id, reason=reason)
    
    return Response({'message': 'the unit is allocated to incid', 'availability': avail.avail_units})

  @action(detail=True, methods=['post'])
  @transaction.atomic
  def return_unit(self, request, pk=None):
    incid = self.get_object()
    unit_id = request.data.get('unit_id')
    reason = request.data.get('reason')

    if not unit_id:
      return Response({'err': 'the unit_id is required'}, status=400)
    alloca = AllocationDecision.objects.filter(unit_id=unit_id, incident=incid)
    alloca = alloca.first()
    if not alloca:
      return Response({'err': 'the unit is not alloca to this incid'}, status=400)
    return_unit_serv(unit_id=unit_id, inventory_id=alloca.inventory_id, user=request.user, reason=reason)

    alloca.delete()
    return Response({'message': 'the unit is returned from the incid'})

class IncidentReportViewset(viewsets.ModelViewSet):
  serializer_class = IncidentReportSerializer
  queryset = IncidentReport.objects.all()
  permission_classes = [IncidentActorPermission]
  
  def get_queryset(self):
    user = self.request.user
    role = getattr(user.profile, 'control', None)
    if user.is_admin:
      return self.queryset
    if role == 'authority':
      return self.queryset

    if role == 'responder':
      incid = self.queryset.filter(incident__allocations__allocated_by=user)
      incid = incid.distinct()
    if role == 'citizen':
        return self.queryset.filter(reported_by=user)
    return self.queryset
  
class IncidentGroupViewset(viewsets.ModelViewSet):
  serializer_class = IncidentGroupSerializer
  queryset = IncidentGroup.objects.all()
  permission_classes = [RolePermission]
  allowed_roles = ['admin', 'responder', 'authority', 'citizen']
  
  def get_queryset(self):
    return self.queryset
  
