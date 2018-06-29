import uuid
from django.conf import settings
from django.db import models


class ProfileManager(models.Manager):
    def create_profile(self, user, username, **kwargs):
        if not user:
            raise ValueError('프로필은 user 가 있는 상태에서만 생성 가능합니다.')
        if not username:
            raise ValueError('닉네임은 필수입니다.')

        profile = Profile(
            user=user,
            username=username,
            **kwargs
        )

        profile.save(using=self._db)
        return profile


class Profile(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='프로필 pk'
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name='해당 프로필의 유저'
    )
    username = models.CharField(
        max_length=8,
        unique=True,
        verbose_name='닉네임'
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
    is_active = models.BooleanField(default=True, verbose_name='활성화 여부')

    objects = ProfileManager()

    class Meta:
        db_table = 'profiles'
        verbose_name = '프로필'
        verbose_name_plural = '프로필들'

    def __str__(self):
        return '{} 의 프로필'.format(self.user)
