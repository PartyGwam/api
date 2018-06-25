import uuid
from django.db import models


class Profile(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='프로필 pk'
    )
    profile_of_user = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        editable=False,
        verbose_name='해당 프로필의 유저'
    )
    profile_picture = models.FileField(
        upload_to='assets/images/',
        null=True,
        verbose_name='프로필 사진',
    )
    is_receiving_notification = models.BooleanField(
        default=True,
        verbose_name='푸시 알림 받는지 여부'
    )

    class Meta:
        db_table = 'profiles'
        verbose_name = '프로필'
        verbose_name_plural = '프로필들'
