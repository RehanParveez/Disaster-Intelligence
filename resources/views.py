from rest_framework import viewsets
from resources.models import Resource, Unit, Availability, Inventory, Consumption
from resources.serializers.detail import ResourceSerializer, UnitSerializer, AvailabilitySerializer, InventorySerializer, ConsumptionSerializer
from rest_framework.decorators import action
from resources.services import create_unit, update_avail
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from Disaster_Intelligence.core.permissions import LogisticsPermission, ReadOnlyPublicPermission

# Create your views here.
class ResourceViewset(viewsets.ModelViewSet):
  serializer_class = ResourceSerializer
  queryset = Resource.objects.all()
  permission_classes = [LogisticsPermission]
  
  def get_queryset(self):
    return self.queryset

class UnitViewset(viewsets.ModelViewSet):
  serializer_class = UnitSerializer
  queryset = Unit.objects.all()
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  
  # filtering fields
  search_fields = ['reason']
  ordering_fields = ['created_at']
  permission_classes = [LogisticsPermission]
  allowed_roles = ['admin', 'responder', 'authority']
  
  def get_queryset(self):
    user = self.request.user
    if user.is_admin:
      return self.queryset
    role = user.profile.control
    user_loc = user.profile.location

    if role == 'authority':
      return self.queryset
    if role == 'responder':
      return self.queryset.filter(location=user_loc)
    return self.queryset.filter(created_by=user)
  
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
  permission_classes = [ReadOnlyPublicPermission]
  
  def get_queryset(self):
    return self.queryset
  
class InventoryViewSet(viewsets.ModelViewSet):
  serializer_class = InventorySerializer
  queryset = Inventory.objects.all()
  permission_classes = [LogisticsPermission]
  allowed_roles = ['admin', 'responder', 'authority']
  
  def get_queryset(self):
    user = self.request.user
    if user.is_admin:
      return self.queryset    
    role = user.profile.control
    user_location = user.profile.location

    if role == 'authority':
      return self.queryset
    if role == 'responder':
      return self.queryset.filter(location=user_location)
    return self.queryset.none()
  
class ConsumptionViewSet(viewsets.ModelViewSet):
  serializer_class = ConsumptionSerializer
  queryset = Consumption.objects.all()
  permission_classes = [LogisticsPermission]
 
  def get_queryset(self):
    user = self.request.user
    if user.is_admin:
      return self.queryset
  
    role = user.profile.control
    if role == 'authority':
      return self.queryset
    return self.queryset.filter(created_by=user)
  