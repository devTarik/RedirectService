import responses
from django.urls import reverse
from rest_framework.status import (
    HTTP_302_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIClient, APITestCase

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
    def test__redirect_rule__get_public_redirect__success(self):
        redirect_rule = RedirectRuleFactory(owner=self.user, is_private=False)

        url = reverse("public-redirect-detail", kwargs={"redirect_identifier": redirect_rule.redirect_identifier})
        with self.assertNumQueries(1):
            response = self.client.get(url)

        self.assertEqual(response.status_code, HTTP_302_FOUND)

    @responses.activate
    def test__redirect_rule__get_private_redirect__success(self):
        redirect_rule = RedirectRuleFactory(owner=self.user, is_private=True)

        url = reverse("private-redirect-detail", kwargs={"redirect_identifier": redirect_rule.redirect_identifier})
        headers = {"Authorization": f"Bearer {self.access_token}"}
        with self.assertNumQueries(2):
            response = self.client.get(url, headers=headers)

        self.assertEqual(response.status_code, HTTP_302_FOUND)

    @responses.activate
    def test__redirect_rule__get_private_redirect__different_owner(self):
        second_user = UserFactory(password="some_password")
        redirect_rule = RedirectRuleFactory(owner=second_user, is_private=True)

        url = reverse("private-redirect-detail", kwargs={"redirect_identifier": redirect_rule.redirect_identifier})
        headers = {"Authorization": f"Bearer {self.access_token}"}  # access_token from first user
        with self.assertNumQueries(2):
            response = self.client.get(url, headers=headers)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    @responses.activate
    def test__redirect_rule__get_private_redirect__unauthorized(self):
        redirect_rule = RedirectRuleFactory(owner=self.user, is_private=True)

        url = reverse("private-redirect-detail", kwargs={"redirect_identifier": redirect_rule.redirect_identifier})
        headers = {"Authorization": "Bearer fake_token"}
        with self.assertNumQueries(0):
            response = self.client.get(url, headers=headers)

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
