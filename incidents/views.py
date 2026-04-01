from rest_framework import viewsets
from incidents.models import Incident, IncidentReport
from incidents.serializers.detail import IncidentSerializer, IncidentReportSerializer
from incidents.serializers.basic import IncidentReportCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from incidents.services.inc_ser import inc_report, verifiy_inc, reject_inc

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
  
class IncidentReportViewset(viewsets.ModelViewSet):
  serializer_class = IncidentReportSerializer
  queryset = IncidentReport.objects.all()