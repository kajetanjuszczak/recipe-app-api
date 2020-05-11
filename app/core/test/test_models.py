from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test@test.test'
        password = 'Test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_domain_is_case_insensitive(self):
        email = "user@DOMAIN.COM"
        user = get_user_model().objects.create_user(email, "Test123")
        self.assertEqual(user.email, email.lower())
