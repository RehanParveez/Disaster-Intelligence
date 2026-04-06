from rest_framework import serializers
from events.models import EventRecord
    
class EventRecordSerializer1(serializers.ModelSerializer):
  class Meta:
    model = EventRecord
    fields = ['event', 'status']