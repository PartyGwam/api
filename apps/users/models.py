import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('이메일은 필수 항목입니다')

        # TODO 비밀번호 검증 추가

        user = self.model(
            email=self.normalize_email(email),
            password=password,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_admin', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_admin', True)
        return self._create_user(email, password, **kwargs)


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

    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = '유저'
        verbose_name_plural = '유저들'

    def __repr__(self):
        return '{} : {}'.format(self.username, self.email)

    def __str__(self):
        return '{} : {}'.format(self.username, self.email)

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
