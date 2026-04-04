from rest_framework import serializers
from incidents.models import Incident, IncidentReport, IncidentGroup, IncidentPriorRecord, AllocationDecision
from incidents.serializers.basic import IncidentReportSerializer1, IncidentGroupSerializer1, IncidentPriorityRecordSerializer1

class IncidentSerializer(serializers.ModelSerializer):
  reports = IncidentReportSerializer1(many=True, read_only=True)
  group = IncidentGroupSerializer1(read_only=True)
  prior_records = IncidentPriorityRecordSerializer1(many=True, read_only=True,)
  class Meta:
    model = Incident
    fields = ['title', 'location', 'reports', 'description', 'severity', 'prior', 'prior_records', 'group', 'status', 'created_by', 'created_at']
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
    
class AllocationDecisionSerializer(serializers.ModelSerializer):
  class Meta:
    model = AllocationDecision
    fields = ['unit', 'incident', 'allocated_by', 'inventory', 'reason', 'created_at']
    
    