from django.db import models


class Notification(models.Model):
    user = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        verbose_name='푸시 알림을 보낼 유저'
    )
    text = models.CharField(max_length=100, verbose_name='알림 내용')
    is_read = models.BooleanField(default=False, verbose_name='읽었는지 여부')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='알림 생성 시간')

    class Meta:
        db_table = 'notifications'
        verbose_name = '알림'
        verbose_name_plural = '알림들'
