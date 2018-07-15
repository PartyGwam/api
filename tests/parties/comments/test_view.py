import datetime
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from api.parties.comments.views import CommentAPIViewSet
from apps.comments.models import Comment
from apps.parties.models import Party
from apps.users.models import User


class CommentAPIViewTest(TestCase):
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

        for i in range(4):
            for j in range(i + 1):
                Comment.objects.create_comment(
                    party=self.parties[i],
                    author=self.users[i].profile,
                    text='댓글 내용 {}'.format(j + 1)
                )

        self.factory = APIRequestFactory()
        self.view = CommentAPIViewSet.as_view({'get': 'list', 'post': 'create'})

    def _get_request_path(self, party_slug):
        path = '/api/parties/{}/comments/'.format(party_slug)
        return path

    def test_get_all_comments(self):
        for i in range(4):
            path = self._get_request_path(self.parties[i].slug)
            request = self.factory.get(path)
            force_authenticate(request, self.users[i])
            response = self.view(request)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), i + 1)

    def test_get_all_comments_when_there_is_no_comment(self):
        path = self._get_request_path(self.parties[4].slug)
        request = self.factory.get(path)
        force_authenticate(request, self.users[4])
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_comment(self):
        party = self.parties[4]
        user = self.users[4]
        path = self._get_request_path(party.slug)
        data = {'text': '댓글 내용'}

        request = self.factory.post(path, data, 'json')
        force_authenticate(request, user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_when_not_participating(self):
        party = self.parties[4]
        user = self.users[0]
        path = self._get_request_path(party.slug)
        data = {'text': '댓글 내용'}

        request = self.factory.post(path, data, 'json')
        force_authenticate(request, user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
