from rest_framework import serializers
from responders.serializers.basic import CapabilitySerializer1
from responders.models import Responder, Capability, Shift, Load
from accounts.serializers.basic import UserSerializer1
from responders.serializers.basic import ShiftSerializer1

class ResponderSerializer(serializers.ModelSerializer):
  user = UserSerializer1(read_only=True)
  skills = CapabilitySerializer1(many=True, read_only=True)
  shifts = ShiftSerializer1(many=True, read_only=True)
  class Meta:
    model = Responder
    fields = ['user', 'max_load', 'skills', 'shifts']

class CapabilitySerializer(serializers.ModelSerializer):
  class Meta:
    model = Capability
    fields = ['id', 'name']

class ShiftSerializer(serializers.ModelSerializer):
  class Meta:
    model = Shift
    fields = ['id', 'start_time', 'end_time']
    
class LoadSerializer(serializers.ModelSerializer):
  class Meta:
    model = Load
    fields = ['responder', 'incident', 'units_assigned', 'load_count']
