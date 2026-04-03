from rest_framework import viewsets
from responders.models import Responder, Capability
from rest_framework.decorators import action
from responders.serializers.basic import RegisterResponderSerializer, AvailabilitySerializer, AddSkillSerializer
from responders.services import register_respon, set_avail
from rest_framework.response import Response
from responders.serializers.detail import ResponderSerializer, ShiftSerializer, CapabilitySerializer
from Disaster_Intelligence.core.permissions import FieldOperationPermission, ReadOnlyPublicPermission

class ResponderViewSet(viewsets.ModelViewSet):
  queryset = Responder.objects.all()
  serializer_class = ResponderSerializer
  permission_classes = [FieldOperationPermission]

  def get_queryset(self):
    user = self.request.user
    if user.is_admin:
      return self.queryset
            
    role = user.profile.control
    if role == 'authority':
      return self.queryset
    if role == 'responder':
      return self.queryset.filter(user=user)
    return self.queryset.none()

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

class CapabilityViewSet(viewsets.ModelViewSet):
  queryset = Capability.objects.all()
  serializer_class = CapabilitySerializer
  permission_classes = [ReadOnlyPublicPermission]
  
  def get_queryset(self):
    return self.queryset
