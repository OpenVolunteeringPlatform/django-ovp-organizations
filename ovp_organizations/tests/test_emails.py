from django.test import TestCase
from django.core import mail

from ovp_core.helpers import get_email_subject, is_email_enabled
from ovp_users.models import User
from ovp_organizations.models import Organization

class TestEmailTriggers(TestCase):
  def setUp(self):
    user = User.objects.create_user(email="test_project@project.com", password="test_project")
    user.save()

    mail.outbox = [] # Mails sent before creating don't matter
    organization = Organization(name="test organization", type=0, owner=user)
    organization.save()
    self.organization = organization

  def test_organization_creation_trigger_email(self):
    """Assert that email is triggered when creating an organization"""
    if is_email_enabled("organizationCreated"): # pragma: no cover
      self.assertTrue(len(mail.outbox) == 1)
      self.assertTrue(mail.outbox[0].subject == get_email_subject("organizationCreated", "Your organization was created"))
    else: # pragma: no cover
      self.assertTrue(len(mail.outbox) == 0)

  def test_organization_publishing_trigger_email(self):
    """Assert that email is triggered when publishing an organization"""
    mail.outbox = []
    self.organization.published = True
    self.organization.save()

    if is_email_enabled("organizationPublished"): # pragma: no cover
      self.assertTrue(len(mail.outbox) == 1)
      self.assertTrue(mail.outbox[0].subject == get_email_subject("organizationPublished", "Your organization was published"))
    else: # pragma: no cover
      self.assertTrue(len(mail.outbox) == 0)
