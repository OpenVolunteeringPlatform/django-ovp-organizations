from ovp_users.models import User

from ovp_core.serializers import EmptySerializer

from ovp_organizations import serializers
from ovp_organizations import models
from ovp_organizations import permissions as organization_permissions

from rest_framework import decorators
from rest_framework import viewsets
from rest_framework import response
from rest_framework import mixins
from rest_framework import pagination
from rest_framework import permissions
from rest_framework import status

from django.shortcuts import get_object_or_404


class OrganizationResourceViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
  """
  OrganizationResourceViewSet resource endpoint
  """
  queryset = models.Organization.objects.all()
  lookup_field = 'slug'
  lookup_value_regex = '[^/]+' # default is [^/.]+ - here we're allowing dots in the url slug field

  def partial_update(self, request, *args, **kwargs):
    """ We do not include the mixin as we want only PATCH and no PUT """
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    if getattr(instance, '_prefetched_objects_cache', None): #pragma: no cover
      instance = self.get_object()
      serializer = self.get_serializer(instance)

    return response.Response(serializer.data)

  @decorators.detail_route(methods=["POST"])
  def invite_user(self, request, *args, **kwargs):
    organization = self.get_object()

    serializer = self.get_serializer_class()(data=request.data)
    serializer.is_valid(raise_exception=True)

    invited = User.objects.get(email=request.data["email"])

    try:
      models.OrganizationInvite.objects.get(organization=organization, invited=invited)
      return response.Response({"email": ["This user is already invited to this organization."]}, status=400)
    except models.OrganizationInvite.DoesNotExist:
      pass

    invite = models.OrganizationInvite(invitator=request.user, invited=invited, organization=organization)
    invite.save()

    organization.mailing().sendUserInvited(context={"invite": invite})

    return response.Response({"detail": "User invited."})

  @decorators.detail_route(methods=["POST"])
  def join(self, request, *args, **kwargs):
    organization = self.get_object()
    organization.members.add(request.user)

    organization.mailing().sendUserJoined(context={"user": request.user, "organization": organization})

    return response.Response({"detail": "Joined organization."})

  @decorators.detail_route(methods=["POST"])
  def revoke_invite(self, request, *args, **kwargs):
    organization = self.get_object()

    try:
      try:
        user = User.objects.get(email=request.data.get("email", ""))
        invite = models.OrganizationInvite.objects.get(invited=user, organization=organization)
      except User.DoesNotExist:
        return response.Response({"email": ["This user is not valid."]}, status=400)
    except models.OrganizationInvite.DoesNotExist:
      return response.Response({"detail": "This user is not invited to this organization."}, status=400)

    organization.mailing().sendUserInvitationRevoked(context={"invite": invite})
    invite.delete()

    return response.Response({"detail": "Invite has been revoked."})

  @decorators.detail_route(methods=["POST"])
  def leave(self, request, *args, **kwargs):
    organization = self.get_object()
    organization.members.remove(request.user)

    organization.mailing().sendUserLeft(context={"user": request.user, "organization": organization})

    return response.Response({"detail": "You've left the organization."})

  @decorators.detail_route(methods=["POST"])
  def remove_member(self, request, *args, **kwargs):
    organization = self.get_object()
    serializer = self.get_serializer_class()

    try:
      user = organization.members.get(email=request.data.get("email", ""))
    except User.DoesNotExist:
      return response.Response({"email": ["This user is not valid."]}, status=400)

    organization.members.remove(user)

    organization.mailing().sendUserRemoved(context={"user": user, "organization": organization})

    return response.Response({"detail": "Member was removed."})

  def get_serializer_class(self):
    request = self.get_serializer_context()['request']
    if self.action in ['create', 'partial_update']:
      return serializers.OrganizationCreateSerializer
    if self.action == 'retrieve':
      return serializers.OrganizationRetrieveSerializer
    if self.action in ['invite_user', 'revoke_invite']:
      return serializers.OrganizationInviteSerializer
    if self.action == 'remove_member':
      return serializers.MemberRemoveSerializer
    if self.action in ['leave', 'join']: # pragma: no cover
      return EmptySerializer


  def get_permissions(self):
    request = self.get_serializer_context()['request']
    if self.action == 'create':
      self.permission_classes = (permissions.IsAuthenticated,)
    if self.action == 'partial_update':
      self.permission_classes = (permissions.IsAuthenticated, organization_permissions.OwnsOrIsOrganizationMember)
    if self.action == 'retrieve':
      self.permission_classes = ()
    if self.action in ['invite_user', 'revoke_invite']:
      self.permission_classes = (permissions.IsAuthenticated, organization_permissions.OwnsOrIsOrganizationMember)
    if self.action == 'join':
      self.permission_classes = (permissions.IsAuthenticated, organization_permissions.IsInvitedToOrganization)
    if self.action == 'leave':
      self.permission_classes = (permissions.IsAuthenticated, organization_permissions.IsOrganizationMember)
    if self.action == 'remove_member':
      self.permission_classes = (permissions.IsAuthenticated, organization_permissions.OwnsOrganization)

    return super(OrganizationResourceViewSet, self).get_permissions()

  def create(self, request, *args, **kwargs):
    request.data['owner'] = request.user.id

    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    organization = serializer.save()
    organization.members.add(request.user)

    headers = self.get_success_headers(serializer.data)
    return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
