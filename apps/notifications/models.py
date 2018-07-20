from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class NotificationManager(models.Manager):
    def create_notification(self, party, user, title, **kwargs):
        if not party:
            raise ValueError('연관된 파티는 필수입니다.')
        if not user:
            raise ValueError('유저는 필수입니다.')
        if not title:
            raise ValueError('알림 제목은 필수입니다.')

        instance = self.model(
            slug=self._generate_notification_slug(title),
            party=party,
            user=user,
            title=title,
            **kwargs
        )
        instance.save()
        return instance

    @staticmethod
    def _generate_notification_slug(notification_title):
        now = timezone.now()
        return slugify(
            '{}-{}'.format(now, notification_title),
            allow_unicode=True
        )


class Notification(models.Model):
    slug = models.SlugField(
        max_length=100,
        allow_unicode=True,
        unique=True,
        editable=False,
        verbose_name='알림 라벨'
    )
    user = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        verbose_name='푸시 알림을 보낼 유저'
    )
    party = models.ForeignKey(
        'parties.Party',
        on_delete=models.CASCADE,
        verbose_name='알림과 연관된 파티'
    )
    title = models.CharField(max_length=30, verbose_name='알림 제목')
    body = models.CharField(
        max_length=100,
        null=True,
        verbose_name='알림 내용'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='알림 생성 시간'
    )

    objects = NotificationManager()

    class Meta:
        db_table = 'notifications'
        verbose_name = '알림'
        verbose_name_plural = '알림들'

    def read_notification(self):
        if not self.is_read:
            self.is_read = True
            self.save()
