from django.core.exceptions import ValidationError

from ovp_core import validators as core_validators
from ovp_core.serializers import GoogleAddressSerializer, GoogleAddressCityStateSerializer

from ovp_organizations import models

from rest_framework import serializers
from rest_framework import permissions

class OrganizationCreateSerializer(serializers.ModelSerializer):
  address = GoogleAddressSerializer(
      validators=[core_validators.address_validate],
      required=False,
    )

  class Meta:
    model = models.Organization
    fields = ['id', 'slug', 'owner', 'name', 'website', 'facebook_page', 'address', 'details', 'description', 'type']

  def create(self, validated_data):
    # Address
    address_data = validated_data.pop('address', None)
    if address_data:
      address_sr = GoogleAddressSerializer(data=address_data)
      address = address_sr.create(address_data)
      validated_data['address'] = address

    # Organization
    organization = models.Organization.objects.create(**validated_data)
    return organization

class OrganizationSearchSerializer(serializers.ModelSerializer):
  address = GoogleAddressCityStateSerializer()

  class Meta:
    model = models.Organization
    fields = ['slug', 'owner', 'name', 'website', 'facebook_page', 'address', 'details', 'description', 'type']

class OrganizationRetrieveSerializer(serializers.ModelSerializer):
  address = GoogleAddressCityStateSerializer()

  class Meta:
    model = models.Organization
    fields = ['slug', 'owner', 'name', 'website', 'facebook_page', 'address', 'details', 'description', 'type']
