from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from ovp_nonprofits import models

from rest_framework import serializers
from rest_framework import permissions

class NonprofitCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Nonprofit
    fields = ['name', 'image', 'cover', 'details', 'description', 'websitefacebook_page', 'google_page', 'twitter_handle']

  def validate(self, data):
    errors = dict()

    if errors:
      raise serializers.ValidationError(errors)

    return super(NonprofitCreateSerializer, self).validate(data)

class NonprofitUpdateSerializer(NonprofitCreateSerializer):
  class Meta:
    model = models.Nonprofit
    permission_classes = (permissions.IsAuthenticated,)
    fields = ['name', 'image', 'cover', 'details', 'description', 'websitefacebook_page', 'google_page', 'twitter_handle']

class NonprofitSearchSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Nonprofit
    fields = ['id', 'name', 'description', 'details']
