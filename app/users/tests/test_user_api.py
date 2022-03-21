from turtle import st
from venv import create
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:auth')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """ Test the User API """

    def setUp(self) -> None:
        self.client = APIClient()
        return super().setUp()

    def test_create_user_success(self):
        """ Test user creation successful """
        payload = {
            'email': 'test@test.com',
            'password': 'somepassword',
            'name': 'user1'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_exists(self):
        """ Test user creation fails if it already exists"""
        payload = {
            'email': 'test@test.com',
            'password': 'somepassword',
            'name': 'user1'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_password_too_short(self):
        """ Test that password must be more than 10 chars """
        payload = {
            'email': 'test@test.com',
            'password': 'pw',
            'name': 'user1'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email'])
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ Tests that a token is generated for a user """
        payload = {
            'email': 'test@test.com',
            'password': 'somepassword'
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials(self):
        """ Tests that token creation fails if invalid credentials given """
        create_user(email='test@test.com', password= 'somepassword')
        payload = {
            'email': 'test@test.com',
            'password': 'wrongpassword'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_no_token_if_user_invalid(self):
        """ Tests that no token is generated if user does not exist """

        payload = {
            'email': 'test@aaaa.com',
            'password': 'password'
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_fails_if_blank_password(self):
        """ Tests that email and password are required """
        res = self.client.post(TOKEN_URL, {'email': 'aaa@aaa.com', 'password': ''})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)