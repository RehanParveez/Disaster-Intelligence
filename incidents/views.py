from rest_framework import viewsets
from incidents.models import Incident, IncidentReport, IncidentGroup
from incidents.serializers.detail import IncidentSerializer, IncidentReportSerializer, IncidentGroupSerializer
from incidents.serializers.basic import IncidentReportCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from incidents.services.inc_ser import inc_report, verifiy_inc, reject_inc, group_incid, cal_prior

# Create your views here.
class IncidentViewset(viewsets.ModelViewSet):
  serializer_class = IncidentSerializer
  queryset = Incident.objects.all()
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  
  # filtering fields
  search_fields = ['title', 'description']
  ordering_fields = ['created_at', 'severity']
  filterset_fields = ['location', 'severity', 'status', 'created_at']
  
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
  
class IncidentReportViewset(viewsets.ModelViewSet):
  serializer_class = IncidentReportSerializer
  queryset = IncidentReport.objects.all()
  
class IncidentGroupViewset(viewsets.ModelViewSet):
  serializer_class = IncidentGroupSerializer
  queryset = IncidentGroup.objects.all()
  
