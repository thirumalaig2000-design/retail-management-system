from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Role

User = get_user_model()


class AccountModelTests(TestCase):
    def test_seeded_roles_exist(self):
        self.assertTrue(Role.objects.filter(code=Role.Code.USER).exists())
        self.assertTrue(Role.objects.filter(code=Role.Code.ADMIN).exists())
        self.assertTrue(Role.objects.filter(code=Role.Code.SUPER_ADMIN).exists())

    def test_user_can_be_created_with_role(self):
        role = Role.objects.get(code=Role.Code.USER)
        user = User.objects.create_user(
            email="cashier@smartstock.local",
            password="demo-password",
            role=role,
        )
        self.assertEqual(user.email, "cashier@smartstock.local")
        self.assertTrue(user.check_password("demo-password"))


class AuthApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_role = Role.objects.get(code=Role.Code.ADMIN)
        self.user_role = Role.objects.get(code=Role.Code.USER)
        self.super_role = Role.objects.get(code=Role.Code.SUPER_ADMIN)
        self.super_user = User.objects.create_user(
            email="superadmin@smartstock.local",
            password="SmartStock!123",
            role=self.super_role,
            is_staff=True,
            is_superuser=True,
        )
        self.admin_user = User.objects.create_user(
            email="admin@smartstock.local",
            password="SmartStock!123",
            role=self.admin_role,
        )
        self.cashier_user = User.objects.create_user(
            email="cashier@smartstock.local",
            password="SmartStock!123",
            role=self.user_role,
        )

    def test_login_returns_tokens_and_user(self):
        response = self.client.post(
            "/api/auth/login/",
            {"email": "superadmin@smartstock.local", "password": "SmartStock!123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["email"], "superadmin@smartstock.local")

    def test_refresh_token_works(self):
        login = self.client.post(
            "/api/auth/login/",
            {"email": "superadmin@smartstock.local", "password": "SmartStock!123"},
            format="json",
        )
        response = self.client.post(
            "/api/auth/refresh/",
            {"refresh": login.data["refresh"]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_me_endpoint_requires_auth_and_returns_profile(self):
        self.client.force_authenticate(user=self.cashier_user)
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "cashier@smartstock.local")

    def test_user_management_blocks_cashier(self):
        self.client.force_authenticate(user=self.cashier_user)
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_cannot_create_super_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            "/api/users/",
            {
                "email": "new-admin@smartstock.local",
                "first_name": "New",
                "last_name": "Admin",
                "phone": "",
                "password": "SmartStock!123",
                "role_code": Role.Code.SUPER_ADMIN,
                "is_active": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_super_admin_can_list_users(self):
        self.client.force_authenticate(user=self.super_user)
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 3)
