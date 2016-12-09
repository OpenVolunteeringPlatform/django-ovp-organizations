from django.core.exceptions import ValidationError

from ovp_uploads.serializers import UploadedImageSerializer

from ovp_core import validators as core_validators
from ovp_core.serializers import GoogleAddressSerializer, GoogleAddressCityStateSerializer

from ovp_organizations import models
from ovp_organizations import validators

from rest_framework import serializers
from rest_framework import permissions
from rest_framework import fields

class OrganizationCreateSerializer(serializers.ModelSerializer):
  address = GoogleAddressSerializer(
      validators=[core_validators.address_validate],
      required=False,
    )

  class Meta:
    model = models.Organization
    fields = ['id', 'slug', 'owner', 'name', 'website', 'facebook_page', 'address', 'details', 'description', 'type', 'image', 'cover']

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
  image = UploadedImageSerializer()

  class Meta:
    model = models.Organization
    fields = ['slug', 'owner', 'name', 'website', 'facebook_page', 'address', 'details', 'description', 'type', 'image']

class OrganizationRetrieveSerializer(serializers.ModelSerializer):
  address = GoogleAddressCityStateSerializer()
  image = UploadedImageSerializer()
  cover = UploadedImageSerializer()

  class Meta:
    model = models.Organization
    fields = ['slug', 'owner', 'name', 'website', 'facebook_page', 'address', 'details', 'description', 'type', 'image', 'cover']

class OrganizationInviteSerializer(serializers.Serializer):
  email = fields.EmailField(validators=[validators.invite_email_validator])

  class Meta:
    fields = ['email']

class MemberRemoveSerializer(serializers.Serializer):
  email = fields.EmailField(validators=[validators.invite_email_validator])

  class Meta:
    fields = ['email']
