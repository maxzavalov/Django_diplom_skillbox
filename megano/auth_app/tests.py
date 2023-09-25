import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from string import ascii_letters
from random import choices
from .models import Profile


class AuthTestCase(APITestCase):

    def setUp(self) -> None:
        self.name = ''.join(choices(ascii_letters, k=8))
        self.username = ''.join(choices(ascii_letters, k=10))
        self.password = ''.join(choices(ascii_letters, k=12))

    def test_login(self):
        User.objects.create_user(username=self.username, password=self.password)
        url = reverse("auth_app:login")
        data = {"username": self.username, "password": self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crete_account(self):
        User.objects.filter(username=self.username).delete()
        url = reverse("auth_app:register")
        data = {
            "name": self.name,
            "username": self.username,
            "password": self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username=self.username).exists())

    def test_crete_profile(self):
        User.objects.filter(username=self.username).delete()
        url = reverse("auth_app:register")
        data = {
            "name": self.name,
            "username": self.username,
            "password": self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Profile.objects.filter(fullName=self.name).exists())


class ProfileTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="exampleUser", password="querty123")
        self.fullName = ''.join(choices(ascii_letters, k=8))
        self.phone = 467321886
        self.email = "testCase@example.com"

    def test_get_method(self):
        Profile.objects.create(
            user=self.user,
            fullName=self.fullName,
            email=self.email,
            phone=self.phone,
            avatar="avatars/default.png"
        )
        url = reverse("auth_app:profile")
        expected_data = {
                  "fullName": self.fullName,
                  "email": self.email,
                  "phone": self.phone,
                  "avatar": {
                    "src": "media/avatars/default.png",
                    "alt": "Image alt string"
                  }
                }
        self.client.force_login(user=self.user)

        response = self.client.get(url)
        received_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(received_data, expected_data)