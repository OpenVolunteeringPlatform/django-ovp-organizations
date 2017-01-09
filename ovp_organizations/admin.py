from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from ovp_organizations.models import Organization


class OrganizationAdmin(admin.ModelAdmin):
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

  def owner__name(self, obj):
    return obj.owner.name
  owner__name.short_description = _("Owner's Name")
  owner__name.admin_order_field = 'owner__name'

  def owner__email(self, obj):
    return obj.owner.name
  owner__email.short_description = _("Owner's E-mail")
  owner__email.admin_order_field = 'owner__email'

  def owner__phone(self, obj):
    return obj.owner.phone
  owner__phone.short_description = _("Owner's Phone")
  owner__phone.admin_order_field = 'owner__phone'


admin.site.register(Organization, OrganizationAdmin)


