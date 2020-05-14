from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class TestAdmin(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="test@test.com",
            password="password123",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test2@test.com",
            password="password123",
            name="TestUser"
        )

    def test_users_are_listed_in_django_admin(self):
        url = reverse("admin:core_user_changelist")
        resp = self.client.get(url)

        self.assertContains(resp, self.user.name)
        self.assertContains(resp, self.user.email)

    def test_user_page_change_in_admin(self):
        url = reverse("admin:core_user_change", args=[self.user.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_user_add_page_in_admin(self):
        url = reverse("admin:core_user_add")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
