from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from ovp_organizations.models import Organization

from ovp_core.mixins import CountryFilterMixin

# This file contains some "pragma: no cover" because the admin
# class is not covered by the test suite


class OrganizationAdmin(admin.ModelAdmin, CountryFilterMixin):
  fields = [
    ('id', 'highlighted'), ('name', 'slug'),
    ('owner'), #- 'type'

    ('published', 'deleted'),
    ('published_date', 'deleted_date'),

    'address',
    'image', 'cover',

    'facebook_page', 'website',

    'description', 'details',
    'causes', 'members',

    ('created_date', 'modified_date'),
    ]

  list_display = [
    'id', 'created_date', 'name', 'owner__email', 'owner__phone', 'address', 'highlighted', 'published', 'deleted', 'modified_date'
  ]

  list_filter = [
    'created_date', 'modified_date', 'highlighted', 'published', 'deleted'
  ]

  list_editable = [
    'highlighted', 'published'
  ]

  search_fields = [
    'name', 'owner__email', 'address__addressline', 'description'
  ]

  readonly_fields = ['id', 'created_date', 'modified_date', 'published_date', 'deleted_date']

  raw_id_fields = [
    'owner'
  ]

  filter_horizontal = ('causes', 'members')

  def owner__name(self, obj): #pragma: no cover
    if obj.owner:
      return obj.owner.name
    else:
      return _('None')
  owner__name.short_description = _("Owner's Name")
  owner__name.admin_order_field = 'owner__name'

  def owner__email(self, obj): #pragma: no cover
    if obj.owner:
      return obj.owner.email
    else:
      return _('None')
  owner__email.short_description = _("Owner's E-mail")
  owner__email.admin_order_field = 'owner__email'

  def owner__phone(self, obj): #pragma: no cover
    if obj.owner:
      return obj.owner.phone
    else:
      return _('None')
  owner__phone.short_description = _("Owner's Phone")
  owner__phone.admin_order_field = 'owner__phone'

  def get_queryset(self, request): #pragma: no cover
    qs = super(OrganizationAdmin, self).get_queryset(request)
    return self.filter_by_country(request, qs, 'address')


admin.site.register(Organization, OrganizationAdmin)


