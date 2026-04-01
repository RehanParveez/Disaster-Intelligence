from rest_framework import serializers
from resources.models import Resource, Unit, Availability

class ResourceSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Resource
    fields = ['name']

class UnitSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Unit
    fields = ['kind', 'identifier']
    
class AvailabilitySerializer1(serializers.ModelSerializer):
  class Meta:
    model = Availability
    fields = ['res_kind', 'total_units']