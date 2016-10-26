from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from ovp_nonprofits import models

from rest_framework import serializers
from rest_framework import permissions

class NonprofitCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Nonprofit
    fields = ['id', 'name', 'email', 'password']
    extra_kwargs = {'password': {'write_only': True}}

  def validate(self, data):
    errors = dict()

    if data.get('password'):
      password = data.get('password', '')
      try:
        validate_password(password=password)
      except ValidationError as e:
        errors['password'] = list(e.messages)

    if errors:
      raise serializers.ValidationError(errors)

    return super(NonprofitCreateSerializer, self).validate(data)

class NonprofitUpdateSerializer(NonprofitCreateSerializer):
  class Meta:
    model = models.Nonprofit
    permission_classes = (permissions.IsAuthenticated,)
    fields = ['password']
    extra_kwargs = {'password': {'write_only': True}}

class NonprofitSearchSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Nonprofit
    fields = ['id', 'name', 'description']

class RecoveryTokenSerializer(serializers.Serializer):
  email = serializers.CharField(required=True)

  class Meta:
    fields = ['email']

class RecoverPasswordSerializer(serializers.Serializer):
  email = serializers.CharField(required=True)
  token = serializers.CharField(required=True)
  new_password = serializers.CharField(required=True)

  class Meta:
    fields = ['email', 'token', 'new_password']
