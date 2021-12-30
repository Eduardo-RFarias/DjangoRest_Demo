from rest_framework.test import APITestCase
from ..models import User


class BaseAuthenticatedTest(APITestCase):
    def login_and_set(self, email, password):
        self.get_user_or_create(email, password)

        loginResponse = self.login(email, password)

        user = loginResponse.data.get("user")
        token = loginResponse.data.get("token")

        self.set_token(token)

        return {"user": user, "token": token}

    def set_token(self, token):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    def get_user_or_create(self, email, password):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return User.objects.create_superuser(
                email=email,
                full_name="example",
                password=password,
            )

    def login(self, email, password):
        return self.client.post("/auth/login/", {"email": email, "password": password})
