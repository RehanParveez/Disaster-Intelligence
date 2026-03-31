from rest_framework import serializers
from incidents.models import Incident, IncidentReport

class IncidentSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Incident
    fields = ['title', 'location', 'description']
    
class IncidentReportSerializer1(serializers.ModelSerializer):
  class Meta:
    model = IncidentReport
    fields = ['incident', 'reported_by']