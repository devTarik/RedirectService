import responses
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient, APITestCase

from apps.redirect.tests.factories import UserFactory


class AuthUserTestCase(APITestCase):
    client: APIClient

    @responses.activate
    def test__auth_user__create_token__success(self):
        user = UserFactory(password="some_password")

        url = reverse("token-create")
        data = {
            "username": user.username,
            "password": "some_password",
        }
        with self.assertNumQueries(1):
            response = self.client.post(url, data)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())

    @responses.activate
    def test__auth_user__create_token__fail_password(self):
        user = UserFactory(password="some_password")

        url = reverse("token-create")
        data = {
            "username": user.username,
            "password": "fail_password",
        }
        with self.assertNumQueries(1):
            response = self.client.post(url, data)

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
