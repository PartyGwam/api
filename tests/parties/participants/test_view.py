import datetime
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from api.parties.participants.views import ParticipantsAPIView
from apps.parties.models import Party
from apps.users.models import User


class ParticipantAPIViewTest(TestCase):
    def setUp(self):
        self.today = timezone.now()

        self.users = [
            User.objects.create_user(
                email='sample{}@gmail.com'.format(i + 1),
                password='sample_password{}'.format(i + 1),
                username='샘플 유저 {}'.format(i + 1)
            )
            for i in range(6)
        ]
        self.parties = [
            Party.objects.create_party(
                owner=self.users[i].profile,
                title='파티 제목 {}'.format(i + 1),
                place='파티 장소 {}'.format(i + 1),
                start_time=self.today + datetime.timedelta(days=(i + 1) * 10),
                max_people=(i + 2),
            )
            for i in range(5)
        ]

        for i in range(1, 5):
            for j in range(i):
                self.parties[i].add_participants(self.users[j].profile)

        self.factory = APIRequestFactory()
        self.view = ParticipantsAPIView.as_view()

    def _get_request_path(self, party_slug):
        return '/api/parties/{}/participants'.format(party_slug)

    def test_get_participants(self):
        for i in range(5):
            slug = self.parties[i].slug
            path = self._get_request_path(slug)

            request = self.factory.get(path)
            force_authenticate(request, self.users[i])
            response = self.view(request, party_slug=slug)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data['participants']), i + 1)

    def test_participate(self):
        slug = self.parties[0].slug
        path = self._get_request_path(slug)

        request = self.factory.post(path)
        force_authenticate(request, self.users[1])
        response = self.view(request, party_slug=slug)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_participate_when_full(self):
        self.parties[0].add_participants(self.users[1].profile)

        slug = self.parties[0].slug
        path = self._get_request_path(slug)

        request = self.factory.post(path)
        force_authenticate(request, self.users[2])
        response = self.view(request, party_slug=slug)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_participate_again(self):
        slug = self.parties[0].slug
        path = self._get_request_path(slug)

        request = self.factory.post(path)
        force_authenticate(request, self.users[0])
        response = self.view(request, party_slug=slug)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_participate(self):
        slug = self.parties[0].slug
        path = self._get_request_path(slug)

        request = self.factory.delete(path)
        force_authenticate(request, self.users[0])
        response = self.view(request, party_slug=slug)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cancel_participate_when_party_owner(self):
        slug = self.parties[1].slug
        path = self._get_request_path(slug)

        request = self.factory.delete(path)
        force_authenticate(request, self.users[1])
        response = self.view(request, party_slug=slug)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_participate_when_not_participating(self):
        slug = self.parties[0].slug
        path = self._get_request_path(slug)

        request = self.factory.delete(path)
        force_authenticate(request, self.users[1])
        response = self.view(request, party_slug=slug)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
