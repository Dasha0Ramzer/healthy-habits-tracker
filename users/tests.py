from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework.test import APIClient

from .models import User


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@example.com", password=make_password("StrongPass123")
        )

    def test_register(self):
        response = self.client.post(
            "/users/register/",
            {"email": "new@example.com", "password": "StrongPass123"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(email="new@example.com")
        self.assertNotEqual(user.password, "StrongPass123")  # пароль захеширован

    def test_register_duplicate_email(self):
        response = self.client.post(
            "/users/register/",
            {"email": "test@example.com", "password": "StrongPass123"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        response = self.client.post(
            "/users/login/",
            {"email": "test@example.com", "password": "StrongPass123"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_habits_without_token(self):
        response = self.client.get("/habits/")
        self.assertEqual(response.status_code, 401)
