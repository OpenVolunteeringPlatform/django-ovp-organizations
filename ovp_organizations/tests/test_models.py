from django.test import TestCase

from ovp_organizations.models import Organization
from ovp_users.models import User

class OrganizationModelTestCase(TestCase):
  def setUp(self):
    user = User.objects.create_user(email="testemail@email.com", password="test_returned")
    user.save()
    self.user = user

    organization = Organization(name="test organization", slug="overriden", owner=user, type=0, published=True)
    organization.save()
    self.organization = organization


  def test_str_method_returns_organization_name(self):
    """ Assert that Organization.__str__() method returns organization name """

    self.assertTrue(self.organization.__str__() == "test organization")


  def test_organization_delete(self):
    """ Assert that Organization.delete() method sets .deleted=True """

    self.assertTrue(self.organization.deleted == False)
    self.assertTrue(self.organization.published == True)
    self.assertTrue(self.organization.deleted_date == None)

    self.organization.delete()

    self.assertTrue(self.organization.deleted == True)
    self.assertTrue(self.organization.published == False)
    self.assertTrue(self.organization.deleted_date)


  def test_organization_publish(self):
    """ Assert that setting Organization.published=True updates published_date """

    organization = Organization(name="test organization", owner=self.user, type=0)
    organization.save()

    self.assertTrue(organization.published == False)
    self.assertTrue(organization.published_date == None)

    organization.published = True
    organization.save()

    self.assertTrue(organization.published == True)
    self.assertTrue(organization.published_date)


  def test_excerpt_from_details(self):
    """ Assert that if an organization has no .description, it will use 100 chars from .details as an excerpt """
    small_details = ("a" * 100)
    details = ("a" * 100) + "b"
    expected_description = "a" * 100

    organization = Organization(name="test organization", owner=self.user, type=0, published=True, details=details)
    organization.save()

    organization = Organization.objects.get(pk=organization.id)
    self.assertTrue(organization.description == expected_description)

    organization = Organization(name="test organization", owner=self.user, type=0, published=True, details=small_details)
    organization.save()

    organization = Organization.objects.get(pk=organization.id)
    self.assertTrue(organization.description == small_details)


  def test_slug_generation_on_create(self):
    """ Assert that slug is generated on create """
    self.assertTrue(self.organization.slug == "test-organization")


  def test_slug_doesnt_repeat(self):
    """ Assert that slug does not repeat """
    organization = Organization(name="test organization", details="abc", owner=self.user, type=0)
    organization.save()
    self.assertTrue(organization.slug == "test-organization-1")


  def test_slug_is_not_generated_without_name(self):
    """ Assert that slug is not generated without name """
    organization = Organization()
    self.assertTrue(organization.generate_slug() == None)
