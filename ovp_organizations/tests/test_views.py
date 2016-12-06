from django.test import TestCase

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp_users.models import User
from ovp_organizations.models import Organization

import copy

base_organization = {"name": "test organization", "slug": "test-override-slug", "description": "test description", "details": "test details", "type": 0, "address": {"typed_address": "r. tecainda, 81, sao paulo"}}

class OrganizationResourceViewSetTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()

  def test_cant_create_organization_unauthenticated(self):
    """Assert that it's not possible to create an organization while unauthenticated"""
    response = self.client.post(reverse("organization-list"), {}, format="json")

    self.assertTrue(response.data["detail"] == "Authentication credentials were not provided.")
    self.assertTrue(response.status_code == 401)

  def test_can_create_organization(self):
    """Assert that it's possible to create a organization while authenticated"""
    user = User.objects.create_user(email="test_can_create_organization@gmail.com", password="testcancreate")
    data = copy.copy(base_organization)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(reverse("organization-list"), data, format="json")

    self.assertTrue(response.data["id"])
    self.assertTrue(response.data["name"] == data["name"])
    self.assertTrue(response.data["slug"] == "test-organization")
    self.assertTrue(response.data["details"] == data["details"])
    self.assertTrue(response.data["description"] == data["description"])

    organization = Organization.objects.get(pk=response.data["id"])
    self.assertTrue(organization.owner.id == user.id)
    self.assertTrue(organization.address.typed_address == data["address"]["typed_address"])

  def test_cant_create_organization_empty_name(self):
    """Assert that it's not possible to create a organization with empty name"""
    user = User.objects.create_user(email="test_can_create_organization@gmail.com", password="testcancreate")

    client = APIClient()
    client.force_authenticate(user=user)

    data = copy.copy(base_organization)
    data["name"] = ""

    response = client.post(reverse("organization-list"), data, format="json")
    self.assertTrue(response.data["name"][0] == "This field may not be blank.")


  def test_organization_retrieval(self):
    """Assert organizations can be retrieved"""
    user = User.objects.create_user(email="test_retrieval@gmail.com", password="testretrieval")

    client = APIClient()
    client.force_authenticate(user=user)

    data = copy.copy(base_organization)
    response = client.post(reverse("organization-list"), data, format="json")

    response = client.get(reverse("organization-detail", ["test-organization"]), format="json")

    self.assertTrue(response.data["name"] == data["name"])
    self.assertTrue(response.data["slug"] == "test-organization")
    self.assertTrue(response.data["details"] == data["details"])
    self.assertTrue(response.data["description"] == data["description"])
