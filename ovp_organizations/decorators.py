from functools import wraps

def hide_address(func):
  """ Used to decorate Serializer.to_representation method.
      It hides the address field if the Organization has 'hidden_address' == True
      and the request user is neither owner or member of the organization """
  @wraps(func)
  def _impl(self, instance):
    if instance.hidden_address:
      for i, field in enumerate(self._readable_fields):
        if field.field_name == "address":
          address = self._readable_fields.pop(i)

      ret = func(self, instance)
      self._readable_fields.insert(i, address) # Put address back

      # Add address representation
      request = self.context["request"]
      if request.user == instance.owner or request.user in instance.members.all():
        ret["address"] = self.fields["address"].to_representation(instance.address)
      else:
        ret["address"] = None
    else:
      ret = func(self, instance)

    return ret
  return _impl
