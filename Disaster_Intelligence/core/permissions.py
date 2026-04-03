from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class RolePermission(BasePermission):
  def has_permission(self, request, view):
    if not request.user:
      return False
    if not request.user.is_authenticated:
      return False
    allowed_roles = getattr(view, 'allowed_roles', None)
    if not allowed_roles:
      return True
  
    user_role = getattr(request.user.profile, 'control', None)
    return user_role in allowed_roles

class AdminOrOwnerPermission(BasePermission):
  def has_permission(self, request, view):
    user = request.user
    if not user:
      return False
    if not user.is_authenticated:
      return False
    return True

  def has_object_permission(self, request, view, obj):
    if request.user.is_admin:
      return True
    return getattr(obj, 'created_by', None) == request.user

class ReadOnlyOrAdminPermission(BasePermission):
  def has_permission(self, request, view):
    if request.method in SAFE_METHODS:
      return True
    user = request.user
    if not user:
      return False
    if not user.is_admin:
      return False
    return True

class IncidentActorPermission(BasePermission):
  def has_permission(self, request, view):
    user = request.user
    if not user:
      return False
    if not user.is_authenticated:
      return False
    return True

  def has_object_permission(self, request, view, obj):
    user = request.user
    role = getattr(user.profile, 'control', None)
    if user.is_admin:
      return True
    if getattr(obj, 'created_by', None) == user:
      return True
    if role in ['responder', 'authority']:
      return True
    return False

class ResourceActorPermission(BasePermission):
  def has_permission(self, request, view):
    if not request.user:
      return False
    if not request.user.is_authenticated:
      return False

    role = getattr(request.user.profile, 'control', None)
    return role in ['responder', 'authority', 'admin']

class SelfOrAdminPermission(BasePermission):
  def has_permission(self, request, view):
    user = request.user
    if not user:
      return False
    return user.is_authenticated

  def has_object_permission(self, request, view, obj):
    if request.user.is_admin:
      return True
    return obj == request.user
