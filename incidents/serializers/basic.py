from rest_framework import serializers
from incidents.models import Incident, IncidentReport, IncidentGroup

class IncidentSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Incident
    fields = ['title', 'location', 'description']
    
class IncidentReportSerializer1(serializers.ModelSerializer):
  class Meta:
    model = IncidentReport
    fields = ['incident']

class IncidentReportCreateSerializer(serializers.Serializer):
  title = serializers.CharField(max_length=60)
  description = serializers.CharField(max_length=80)
  location = serializers.CharField(max_length=55)
  severity = serializers.IntegerField()
  
class IncidentGroupSerializer1(serializers.ModelSerializer):
  class Meta:
    model = IncidentGroup
    fields = ['location']
  
