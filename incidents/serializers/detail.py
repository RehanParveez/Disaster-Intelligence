from rest_framework import serializers
from incidents.models import Incident, IncidentReport

class IncidentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Incident
    fields = ['title', 'location', 'description', 'severity', 'status', 'created_by', 'created_at']
    
class IncidentReportSerializer(serializers.ModelSerializer):
  class Meta:
    model = IncidentReport
    fields = ['incident', 'reported_by', 'description', 'location', 'created_at']