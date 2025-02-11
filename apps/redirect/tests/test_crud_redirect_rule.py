import responses
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.test import APIClient, APITestCase

from apps.redirect.models import RedirectRule
from apps.redirect.tests.factories import RedirectRuleFactory, UserFactory


class CRUDRedirectRuleTestCase(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = UserFactory(password="some_password")

        auth_url = reverse("token-create")
        auth_data = {
            "username": self.user.username,
            "password": "some_password",
        }
        response = self.client.post(auth_url, auth_data)
        self.access_token = response.json()["access"]

    @responses.activate
    def test__redirect_rule__create_redirect__success(self):
        url = reverse("create-redirect")
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {
            "redirect_url": "https://google.com",
            "is_private": False,
        }
        with self.assertNumQueries(2):
            response = self.client.post(url, data, headers=headers)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        redirect_identifier = response.json()["redirect_identifier"]
        redirect_rule = RedirectRule.objects.get(redirect_identifier=redirect_identifier)
        self.assertEqual(redirect_rule.redirect_url, "https://google.com")

    @responses.activate
    def test__redirect_rule__create_redirect__wrong_data(self):
        url = reverse("create-redirect")
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {
            "is_private": False,
        }
        with self.assertNumQueries(1):
            response = self.client.post(url, data, headers=headers)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    @responses.activate
    def test__redirect_rule__create_redirect__unauthorized(self):
        url = reverse("create-redirect")
        headers = {"Authorization": "Bearer fake_token"}
        data = {
            "redirect_url": "https://google.com",
            "is_private": False,
        }
        with self.assertNumQueries(0):
            response = self.client.post(url, data, headers=headers)

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    @responses.activate
    def test__redirect_rule__update_redirect__put_redirect_url(self):
        redirect_rule = RedirectRuleFactory(owner=self.user)

        url = reverse("item_redirect", kwargs={"redirect_identifier": redirect_rule.redirect_identifier})
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {
            "redirect_url": "https://google.com",
        }
        with self.assertNumQueries(4):
            response = self.client.put(url, data, headers=headers)

        self.assertEqual(response.status_code, HTTP_200_OK)

        updated_redirect_rule = RedirectRule.objects.get(id=redirect_rule.id)
        self.assertNotEqual(updated_redirect_rule.redirect_url, redirect_rule.redirect_url)
        self.assertEqual(updated_redirect_rule.redirect_url, "https://google.com")
        self.assertEqual(response.json()["redirect_identifier"], redirect_rule.redirect_identifier)

    @responses.activate
    def test__redirect_rule__update_redirect__put_is_private(self):
        redirect_rule = RedirectRuleFactory(owner=self.user, is_private=False)

        url = reverse("item_redirect", kwargs={"redirect_identifier": redirect_rule.redirect_identifier})
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {
            "is_private": True,
        }
        with self.assertNumQueries(4):
            response = self.client.put(url, data, headers=headers)

        self.assertEqual(response.status_code, HTTP_200_OK)

        updated_redirect_rule = RedirectRule.objects.get(id=redirect_rule.id)
        self.assertEqual(updated_redirect_rule.redirect_url, redirect_rule.redirect_url)
        self.assertNotEqual(updated_redirect_rule.is_private, redirect_rule.is_private)
        self.assertEqual(response.json()["redirect_identifier"], redirect_rule.redirect_identifier)

    @responses.activate
    def test__redirect_rule__update_redirect__put_unauthorized(self):
        redirect_rule = RedirectRuleFactory(owner=self.user)

        url = reverse("item_redirect", kwargs={"redirect_identifier": redirect_rule.redirect_identifier})
        headers = {"Authorization": "Bearer fake_token"}
        data = {
            "redirect_url": "https://google.com",
        }
        with self.assertNumQueries(0):
            response = self.client.put(url, data, headers=headers)

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

        updated_redirect_rule = RedirectRule.objects.get(id=redirect_rule.id)
        self.assertEqual(updated_redirect_rule.redirect_url, redirect_rule.redirect_url)
        self.assertEqual(updated_redirect_rule.is_private, redirect_rule.is_private)

    @responses.activate
    def test__redirect_rule__delete_redirect__success(self):
        redirect_rule = RedirectRuleFactory(owner=self.user, is_private=False)

        url = reverse("item_redirect", kwargs={"redirect_identifier": redirect_rule.redirect_identifier})
        headers = {"Authorization": f"Bearer {self.access_token}"}
        with self.assertNumQueries(4):
            response = self.client.delete(url, headers=headers)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        updated_redirect_rule = RedirectRule.objects.filter(id=redirect_rule.id).exists()
        self.assertEqual(updated_redirect_rule, False)

    @responses.activate
    def test__redirect_rule__delete_redirect__unauthorized(self):
        redirect_rule = RedirectRuleFactory(owner=self.user)

        url = reverse("item_redirect", kwargs={"redirect_identifier": redirect_rule.redirect_identifier})
        headers = {"Authorization": "Bearer fake_token"}
        data = {
            "redirect_url": "https://google.com",
        }
        with self.assertNumQueries(0):
            response = self.client.delete(url, data, headers=headers)

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

        updated_redirect_rule = RedirectRule.objects.get(id=redirect_rule.id)
        self.assertEqual(updated_redirect_rule.redirect_url, redirect_rule.redirect_url)
        self.assertEqual(updated_redirect_rule.is_private, redirect_rule.is_private)
