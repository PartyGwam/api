import uuid
from django.db import models, transaction
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from apps.profiles.models import ProfileManager


class UserManager(BaseUserManager):
    @transaction.atomic
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

        self.model.profiles.create_profile(
            user=user,
            username=user.username
        )

        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_admin', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_admin', True)
        return self._create_user(email, password, **kwargs)

    def update_password(self, instance, new_password):
        if not new_password:
            raise ValueError("비밀번호는 필수항목입니다.")

        instance.password = new_password
        instance.set_password(new_password)
        instance.save(using=self._db)
        return instance

    @transaction.atomic
    def deactivate(self, instance):
        if instance.is_active:
            instance.is_active = False
            instance.profile.is_active = False
            instance.save()
            instance.profile.save()

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
    profiles = ProfileManager()

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
