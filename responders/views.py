from rest_framework import viewsets
from responders.models import Responder, Capability, Load
from rest_framework.decorators import action
from responders.serializers.basic import RegisterResponderSerializer, AvailabilitySerializer, AddSkillSerializer
from responders.services import register_respon, set_avail
from rest_framework.response import Response
from responders.serializers.detail import ResponderSerializer, ShiftSerializer, CapabilitySerializer, LoadSerializer
from Disaster_Intelligence.core.permissions import FieldOperationPermission, ReadOnlyPublicPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.core.cache import cache
from responders.selectors import balanced_respons

class ResponderViewSet(viewsets.ModelViewSet):
  queryset = Responder.objects.all()
  serializer_class = ResponderSerializer
  permission_classes = [FieldOperationPermission]
  filter_backends = [DjangoFilterBackend, OrderingFilter]
  
  # filtering fields
  ordering_fields = ['max_load']
  filterset_fields = ['max_load']

  def get_queryset(self):
    user = self.request.user
    cache_key = f'resp_list_user_{user.id}'
    cached_query = cache.get(cache_key)
    if cached_query is not None:
      return cached_query
  
    if user.is_admin:
      check = self.queryset
    else:  
      role = user.profile.control
      if role == 'authority':
        check = self.queryset
      elif role == 'responder':
        check = self.queryset.filter(user=user)
      else:
        check = self.queryset.none()
    cache.set(cache_key, check, 150)
    return check

  @action(detail=False, methods=['post'])
  def register(self, request):
    serializer = RegisterResponderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    respon = register_respon(user=request.user, data=serializer.validated_data)
    return Response(ResponderSerializer(respon).data, status=201)

  @action(detail=True, methods=['post'])
  def set_availability(self, request, pk=None):
    serializer = AvailabilitySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    shift = set_avail(responder_id=pk, schedule=serializer.validated_data)
    return Response(ShiftSerializer(shift).data, status=201)

  @action(detail=True, methods=['post'])
  def skill(self, request, pk=None):
    serializer = AddSkillSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    respon = self.get_object()

    skill_id = serializer.validated_data['skill_id']
    skill = Capability.objects.filter(id=skill_id)
    skill = skill.first()

    if not skill:
      return Response({'error': 'the skill is not pres.'}, status=400)
    respon.skills.add(skill)
    return Response({'message': 'the skill is added'})

  @action(detail=False, methods=['get'])
  def smart_recommens(self, request):
    skill_ids = request.query_params.getlist('skills')
    respon = balanced_respons(required_skills=skill_ids)
    
    serializer = self.get_serializer(respon, many=True)
    return Response(serializer.data)

class CapabilityViewSet(viewsets.ModelViewSet):
  queryset = Capability.objects.all()
  serializer_class = CapabilitySerializer
  permission_classes = [ReadOnlyPublicPermission]
  
  def get_queryset(self):
    return self.queryset

class LoadViewSet(viewsets.ModelViewSet):
  queryset = Load.objects.all()
  serializer_class = LoadSerializer
  permission_classes = [FieldOperationPermission]
  filter_backends = [DjangoFilterBackend, OrderingFilter]
  
  # filtering fields
  ordering_fields = ['load_count']
  filterset_fields = ['responder', 'incident']
  
  def get_queryset(self):
    user = self.request.user
    if user.is_admin:
      return self.queryset
    role = getattr(user.profile, 'control', None)
    if role == 'authority':
      return self.queryset 
    if role == 'responder':
      return self.queryset.filter(responder__user=user)
    return self.queryset.none()
