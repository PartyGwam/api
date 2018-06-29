from django.db import models, transaction
from django.utils import timezone


class PartyManager(models.Manager):
    @transaction.atomic
    def create(self, owner, **kwargs):
        if not owner:
            raise ValueError('파티 주최자가 있어야 합니다.')

        today = timezone.now()
        date_difference = (kwargs['start_time'] - today).days
        if date_difference < 0:
            raise ValueError('현재 시각 이전에 시작하는 파티를 주최할 수 없습니다.')
        elif date_difference == 0:
            kwargs['will_start_soon'] = True

        if kwargs['max_people'] < 2:
            raise ValueError('참여 가능 인원은 2명 이상이어야 합니다.')

        instance = self.model(
            party_owner=owner,
            **kwargs
        )
        instance.save()

        instance.participants.add(owner)
        instance.save()

        return instance


class Party(models.Model):
    title = models.CharField(max_length=25, verbose_name='파티 제목')
    party_owner = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.PROTECT,
        editable=False,
        related_name='owner',
        verbose_name='파티 주최자'
    )
    place = models.CharField(max_length=25, verbose_name='파티 장소')
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='파티 설명'
    )
    participants = models.ManyToManyField(
        'profiles.Profile',
        limit_choices_to={'is_active', True},
        related_name='participants',
        db_table='participants',
        verbose_name='파티 참가자'
    )
    start_time = models.DateTimeField(verbose_name='파티 시작 시간')
    current_people = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='현재 참여 인원'
    )
    max_people = models.PositiveSmallIntegerField(verbose_name='최대 참여 가능 인원')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성된 시간')
    last_updated = models.DateTimeField(auto_now=True, verbose_name='마지막으로 수정된 시간')

    is_new = models.BooleanField(default=True, verbose_name='최근 개설된 파티인지 여부')
    will_start_soon = models.BooleanField(default=False, verbose_name='곧 시작하는 파티인지 여부')
    has_started = models.BooleanField(default=False, verbose_name='이미 시작된 파티인지 여부')
    can_join = models.BooleanField(default=True, verbose_name='참여 가능한지 여부')

    objects = PartyManager()

    class Meta:
        db_table = 'parties'
        verbose_name = '파티'
        verbose_name_plural = '파티들'

    def __str__(self):
        return '{} 이(가) 주최한 {}'.format(self.party_owner, self.title)
