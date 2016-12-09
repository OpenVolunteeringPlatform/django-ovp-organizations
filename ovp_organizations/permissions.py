from rest_framework import permissions
from rest_framework import exceptions
from ovp_organizations.models import Organization, OrganizationInvite

class OwnsOrIsOrganizationMember(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.user.is_authenticated:
      if obj.owner == request.user:
        return True
      if request.user in obj.members.all():
        return True
      raise exceptions.PermissionDenied() #403
    return False #401 #pragma: no cover

class OwnsOrganization(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.user.is_authenticated:
      if obj.owner == request.user:
        return True
      raise exceptions.PermissionDenied() #403
    return False #401 #pragma: no cover

class IsOrganizationMember(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.user.is_authenticated:
      if request.user in obj.members.all():
        return True
      raise exceptions.PermissionDenied() #403
    return False #401 #pragma: no cover

class IsInvitedToOrganization(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.user.is_authenticated:
      try:
        OrganizationInvite.objects.get(invited=request.user, organization=obj)
        return True
      except OrganizationInvite.DoesNotExist:
        raise exceptions.PermissionDenied() #403
    return False #401 #pragma: no cover
