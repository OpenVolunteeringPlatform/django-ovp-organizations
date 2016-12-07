from ovp_organizations import serializers
from ovp_organizations import models

from rest_framework import decorators, viewsets
from rest_framework import response
from rest_framework import mixins, pagination
from rest_framework import permissions
from rest_framework import status

from django.shortcuts import get_object_or_404

#POST, PUT, PATCH -> /public-profile
#-criar perfil publico
#-editar perfil publico
#-convidar outro usuario pra organização
#-sair da organização
#-email
#
#GET -> /public-profile/:pk
class OrganizationResourceViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
  """
  OrganizationResourceViewSet resource endpoint
  """
  queryset = models.Organization.objects.all()
  lookup_field = 'slug'
  lookup_value_regex = '[^/]+' # default is [^/.]+ - here we're allowing dots in the url slug field

  #def invite_user(self, request, *args, **kwargs):
  #  queryset = self.get_object()
  #  serializer = self.get_serializer(queryset)
  #  return response.Response(serializer.data)

  def get_serializer_class(self):
    request = self.get_serializer_context()['request']
    if self.action == 'create':
      return serializers.OrganizationCreateSerializer
    if self.action == 'retrieve':
      return serializers.OrganizationRetrieveSerializer


  def get_permissions(self):
    request = self.get_serializer_context()['request']
    if self.action == 'create':
      self.permission_classes = (permissions.IsAuthenticated,)
    if self.action == 'retrieve':
      self.permission_classes = ()

    return super(OrganizationResourceViewSet, self).get_permissions()

  def create(self, request, *args, **kwargs):
    request.data['owner'] = request.user.id

    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    organization = serializer.save()
    organization.members.add(request.user)

    headers = self.get_success_headers(serializer.data)
    return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
