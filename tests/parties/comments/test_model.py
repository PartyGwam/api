import datetime
from django.test import TestCase
from django.utils import timezone

from apps.comments.models import Comment
from apps.parties.models import Party
from apps.users.models import User


class CommentModelTest(TestCase):
    def setUp(self):
        self.users = [
            User.objects.create_user(
                email='sample{}@gmail.com'.format(i + 1),
                password='sample_password{}'.format(i + 1),
                username='샘플 유저 {}'.format(i + 1)
            )
            for i in range(3)
        ]
        self.party = Party.objects.create_party(
            title='파티 제목',
            owner=self.users[0].profile,
            place='파티 장소',
            start_time=datetime.datetime(
                2018, 8, 30, 0, 0,
                tzinfo=timezone.get_current_timezone()
            ),
            max_people=4
        )
        self.party.add_participants(self.users[1].profile)

    def test_create_comment(self):
        comment = Comment.objects.create_comment(
            self.party,
            self.users[1].profile,
            text='댓글'
        )
        self.assertTrue('샘플-유저-2-댓글' in comment.slug)
        self.assertEqual(self.party.comment_set.count(), 1)
        self.assertTrue(comment in self.party.comment_set.all())
        self.assertEqual(
            str(comment),
            '{} 에 {} 이 남긴 댓글: {}'.format(self.party, comment.author, '댓글')
        )

    def test_create_comment_without_party(self):
        self.assertRaises(
            TypeError,
            lambda: Comment.objects.create_comment(
                author=self.users[1].profile,
                text='댓글'
            )
        )
        self.assertRaises(
            ValueError,
            lambda: Comment.objects.create_comment(
                party=None,
                author=self.users[1].profile,
                text='댓글'
            )
        )

    def test_create_comment_without_author(self):
        self.assertRaises(
            TypeError,
            lambda: Comment.objects.create_comment(
                party=self.party,
                text='댓글'
            )
        )
        self.assertRaises(
            ValueError,
            lambda: Comment.objects.create_comment(
                party=self.party,
                author=None,
                text='댓글'
            )
        )

    def test_create_comment_with_author_whom_did_not_participate(self):
        self.assertRaises(
            ValueError,
            lambda: Comment.objects.create_comment(
                self.party,
                self.users[2].profile,
                text='댓글'
            )
        )

    def test_update_comment(self):
        comment = Comment.objects.create_comment(
            self.party,
            self.users[1].profile,
            text='댓글'
        )
        Comment.objects.update_comment(instance=comment, text='바뀐 댓글 내용')

        self.assertEqual(comment.text, '바뀐 댓글 내용')
        self.assertTrue('샘플-유저-2-바뀐-댓글-내용' in comment.slug)
