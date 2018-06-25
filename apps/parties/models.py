from django.db import models


class Party(models.Model):
    title = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        verbose_name='파티 제목'
    )
    party_owner = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.PROTECT,
        editable=False,
        verbose_name='파티 주최자'
    )
    place = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        verbose_name='파티 장소'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='파티 설명'
    )
    start_time = models.DateTimeField(null=False, verbose_name='파티 시작 시간')
    current_people = models.PositiveSmallIntegerField(verbose_name='현재 참여 인원')
    max_people = models.PositiveSmallIntegerField(verbose_name='최대 참여 가능 인원')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성된 시간')
    last_updated = models.DateTimeField(auto_now=True, verbose_name='마지막으로 수정된 시간')

    is_new = models.BooleanField(default=True, verbose_name='최근 개설된 파티인지 여부')
    will_start_soon = models.BooleanField(default=False, verbose_name='곧 시작하는 파티인지 여부')
    has_started = models.BooleanField(default=False, verbose_name='이미 시작된 파티인지 여부')
    can_join = models.BooleanField(default=True, verbose_name='참여 가능한지 여부')

    class Meta:
        db_table = 'parties'
        verbose_name = '파티'
        verbose_name_plural = '파티들'
