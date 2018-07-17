import unittest
from django.test import TestCase

from apps.profiles.models import Profile
from apps.users.models import User


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='sample@gmail.com',
            password='sample_password',
            username='샘플 유저'
        )

    def test_create_profile(self):
        profile = Profile.objects.create_profile(
            user=self.user,
            username=self.user.username
        )
        self.assertIsNotNone(self.user.profile)
        self.assertEqual(self.user.username, self.user.profile.username)
        self.assertEqual(str(profile), '{} 의 프로필'.format(self.user))

    def test_create_profile_without_user(self):
        self.assertRaises(
            ValueError,
            lambda: Profile.objects.create_profile(user=None, username='샘플 유저')
        )

    def test_create_profile_without_username(self):
        self.assertRaises(
            TypeError,
            lambda: Profile.objects.create_profile(self.user)
        )
        self.assertRaises(
            ValueError,
            lambda: Profile.objects.create_profile(self.user, None)
        )

    def test_update_username(self):
        user = User.objects.create_user(
            email='test@gmail.com',
            password='test',
            username='test'
        )
        Profile.objects.update_username(user.profile, 'new_username')
        self.assertEqual(user.username, user.profile.username)
        self.assertEqual(user.username, 'new_username')

    @unittest.skip('Need to mock patch file upload')
    def test_update_profile_picture(self):
        pass
