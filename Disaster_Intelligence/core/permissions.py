from rest_framework.permissions import BasePermission, SAFE_METHODS

class AdminUserPermission(BasePermission):
  def has_permission(self, request, view):
    if not request.user.is_authenticated:
      return False
    if request.user.is_admin:
      return True     
    return False

class RoleBasedPermission(BasePermission):
  def has_permission(self, request, view):
    if not request.user.is_authenticated:
      return False
    if request.user.is_admin:
      return True

    allowed_roles = getattr(view, 'allowed_roles', None)
    if not allowed_roles:
        return True  
    user_role = request.user.profile.control
    if user_role in allowed_roles:
      return True    
    return False

class OwnerOrCoordinatoPermission(BasePermission):
  def has_permission(self, request, view):
    if not request.user.is_authenticated:
      return False
    return True

  def has_object_permission(self, request, view, obj):
    if request.user.is_admin:
      return True 
    
    user_role = request.user.profile.control
    if user_role == 'authority':
      return True
    if hasattr(obj, 'created_by'):
      if obj.created_by == request.user:
        return True  
    if hasattr(obj, 'reported_by'):
      if obj.reported_by == request.user:
        return True        
    return False

class FieldOperationPermission(BasePermission):
  def has_permission(self, request, view):
    if not request.user.is_authenticated:
      return False
    return True

  def has_object_permission(self, request, view, obj):
    if request.user.is_admin:
      return True  
    user_role = request.user.profile.control
        
    if user_role == 'responder':
      return True
    if user_role == 'authority':
      return True 
    if hasattr(obj, 'created_by'):
      if obj.created_by == request.user:
        return True
    if hasattr(obj, 'reported_by'):
      if obj.reported_by == request.user:
        return True         
    return False

class LogisticsPermission(BasePermission):
  def has_permission(self, request, view):
    if not request.user.is_authenticated:
      return False
    if request.user.is_admin:
      return True

    user_role = request.user.profile.control
    if user_role == 'responder':
      return True
    if user_role == 'authority':
      return True    
    return False

class SelfOnlyPermission(BasePermission):
  def has_permission(self, request, view):
    if not request.user.is_authenticated:
      return False
    return True

  def has_object_permission(self, request, view, obj):
    if request.user.is_admin:
      return True    
    if obj == request.user:
      return True
            
    if hasattr(obj, 'user'):
      if obj.user == request.user:
        return True        
    return False

class ReadOnlyPublicPermission(BasePermission):
  def has_permission(self, request, view):
    if request.method in SAFE_METHODS:
      return True
    if not request.user.is_authenticated:
      return False      
    if request.user.is_admin:
      return True    
    return False