from rest_framework import serializers
from resources.models import Resource, Unit, Availability
from resources.serializers.basic import UnitSerializer1, AvailabilitySerializer1

class ResourceSerializer(serializers.ModelSerializer):
  units = UnitSerializer1(many=True, read_only=True)
  class Meta:
    model = Resource
    fields = ['name', 'description', 'units']

class UnitSerializer(serializers.ModelSerializer):
  availability = AvailabilitySerializer1(read_only=True)
  class Meta:
    model = Unit
    fields = ['kind', 'identifier', 'availability', 'location', 'created_by']
    
class AvailabilitySerializer(serializers.ModelSerializer):
  class Meta:
    model = Availability
    fields = ['res_kind', 'total_units', 'avail_units', 'location', 'last_updated']