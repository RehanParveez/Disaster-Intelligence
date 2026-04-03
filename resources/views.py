from rest_framework import viewsets
from resources.models import Resource, Unit, Availability, Inventory, Consumption
from resources.serializers.detail import ResourceSerializer, UnitSerializer, AvailabilitySerializer, InventorySerializer, ConsumptionSerializer
from rest_framework.decorators import action
from resources.services import create_unit, update_avail
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.
class ResourceViewset(viewsets.ModelViewSet):
  serializer_class = ResourceSerializer
  queryset = Resource.objects.all()

class UnitViewset(viewsets.ModelViewSet):
  serializer_class = UnitSerializer
  queryset = Unit.objects.all()
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  
  # filtering fields
  search_fields = ['reason']
  ordering_fields = ['created_at']
  filterset_fields = ['pres_avail_units', 'change_kind', 'created_at']
  
  def create(self, request):
    unit = create_unit(request.data, request.user)
    return Response({'message': 'the unit is created', 'unit_id': unit.id}, status=201)
  
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
  