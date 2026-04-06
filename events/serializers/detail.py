from rest_framework import serializers
from events.models import EventKind, Event, EventRecord
from events.serializers.basic import EventRecordSerializer1

class EventKindSerializer(serializers.ModelSerializer):
  event_records = EventRecordSerializer1(many=True, read_only=True)
  class Meta:
    model = EventKind
    fields = ['name', 'description', 'event_records']

class EventSerializer(serializers.ModelSerializer):
  class Meta:
    model = Event
    fields = ['event_kind', 'payload', 'is_processed']
    
class EventRecordSerializer(serializers.ModelSerializer):
  class Meta:
    model = EventRecord
    fields = ['event', 'status', 'message', 'processed_at']