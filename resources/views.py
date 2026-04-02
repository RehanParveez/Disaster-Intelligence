from rest_framework import viewsets
from resources.models import Resource, Unit, Availability, Inventory, Consumption
from resources.serializers.detail import ResourceSerializer, UnitSerializer, AvailabilitySerializer, InventorySerializer, ConsumptionSerializer
from rest_framework.decorators import action
from resources.services import create_unit, allocate_unit, return_unit, update_avail
from rest_framework.response import Response

# Create your views here.
class ResourceViewset(viewsets.ModelViewSet):
  serializer_class = ResourceSerializer
  queryset = Resource.objects.all()

class UnitViewset(viewsets.ModelViewSet):
  serializer_class = UnitSerializer
  queryset = Unit.objects.all()
  
  def create(self, request):
    unit = create_unit(request.data, request.user)
    return Response({'message': 'the unit is created', 'unit_id': unit.id}, status=201)
  
  @action(detail=True, methods=['post'])
  def allocate(self, request, pk=None):
    invent_id = request.data.get('invent_id')
    reason = request.data.get('reason')
    if not invent_id:
      return Response({'err': 'the invent_id is need.'}, status=400)
  
    avail = allocate_unit(unit_id=pk, invent_id=invent_id, user=request.user, reason=reason)
    serializer = AvailabilitySerializer(avail)
    return Response({'message': 'the unit is allocated', 'availability': serializer.data})
      
  @action(detail=True, methods=['post'])
  def return_unit(self, request, pk=None):
    invent_id = request.data.get('invent_id')
    reason = request.data.get('reason')

    if not invent_id:
      return Response({'err': 'the invent_id is need.'}, status=400)
    avail = return_unit(unit_id=pk, invent_id=invent_id, user=request.user, reason=reason)
    serializer = AvailabilitySerializer(avail)
    return Response({'message': 'the unit is returned', 'availability': serializer.data})
  
  @action(detail=True, methods=['post'])
  def upd_avail(self, request, pk=None):
    avail = update_avail(pk, request.data)
    serializer = AvailabilitySerializer(avail)
    return Response(serializer.data)
  
class AvailabilityViewset(viewsets.ReadOnlyModelViewSet):
  serializer_class = AvailabilitySerializer
  queryset = Availability.objects.all()
  
class InventoryViewSet(viewsets.ModelViewSet):
  serializer_class = InventorySerializer
  queryset = Inventory.objects.all()
  
class ConsumptionViewSet(viewsets.ModelViewSet):
  serializer_class = ConsumptionSerializer
  queryset = Consumption.objects.all()
  
  

