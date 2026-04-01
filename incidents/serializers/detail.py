from rest_framework import serializers
from incidents.models import Incident, IncidentReport

class IncidentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Incident
    fields = ['title', 'location', 'description', 'severity', 'status', 'created_at']
    read_only_fields = ['status', 'created_at']
    
class IncidentReportSerializer(serializers.ModelSerializer):
  class Meta:
    model = IncidentReport
    fields = ['incident', 'description', 'location', 'created_at']
    read_only_fields = ['created_at']