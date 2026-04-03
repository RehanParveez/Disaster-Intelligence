from rest_framework import serializers
from responders.models import Capability, Load

class RegisterResponderSerializer(serializers.Serializer):
  max_load = serializers.IntegerField(required=False)
  skills = serializers.ListField(child=serializers.IntegerField(), required=False)

class AvailabilitySerializer(serializers.Serializer):
  start_time = serializers.DateTimeField()
  end_time = serializers.DateTimeField()

class AddSkillSerializer(serializers.Serializer):
    skill_id = serializers.IntegerField()
    
class CapabilitySerializer1(serializers.ModelSerializer):
  class Meta:
    model = Capability
    fields = ['id', 'name']
    
class LoadSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Load
    fields = ['responder', 'incident']