from ovp_nonprofits import serializers
from ovp_nonprofits import models

from rest_framework import decorators, viewsets
from rest_framework import response
from rest_framework import mixins, pagination
from rest_framework import permissions

from django.shortcuts import get_object_or_404

#POST, PUT, PATCH -> /public-profile
#-criar perfil publico
#-editar perfil publico
#-convidar outro usuario pra organização
#-sair da organização
#-email
#-admin(visualizar, publicar)
#
#GET -> /public-profile/:pk
class NonprofitResourceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  """
  NonprofitResourceViewSet resource endpoint
  """
  queryset = models.Nonprofit.objects.all()

  def invite_user(self, request, *args, **kwargs):
    queryset = self.get_object()
    serializer = self.get_serializer(queryset)
    return response.Response(serializer.data)

  def get_serializer_class(self):
    request = self.get_serializer_context()['request']
    if self.action == 'create':
      return serializers.NonprofitCreateSerializer
