from django.core.exceptions import ValidationError

from ovp_core import validators as core_validators
from ovp_core.serializers import GoogleAddressSerializer

from ovp_organizations import models

from rest_framework import serializers
from rest_framework import permissions

class OrganizationCreateSerializer(serializers.ModelSerializer):
  address = GoogleAddressSerializer(
      validators=[core_validators.address_validate]
    )

  class Meta:
    model = models.Organization
    fields = ['id', 'owner', 'name', 'website', 'facebook_page', 'address', 'details', 'description', 'type']

  def create(self, validated_data):
    # Address
    address_data = validated_data.pop('address', {})
    address_sr = GoogleAddressSerializer(data=address_data)
    address = address_sr.create(address_data)
    validated_data['address'] = address

    # Organization
    organization = models.Organization.objects.create(**validated_data)
    return organization

#class NonprofitUpdateSerializer(NonprofitCreateSerializer):
#  class Meta:
#    model = models.Nonprofit
#    permission_classes = (permissions.IsAuthenticated,)
#    fields = ['name', 'image', 'cover', 'details', 'description', 'websitefacebook_page', 'google_page', 'twitter_handle']

class OrganizationSearchSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Organization
    fields = ['id', 'owner', 'name', 'website', 'facebook_page', 'address', 'details', 'description', 'type']
