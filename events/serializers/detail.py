from rest_framework import serializers
from events.models import EventKind, Event, EventRecord
from events.serializers.basic import EventRecordSerializer1

class EventKindSerializer(serializers.ModelSerializer):
  event_records = EventRecordSerializer1(many=True, read_only=True)
  
  class Meta:
    model = EventKind
    fields = ['name', 'kind_name', 'description', 'event_records']

class EventSerializer(serializers.ModelSerializer):
  kind_name = serializers.CharField(write_only=True)
  class Meta:
    model = Event
    fields = ['event_kind', 'kind_name', 'payload', 'is_processed']
    extra_kwargs = {'event_kind': {'required': False}}
  
  def create(self, validated_data):
    kind_name = validated_data.pop('kind_name')
    kind, _ = EventKind.objects.get_or_create(name=kind_name)
    event = Event.objects.create(event_kind=kind, **validated_data)
    return event
    
class EventRecordSerializer(serializers.ModelSerializer):
  class Meta:
    model = EventRecord
    fields = ['event', 'status', 'message', 'processed_at']