import unittest
from django.test import TestCase

from apps.users.models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.email = 'test@gmail.com'
        self.username = '테스트 닉네임'
        self.password = 'test_password'

    def test_create_user(self):
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            username=self.username
        )
        self.assertFalse(user.is_admin)
        self.assertEqual(user.profile.username, self.username)

    def test_create_user_without_email(self):
        self.assertRaises(ValueError, lambda: User.objects.create_user(email=None, password=self.password))
        self.assertRaises(TypeError, lambda: User.objects.create_user(password=self.password))

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email=self.email,
            password=self.password,
            username=self.username
        )
        self.assertTrue(user.is_admin)
        self.assertEqual(user.profile.username, self.username)

    @unittest.skip('Test not fully implemented')
    def test_update_password(self):
        pass

    @unittest.skip('Test not fully implemented')
    def test_update_password_without_password(self):
        pass

    def test_deactivate_user(self):
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            username=self.username
        )
        User.objects.deactivate_user(user)
        self.assertFalse(user.is_active)
        self.assertFalse(user.profile.is_active)
        self.assertFalse(user.profile.is_receiving_notification)

    def test_reactivate_user(self):
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            username=self.username
        )
        User.objects.deactivate_user(user)
        User.objects.reactivate_user(user)
        self.assertTrue(user.is_active)
        self.assertTrue(user.profile.is_active)
        self.assertTrue(user.profile.is_receiving_notification)
