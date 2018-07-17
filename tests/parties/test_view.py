import datetime
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from api.parties.views import \
    CreatedPartyAPIView, JoinedPartyAPIView, PartyAPIViewSet
from apps.parties.models import Party
from apps.users.models import User


class PartyAPIViewTest(TestCase):
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
                max_people=(i + 1) * 4,
            )
            for i in range(5)
        ]
        self.party_data = {
            'title': '새로운 파티',
            'place': '새로운 장소',
            'max_people': 6,
            'description': '새로운 설명',
        }

        self.factory = APIRequestFactory()
        self.party_view = PartyAPIViewSet.as_view({'post': 'create', 'put': 'update'})
        self.created_view = CreatedPartyAPIView.as_view()
        self.joined_view = JoinedPartyAPIView.as_view()

        self.party_path = '/api/parties/'
        self.party_created_path = '/api/parties/created/'
        self.party_joined_path = '/api/parties/joined/'

    def test_create_party_successful(self):
        data = self.party_data.copy()
        data['start_time'] = self.today + datetime.timedelta(days=30)

        request = self.factory.post(self.party_path, data, 'json')
        force_authenticate(request, self.users[0])
        response = self.party_view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_party_failure(self):
        data = self.party_data.copy()
        data['start_time'] = self.today - datetime.timedelta(hours=1)

        request = self.factory.post(self.party_path, data, 'json')
        force_authenticate(request, self.users[0])
        response = self.party_view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_party(self):
        update_data = {
            'title': '바뀐 파티',
            'place': '바뀐 장소',
            'description': '바뀐 설명',
        }

        request = self.factory.put(self.party_path, update_data, 'json')
        force_authenticate(request, self.users[0])
        response = self.party_view(request, slug=self.parties[0].slug)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
