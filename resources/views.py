from rest_framework import viewsets
from resources.models import Resource, Unit, Availability
from resources.serializers.detail import ResourceSerializer, UnitSerializer, AvailabilitySerializer
from rest_framework.decorators import action
from resources.services import create_reso, update_avail
from rest_framework.response import Response

# Create your views here.
class ResourceViewset(viewsets.ModelViewSet):
  serializer_class = ResourceSerializer
  queryset = Resource.objects.all()

class UnitViewset(viewsets.ModelViewSet):
  serializer_class = UnitSerializer
  queryset = Unit.objects.all()
  
  def create(self, request):
    unit = create_reso(request.data, request.user)
    return Response({'message': 'the reso is created', 'unit_id': unit.id}, status=201)
  
  @action(detail=True, methods=['post'])
  def upd_avail(self, request, pk=None):
    avail = update_avail(pk, request.data)
    serializer = AvailabilitySerializer(avail)
    return Response(serializer.data)
  
class AvailabilityViewset(viewsets.ReadOnlyModelViewSet):
  serializer_class = AvailabilitySerializer
  queryset = Availability.objects.all()
