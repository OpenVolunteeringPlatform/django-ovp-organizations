from django.core.exceptions import ValidationError

from ovp_organizations import models

from rest_framework import serializers
from rest_framework import permissions

class NonprofitCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Nonprofit
    fields = ['owner', 'name', 'website', 'facebook_page', 'address', 'details', 'description']

#class NonprofitUpdateSerializer(NonprofitCreateSerializer):
#  class Meta:
#    model = models.Nonprofit
#    permission_classes = (permissions.IsAuthenticated,)
#    fields = ['name', 'image', 'cover', 'details', 'description', 'websitefacebook_page', 'google_page', 'twitter_handle']

#class NonprofitSearchSerializer(serializers.ModelSerializer):
#  class Meta:
#    model = models.Nonprofit
#    fields = ['id', 'name', 'description', 'details']
