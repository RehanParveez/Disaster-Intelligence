from rest_framework import serializers
from incidents.models import Incident, IncidentReport, IncidentPriorRecord

class IncidentSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Incident
    fields = ['title', 'location', 'description']
    
class IncidentReportSerializer1(serializers.ModelSerializer):
  class Meta:
    model = IncidentReport
    fields = ['incident', 'reported_by']

class IncidentReportCreateSerializer(serializers.Serializer):
  title = serializers.CharField(max_length=60)
  description = serializers.CharField(max_length=80)
  location = serializers.CharField(max_length=55)
  severity = serializers.IntegerField()
  
class IncidentPriorityRecordSerializer1(serializers.ModelSerializer):
  class Meta:
    model = IncidentPriorRecord
    fields = ['incident', 'prev_priority']
  
