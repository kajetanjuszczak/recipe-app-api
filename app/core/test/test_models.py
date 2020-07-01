from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def create_sample_user(email="test@test.com", password='password'):
    return get_user_model().objects.create_user(email, password)


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

    def test_user_registering_with_no_email_throws_error(self):
        email = ""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email, "Test123")

    def test_superuser_is_created_with_is_superuser_and_is_staff_flag(self):
        user = get_user_model().objects.create_superuser(
            "email@outlook.com", "Test123")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_tag_model_has_a_string_representation(self):
        tag = models.Tag.objects.create(
            user=create_sample_user(),
            name='Name',
        )
        self.assertEqual(str(tag), tag.name)
