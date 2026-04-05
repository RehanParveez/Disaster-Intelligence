from rest_framework import serializers
from execution.models import Execution, ExecutionRecord, FailureRecord

class ExecutionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Execution
    fields = ['incident', 'unit', 'inventory', 'status', 'created_by', 'created_at', 'updated_at']

class ExecutionRecordSerializer(serializers.ModelSerializer):
  class Meta:
    model = ExecutionRecord
    fields = ['execution', 'message', 'updated_at']

class FailureRecordSerializer(serializers.ModelSerializer):
  class Meta:
    model = FailureRecord
    fields = ['execution', 'reason', 'updated_at']