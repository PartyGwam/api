import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    pass


class User(AbstractBaseUser):
    uuid = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='유저 pk'
    )
    email = models.EmailField(unique=True, verbose_name='이메일')
    username = models.CharField(
        max_length=8,
        unique=True,
        verbose_name='닉네임'
    )
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일')
    last_logged_in = models.DateTimeField(auto_now=True, verbose_name='마지막 로그인 날짜')
    is_active = models.BooleanField(default=True, verbose_name='활성화 여부')
    is_admin = models.BooleanField(default=False, verbose_name='관리자 여부')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    # objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = '유저'
        verbose_name_plural = '유저들'

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
