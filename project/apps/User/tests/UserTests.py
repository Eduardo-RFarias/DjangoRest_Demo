from django.contrib.auth.hashers import check_password
from rest_framework import status

from ..models import User
from . import BaseAuthenticatedTest

email = "test@example.com"
full_name = "John Doe"
password = "123456"


class UserTests(BaseAuthenticatedTest):
    def setUp(self):
        self.login_response = self.login_and_set("admin@example.com", password)
        self.id = self.login_response.get("user").get("id")

    def test_user_model(self):
        user = User.objects.create_user(
            email=email,
            full_name=full_name,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.full_name, full_name)
        self.assertTrue(check_password(password, user.password))

        user.delete()

        superuser = User.objects.create_superuser(
            email=email,
            full_name=full_name,
            password=password,
        )

        self.assertEqual(superuser.email, email)
        self.assertEqual(superuser.full_name, full_name)
        self.assertTrue(check_password(password, superuser.password))

        superuser.delete()

    def test_user_list(self):
        response = self.client.get("/auth/user/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data[0].get("url"))

    def test_user_detail(self):
        response = self.client.get(f"/auth/user/{self.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("url"))

    def test_user_create(self):
        new_email = "test2@example.com"

        response = self.client.post(
            "/auth/user/",
            {
                "email": new_email,
                "full_name": full_name,
                "password": password,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get("url"))
        self.assertTrue(response.data.get("email"), new_email)

    def test_user_update(self):
        new_name = "Teste de edi????o"

        user = self.login_response.get("user")
        user["full_name"] = new_name

        response = self.client.put(f"/auth/user/{self.id}/", user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("full_name"), new_name)

    def test_user_delete(self):
        response = self.client.delete(f"/auth/user/{self.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data.get("is_active"))
