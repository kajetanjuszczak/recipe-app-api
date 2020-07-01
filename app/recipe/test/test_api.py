from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Tag

from recipe.serializers import TagSerializer

TAG_URL = reverse('recipe:tag-list')


class PublicRecipeAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_tags_endpoint_returns_405_when_user_is_unauthorized(self):
        response = self.client.get(TAG_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            email='test@test.com',
            password='password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_user_retrieve_tags_assigned_for_it(self):
        Tag.objects.create(user=self.user, name='Tag2')
        Tag.objects.create(user=self.user, name='Tag1')

        response = self.client.get(TAG_URL)

        tags = Tag.objects.all()

        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_user_specific_tags_are_only_ones_returned(self):
        user2 = get_user_model().objects.create(
            email='test2@test.com',
            password='password123'
        )

        user_tag = Tag.objects.create(user=self.user, name='Tag')
        Tag.objects.create(user=user2, name='Tag2')

        response = self.client.get(TAG_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], user_tag.name)
