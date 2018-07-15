import uuid
from django.db import models, transaction
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from apps.profiles.models import ProfileManager


class UserManager(BaseUserManager):
    @transaction.atomic
    def _create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('이메일은 필수 항목입니다')

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
            raise ValueError('비밀번호는 필수입니다.')

        instance.password = new_password
        instance.set_password(new_password)
        instance.save()
        return instance

    @transaction.atomic
    def deactivate_user(self, user):
        if user.is_active:
            user.is_active = False
            user.profile.is_active = False
            user.profile.is_receiving_notification = False
            user.save()
            user.profile.save()

    @transaction.atomic
    def reactivate_user(self, user):
        if not user.is_active:
            user.is_active = True
            user.profile.is_active = True
            user.profile.is_receiving_notification = True
            user.save()
            user.profile.save()


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

    def __str__(self):
        return '{} : {}'.format(self.username, self.email)

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_active

    def has_module_perms(self, app_label):
        return self.is_active
