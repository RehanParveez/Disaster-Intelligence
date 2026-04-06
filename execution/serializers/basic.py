from rest_framework import serializers
from execution.models import ExecutionRecord, FailureRecord, Execution

class ExecutionRecordSerializer1(serializers.ModelSerializer):
  class Meta:
    model = ExecutionRecord
    fields = ['execution']

class FailureRecordSerializer1(serializers.ModelSerializer):
  class Meta:
    model = FailureRecord
    fields = ['execution']
    
class ExecutionSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Execution
    fields = ['incident', 'decision',]
