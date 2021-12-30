from django.test import RequestFactory
from rest_framework import status

from ..serializers import UserSerializer
from . import BaseAuthenticatedTest

email = "test@example.com"
password = "123456"


class AuthTests(BaseAuthenticatedTest):
    def test_login_view(self):
        user = self.get_user_or_create(email, password)

        request = RequestFactory().post("/")
        userJson = UserSerializer(user, context={"request": request}).data

        response = self.login(email, password)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsNotNone(response.data.get("expiry"))
        self.assertIsNotNone(response.data.get("token"))
        self.assertIsNotNone(response.data.get("user"))

        authenticated_user = response.data.get("user")

        self.assertEqual(authenticated_user.get("url"), userJson.get("url"))
        self.assertEqual(authenticated_user.get("email"), userJson.get("email"))

    def test_logout_view(self):
        self.login_and_set(email, password)

        response = self.client.post("/auth/logout/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        unauthorized_response = self.client.get("/auth/user/")

        self.assertEqual(
            unauthorized_response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_user_view_authentication(self):
        response = self.client.get("/auth/user/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
