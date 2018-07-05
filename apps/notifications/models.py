from django.db import models


class NotificationManager(models.Manager):
    def create_notification(self, user, text, **kwargs):
        if not user:
            raise ValueError('유저는 필수입니다.')
        if not text:
            raise ValueError('알림 내용은 필수입니다.')

        instance = self.model(user=user, text=text, **kwargs)
        instance.save()
        return instance


class Notification(models.Model):
    user = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        verbose_name='푸시 알림을 보낼 유저'
    )
    text = models.CharField(max_length=100, verbose_name='알림 내용')
    is_read = models.BooleanField(default=False, verbose_name='읽었는지 여부')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='알림 생성 시간')

    objects = NotificationManager()

    class Meta:
        db_table = 'notifications'
        verbose_name = '알림'
        verbose_name_plural = '알림들'

    def read_notification(self):
        if not self.is_read:
            self.is_read = True
            self.save()
