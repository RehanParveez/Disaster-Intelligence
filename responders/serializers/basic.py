from rest_framework import serializers
from responders.models import Capability, Shift, Responder
from accounts.serializers.basic import UserSerializer1

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
    
class ShiftSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Shift
    fields = ['id', 'start_time']
    
class ResponderSerializer1(serializers.ModelSerializer):
  user = UserSerializer1(read_only=True)
  class Meta:
    model = Responder
    fields = ['user', 'max_load']
    

    

