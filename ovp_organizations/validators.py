from rest_framework import serializers

from ovp_users.models import User


from django.core.exceptions import ValidationError
from django.core.validators import validate_email



def invite_email_validator(email):
  try:
    validate_email(email)
  except ValidationError as e:
    return True # we let serializers.EmailField validation handle invalid emails

  try:
    User.objects.get(email=email)
  except User.DoesNotExist:
    raise serializers.ValidationError("This user is not valid.")
