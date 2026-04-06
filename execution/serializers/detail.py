from rest_framework import serializers
from execution.models import Execution, ExecutionRecord, FailureRecord
from execution.serializers.basic import ExecutionRecordSerializer1, FailureRecordSerializer1
from incidents.serializers.basic import IncidentSerializer1

class ExecutionSerializer(serializers.ModelSerializer):
  decision_id = serializers.IntegerField(source = 'decision.id', read_only=True)
  cycle_id = serializers.IntegerField(source = 'decision.cycle.id', read_only=True)
  responder_id = serializers.IntegerField(source = 'decision.responder.id', read_only=True)
  incident_title = serializers.CharField(source = 'incident.title', read_only=True)
  exe_records = ExecutionRecordSerializer1(many=True, read_only=True)
  failures = FailureRecordSerializer1(many=True, read_only=True)
  incident = IncidentSerializer1(read_only=True)
  class Meta:
    model = Execution
    fields = ['incident', 'incident_title', 'decision', 'exe_records', 'failures', 'decision_id', 'cycle_id', 'responder_id', 'unit', 'inventory', 'status', 'created_by']

class ExecutionRecordSerializer(serializers.ModelSerializer):
  class Meta:
    model = ExecutionRecord
    fields = ['execution', 'message', 'updated_at']

class FailureRecordSerializer(serializers.ModelSerializer):
  class Meta:
    model = FailureRecord
    fields = ['execution', 'reason', 'updated_at']