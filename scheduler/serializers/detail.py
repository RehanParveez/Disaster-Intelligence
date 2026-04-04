from rest_framework import serializers
from scheduler.models import IncidentList, Cycle, DecisionRecord

class IncidentListSerializer(serializers.ModelSerializer):
  class Meta:
    model = IncidentList
    fields = ['incident', 'prior', 'position', 'updated_at']

class CycleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cycle
    fields = ['started_at', 'completed_at', 'total_incids', 'decis_made']
    
class DecisionRecordSerializer(serializers.ModelSerializer):
  class Meta:
    model = DecisionRecord
    fields = ['cycle', 'incident', 'unit', 'responder', 'reason', 'created_at']