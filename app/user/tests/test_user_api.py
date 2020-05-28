from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

USER_CREATE_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create(**params)


class TestUserAPI(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_user_is_created_when_required_fields_were_filled(self):
        payload = {
            'email': 'email@test.com',
            'password': 'test123!',
            'name': 'testname',
        }
        response = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_not_created_when_user_with_the_same_email_exists(self):
        payload = {
            'email': 'email@test.com',
            'password': 'test123!',
            'name': 'testname',
        }
        create_user(**payload)
        response = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_too_short_password_will_not_be_created(self):
        payload = {
            'email': 'email@test.com',
            'password': 't1',
            'name': 'testname',
        }
        response = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
