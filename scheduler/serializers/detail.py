from rest_framework import serializers
from scheduler.models import IncidentList, Cycle, DecisionRecord
from execution.serializers.basic import ExecutionSerializer1

class IncidentListSerializer(serializers.ModelSerializer):
  class Meta:
    model = IncidentList
    fields = ['incident', 'prior', 'position', 'updated_at']

class CycleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cycle
    fields = ['id', 'started_at', 'completed_at', 'total_incids', 'decis_made']
    
class DecisionRecordSerializer(serializers.ModelSerializer):
  executions = ExecutionSerializer1(many=True, read_only=True)
  class Meta:
    model = DecisionRecord
    fields = ['cycle', 'incident', 'executions', 'unit', 'responder', 'reason', 'created_at']