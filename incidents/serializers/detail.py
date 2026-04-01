from rest_framework import serializers
from incidents.models import Incident, IncidentReport, IncidentGroup, IncidentPriorRecord
from incidents.serializers.basic import IncidentReportSerializer1, IncidentGroupSerializer1

class IncidentSerializer(serializers.ModelSerializer):
  reports = IncidentReportSerializer1(many=True, read_only=True)
  group = IncidentGroupSerializer1(read_only=True)
  class Meta:
    model = Incident
    fields = ['title', 'location', 'reports', 'description', 'severity', 'prior', 'group', 'status', 'created_at']
    read_only_fields = ['status', 'created_at']
    
class IncidentReportSerializer(serializers.ModelSerializer):
  class Meta:
    model = IncidentReport
    fields = ['incident', 'description', 'location', 'created_at']
    read_only_fields = ['created_at']
    
class IncidentGroupSerializer(serializers.ModelSerializer):
  class Meta:
    model = IncidentGroup
    fields = ['location', 'group_size']
    
class IncidentPriorityRecordSerializer(serializers.ModelSerializer):
  class Meta:
    model = IncidentPriorRecord
    fields = ['incident', 'prev_priority', 'new_priority', 'reason', 'created_at']