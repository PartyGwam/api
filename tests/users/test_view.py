import unittest
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from api.users.views import LoginAPIView, UserAPIViewset
from apps.users.models import User


class BaseUserAPIViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@gmail.com',
            password='test_password',
            username='테스트 유저'
        )
        self.factory = APIRequestFactory()
        self.LOGIN_URL = '/api/users/login/'
        self.USER_URL = '/api/users/'


class LoginAPIViewTest(BaseUserAPIViewTest):
    def setUp(self):
        super(LoginAPIViewTest, self).setUp()
        self.view = LoginAPIView.as_view()

    def _send_login_request(self, email, password):
        data = {'email': email, 'password': password}
        request = self.factory.post(self.LOGIN_URL, data, format='json')
        response = self.view(request)
        return response

    def test_login_successful(self):
        response = self._send_login_request('test@gmail.com', 'test_password')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.user.username)

    def test_login_failure(self):
        response = self._send_login_request('test2@gmail.com', 'test_password')
        self.assertEqual(response.status_code, 400)

    @unittest.skip('Test not fully implemented')
    def test_login_with_deactivated_user(self):
        User.objects.deactivate_user(self.user)
        response = self._send_login_request('test@gmail.com', 'test_password')
        self.assertTrue(self.user.is_active)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.user.username)


class UserAPIViewSetTest(BaseUserAPIViewTest):
    def setUp(self):
        super(UserAPIViewSetTest, self).setUp()
        self.view = UserAPIViewset.as_view({'post': 'create', 'put': 'update'})

    def _send_create_request(self, email, username, password):
        data = {'email': email, 'username': username, 'password': password}
        request = self.factory.post(self.USER_URL, data, format='json')
        response = self.view(request)
        return response

    def _send_update_request(self, new_password):
        data = {'password': new_password}
        url = self.USER_URL + '{}/'.format(self.user.uuid)
        request = self.factory.put(url, data, format='json')
        force_authenticate(request, self.user)
        response = self.view(request, pk=self.user.uuid)
        return response

    def test_create_successful(self):
        response = self._send_create_request(
            'sample@gmail.com',
            '샘플 유저',
            'samplepassword'
        )
        self.assertEqual(response.status_code, 201)
        profile = User.objects.get(email='sample@gmail.com').profile
        self.assertIsNotNone(profile)

    @unittest.skip('Test not fully implemented')
    def test_update_successful(self):
        response = self._send_update_request('new_password')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.user._password, 'new_password')
