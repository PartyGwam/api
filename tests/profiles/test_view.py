from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from api.profiles.views import ProfileAPIViewSet
from apps.users.models import User


class ProfileAPIViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='sample@gmail.com',
            password='sample_password',
            username='샘플 유저'
        )
        self.factory = APIRequestFactory()
        self.path = '/api/profiles/'
        self.view = ProfileAPIViewSet.as_view({'get': 'retrieve', 'post': 'create'})

    def test_create_with_username(self):
        data = {'username': '바뀐 유저'}
        request = self.factory.post(self.path, data, 'json')
        force_authenticate(request, self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.username, '바뀐 유저')
        self.assertEqual(self.user.username, self.user.profile.username)

    def test_create_with_profile_picture(self):
        data = {
            'username': '바뀐 유저',
            'profile-picture': 'picture.png'
        }
        request = self.factory.post(self.path, data, 'multipart')
        force_authenticate(request, self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_without_anything(self):
        request = self.factory.post(self.path, None, 'json')
        force_authenticate(request, self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_without_permission(self):
        another_user = User.objects.create_user(
            email='another@gmail.com',
            password='another_password',
            username='다른 유저'
        )
        request = self.factory.get(self.path)
        force_authenticate(request, another_user)
        response = self.view(request, username='샘플 유저')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
