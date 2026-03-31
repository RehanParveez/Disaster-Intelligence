from rest_framework import viewsets
from incidents.models import Incident, IncidentReport
from incidents.serializers.detail import IncidentSerializer, IncidentReportSerializer

# Create your views here.
class IncidentViewset(viewsets.ModelViewSet):
  serializer_class = IncidentSerializer
  queryset = Incident.objects.all()

class IncidentReportViewset(viewsets.ModelViewSet):
  serializer_class = IncidentReportSerializer
  queryset = IncidentReport.objects.all()