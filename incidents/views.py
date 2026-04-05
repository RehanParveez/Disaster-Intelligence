from rest_framework import viewsets
from incidents.models import Incident, IncidentReport, IncidentGroup, AllocationDecision
from incidents.serializers.detail import IncidentSerializer, IncidentReportSerializer, IncidentGroupSerializer, AllocationDecisionSerializer
from incidents.serializers.basic import IncidentReportCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from incidents.services.inc_ser import inc_report, verifiy_inc, reject_inc
from resources.services import allocate_unit_serv, return_unit_serv
from django.db import transaction
from Disaster_Intelligence.core.permissions import FieldOperationPermission, OwnerOrCoordinatoPermission, ReadOnlyPublicPermission
from scheduler.services import manual_assign, suggest_responders, suggest_resources
from incidents.services.inc_ser import return_unit_delete

# Create your views here.
class IncidentViewset(viewsets.ModelViewSet):
  serializer_class = IncidentSerializer
  queryset = Incident.objects.all()
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  
  # filtering fields
  search_fields = ['title', 'description']
  ordering_fields = ['created_at', 'severity']
  filterset_fields = ['location', 'severity', 'status', 'created_at']
  permission_classes = [FieldOperationPermission]
  
  def get_queryset(self):
    user = self.request.user
    role = user.profile.control

    if user.is_admin:
      return self.queryset
    if role == 'authority':
      return self.queryset
    if role == 'responder':
      verified = self.queryset.filter(status = 'verified')
      own = self.queryset.filter(created_by=user)
      check = verified | own
      check = check.distinct()
      return check
    if role == 'citizen':
      verified = self.queryset.filter(status = 'verified')
      own = self.queryset.filter(created_by=user)
      check = verified | own
      check = check.distinct()
      return check
    
    return self.queryset.none()
  
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
    return_unit_delete(incident=incid, unit_id=unit_id, user=request.user, reason=reason)
    return Response({'message': 'the unit is returned from the incid'})
  
  @action(detail=True, methods=['post'])
  def assign(self, request, pk=None):
    incident = self.get_object()
    
    unit_id = request.data.get('unit_id')
    inventory_id = request.data.get('inventory_id')
    if not unit_id:
      return Response({'detail': 'the unit_id is need.'}, status=400)
    if not inventory_id:
      return Response({'detail': 'the inventory_id is need.'}, status=400)

    decision = manual_assign(incident, unit_id, inventory_id, request.user)
    serializer = AllocationDecisionSerializer(decision)
    return Response(serializer.data, status=201)
  
  @action(detail=True, methods=['get'])
  def suggest_reso(self, request, pk=None):
    incident = self.get_object()
    resources = suggest_resources(incident)
      
    units_list = []
    for unit in resources['units']:
      unit_id = unit.id
      units_list.append(unit_id)
    invents_list = []
    for inventory in resources['inventories']:
      inventory_id = inventory.id
      invents_list.append(inventory_id)
    data = {'units': units_list, 'inventories': invents_list}
    return Response(data, status=200)
  
  @action(detail=True, methods=['get'])
  def suggest_respon(self, request, pk=None):
    responders = suggest_responders()
    data = []
    for res in responders:
      respon = {}
      respon['id'] = res.id
      respon['username'] = res.user.username
      respon['max_load'] = res.max_load
      data.append(respon)
    return Response(data, status=200)

class IncidentReportViewset(viewsets.ModelViewSet):
  serializer_class = IncidentReportSerializer
  queryset = IncidentReport.objects.all()
  permission_classes = [OwnerOrCoordinatoPermission]
  
  def get_queryset(self):
    user = self.request.user
    role = user.profile.control
    if user.is_admin:
      return self.queryset
    if role == 'authority':
      return self.queryset
    if role == 'responder':  
      res = self.queryset.filter(incident__allocations__allocated_by=user)
      res = res.distinct()
      return res

    if role == 'citizen':
      return self.queryset.filter(reported_by=user)
    return self.queryset.none()
  
class IncidentGroupViewset(viewsets.ModelViewSet):
  serializer_class = IncidentGroupSerializer
  queryset = IncidentGroup.objects.all()
  permission_classes = [ReadOnlyPublicPermission]
  
  def get_queryset(self):
    return self.queryset
