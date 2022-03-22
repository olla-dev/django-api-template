from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from recipes.models import Tag
from recipes.serializers import TagSerializer

TAGS_URL = reverse('recipes:tag-list')

class PublicTagApiTests(TestCase):
    """ Test the public Tag API """

    def setUp(self) -> None:
        self.client = APIClient()
        return super().setUp()

    def test_login_required(self):
        """Tests that login is required"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTests(TestCase):
    """ Test the private Tag API """

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="1234567890"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        return super().setUp()

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(
            user=self.user,
            name='Vegan'
        )
        Tag.objects.create(
            user=self.user,
            name='Dessert'
        )

        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_by_user(self):
        """Test that tags are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'some@mail.com',
            'dskjhfksjfksdnfksjd'
        )
        Tag.objects.create(
            user=user2,
            name='Fruit'
        )
        tag = Tag.objects.create(
            user=self.user,
            name='Vegan'
        )

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag(self):
        """Test the creation of a tag"""
        payload = { 'name': 'entrees' }

        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
