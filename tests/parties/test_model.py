import datetime
import unittest
from django.test import TestCase
from django.utils import timezone

from apps.parties.models import Party
from apps.users.models import User


class PartyModelTest(TestCase):
    def setUp(self):
        self.today = timezone.now()
        self.user = User.objects.create_user(
            email='sample@gmail.com',
            password='sample_password',
            username='샘플 유저 1'
        )
        self.party = Party.objects.create_party(
            owner=self.user.profile,
            title='파티 제목',
            place='파티 장소',
            description='파티 설명',
            start_time=self.today + datetime.timedelta(days=10),
            max_people=4,
        )

    def test_create_party_with_description_successful(self):
        party = Party.objects.create_party(
            owner=self.user.profile,
            title='새로운 파티 제목',
            place='새로운 파티 장소',
            description='새로운 파티 설명',
            start_time=self.today + datetime.timedelta(days=10),
            max_people=4
        )
        self.assertEqual(str(party), '{} 이(가) 주최한 {}'.format(self.user.profile, '새로운 파티 제목'))
        self.assertIs(party.party_owner, self.user.profile)
        self.assertEqual(party.current_people, 1)
        self.assertTrue('샘플-유저-1-새로운-파티-제목' in party.slug)
        self.assertFalse(party.will_start_soon)
        self.assertTrue(self.user.profile in party.participants.all())

    def test_create_party_without_description_successful(self):
        party = Party.objects.create_party(
            owner=self.user.profile,
            title='새로운 파티 제목',
            place='새로운 파티 장소',
            start_time=self.today + datetime.timedelta(days=10),
            max_people=4
        )
        self.assertIsNone(party.description)

    def test_create_party_which_starts_soon(self):
        party = Party.objects.create_party(
            owner=self.user.profile,
            title='새로운 파티 제목',
            place='새로운 파티 장소',
            start_time=self.today + datetime.timedelta(hours=19),
            max_people=4
        )
        self.assertTrue(party.will_start_soon)

    def test_create_party_without_owner(self):
        self.assertRaises(
            ValueError,
            lambda: Party.objects.create_party(
                owner=None,
                title='새로운 파티 제목',
                place='새로운 파티 장소',
                start_time=self.today + datetime.timedelta(days=10),
                max_people=4
            )
        )
        self.assertRaises(
            TypeError,
            lambda: Party.objects.create_party(
                title='새로운 파티 제목',
                place='새로운 파티 장소',
                start_time=self.today + datetime.timedelta(days=10),
                max_people=4
            )
        )

    def test_create_party_with_insufficient_max_people(self):
        self.assertRaises(
            ValueError,
            lambda: Party.objects.create_party(
                owner=self.user.profile,
                title='새로운 파티 제목',
                place='새로운 파티 장소',
                start_time=self.today + datetime.timedelta(days=10),
                max_people=1
            )
        )

    def test_create_party_with_past_start_time(self):
        self.assertRaises(
            ValueError,
            lambda: Party.objects.create_party(
                owner=self.user.profile,
                title='새로운 파티 제목',
                place='새로운 파티 장소',
                start_time=self.today - datetime.timedelta(days=10),
                max_people=3
            )
        )

    def test_update_party_with_general_information(self):
        party = Party.objects.update_party(
            instance=self.party,
            title='바뀐 제목',
            description='바뀐 설명'
        )
        self.assertTrue('샘플-유저-1-바뀐-제목' in party.slug)
        self.assertEqual(party.description, '바뀐 설명')

    def test_update_party_with_start_time(self):
        party = Party.objects.update_party(
            instance=self.party,
            start_time=self.today + datetime.timedelta(days=15),
        )
        self.assertEqual(party.start_time, self.today + datetime.timedelta(days=15))

    def test_update_party_with_max_people(self):
        party = Party.objects.update_party(
            instance=self.party,
            max_people=10,
        )
        self.assertEqual(party.max_people, 10)

    def test_update_party_with_past_start_time(self):
        self.assertRaises(
            ValueError,
            lambda: Party.objects.update_party(
                instance=self.party,
                start_time=self.today - datetime.timedelta(hours=10),
            )
        )

    def test_update_party_with_insufficient_max_people(self):
        another_user = User.objects.create_user(
            email='another@gmail.com',
            password='another_password',
            username='다른 유저 1'
        )
        self.party.add_participants(another_user.profile)

        self.assertRaises(
            ValueError,
            lambda: Party.objects.update_party(
                instance=self.party,
                max_people=1
            )
        )

    def test_update_party_with_just_right_max_people(self):
        another_user = User.objects.create_user(
            email='another@gmail.com',
            password='another_password',
            username='다른 유저 1'
        )
        self.party.add_participants(another_user.profile)
        Party.objects.update_party(
            instance=self.party,
            max_people=2
        )
        self.assertFalse(self.party.can_join)

    def test_update_party_without_party_instance(self):
        self.assertRaises(
            TypeError,
            lambda: Party.objects.update_party(
                title='바뀐 제목',
                description='바뀐 설명'
            )
        )
        self.assertRaises(
            ValueError,
            lambda: Party.objects.update_party(
                instance=None,
                title='바뀐 제목',
                description='바뀐 설명'
            )
        )

    def test_update_party_with_slug(self):
        self.assertRaises(
            ValueError,
            lambda: Party.objects.update_party(
                instance=self.party,
                slug='이러쿵 저러쿵'
            )
        )

    @unittest.skip('Test not fully implemented')
    def test_update_party_info(self):
        pass

    def test_add_participants(self):
        another_user = User.objects.create_user(
            email='another@gmail.com',
            password='another_password',
            username='다른 유저 1'
        )
        self.party.add_participants(another_user.profile)

        self.assertEqual(self.party.participants.count(), 2)
        self.assertEqual(self.party.current_people, 2)
        self.assertTrue(another_user.profile in self.party.participants.all())

    def test_add_participants_duplicate(self):
        self.assertRaises(
            ValueError,
            lambda: self.party.add_participants(self.user.profile)
        )

    @unittest.skip('Test not implemented')
    def test_add_participants_when_full(self):
        pass

    def test_remove_participants(self):
        another_user = User.objects.create_user(
            email='another@gmail.com',
            password='another_password',
            username='다른 유저 1'
        )
        self.party.add_participants(another_user.profile)
        self.party.remove_participants(another_user.profile)

        self.assertEqual(self.party.participants.count(), 1)
        self.assertEqual(self.party.current_people, 1)
        self.assertTrue(another_user.profile not in self.party.participants.all())

    def test_remove_participant_whom_is_party_owner(self):
        another_user = User.objects.create_user(
            email='another@gmail.com',
            password='another_password',
            username='다른 유저 1'
        )
        self.party.add_participants(another_user.profile)

        self.assertRaises(
            ValueError,
            lambda: self.party.remove_participants(self.user.profile)
        )

    def test_remove_participant_whom_did_not_participate(self):
        another_user = User.objects.create_user(
            email='another@gmail.com',
            password='another_password',
            username='다른 유저 1'
        )
        self.assertRaises(
            ValueError,
            lambda: self.party.remove_participants(another_user.profile)
        )

    def test_pass_party_owner(self):
        another_user = User.objects.create_user(
            email='another@gmail.com',
            password='another_password',
            username='다른 유저 1'
        )
        self.party.add_participants(another_user.profile)
        party = Party.objects.pass_party_owner(self.party, another_user.profile)
        self.assertEqual(party.party_owner, another_user.profile)

    def test_pass_party_owner_to_myself(self):
        self.assertRaises(
            ValueError,
            lambda: Party.objects.pass_party_owner(self.party, self.user.profile)
        )

    def test_pass_party_owner_to_whom_did_not_participate(self):
        another_user = User.objects.create_user(
            email='another@gmail.com',
            password='another_password',
            username='다른 유저 1'
        )
        self.assertRaises(
            ValueError,
            lambda: Party.objects.pass_party_owner(self.party, another_user.profile)
        )
