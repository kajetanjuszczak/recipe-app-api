from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

USER_CREATE_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


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

    def test_token_succesfully_created(self):
        payload = {
            'email': 'email@test.com',
            'password': 'test123!'
        }
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_token_not_created_when_incorect_password(self):
        create_user(email="test@test.com", password='correct')
        payload = {
            'email': 'test@test.com',
            'password': 'incorrect',
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_token_not_created_when_non_existant_user(self):
        response = self.client.post(
            TOKEN_URL,
            {'email': 'test@test.com', 'password': 'correct'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_token_not_created_when_no_password_provided(self):
        response = self.client.post(
            TOKEN_URL,
            {'email': 'test@test.com', 'password': ''}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_me_endpoint_not_accessible_without_token(self):
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUserAPIPrivate(TestCase):

    def setUp(self):
        self.user = create_user(
            email='email@test.com',
            password='test123!',
            name='testname',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_profile_success(self):
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'email': self.user.email, 'name': self.user.name
        })

    def test_post_not_allowed_for_me_endpoint(self):
        response = self.client.post(ME_URL, {})
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_authenticated_user_can_change_user_data(self):
        payload = {
            'name': 'test',
            'password': 'correct'
        }
        response = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
