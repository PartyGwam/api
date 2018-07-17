from django.db import models, transaction
from django.utils import timezone
from django.utils.text import slugify


class PartyManager(models.Manager):
    @transaction.atomic
    def create_party(self, owner, **kwargs):
        if not owner:
            raise ValueError('파티 주최자가 있어야 합니다.')
        if kwargs['max_people'] < 2:
            raise ValueError('참여 가능 인원은 2명 이상이어야 합니다.')

        today = timezone.localtime()
        date_difference = (kwargs['start_time'] - today).days
        if date_difference < 0:
            raise ValueError('현재 시각 이전에 시작하는 파티를 주최할 수 없습니다.')
        elif date_difference == 0:
            kwargs['will_start_soon'] = True

        instance = self.model(
            party_owner=owner,
            slug=self._generate_slug(kwargs['title'], owner.username),
            **kwargs
        )
        instance.save(using=self._db)
        Participant.objects.create(party=instance, profile=owner)

        return instance

    @transaction.atomic
    def update_party(self, instance,
                     title=None, start_time=None,
                     max_people=None, **kwargs):
        if not instance:
            raise ValueError('업데이트 할 모델은 필수입니다.')

        if start_time:
            today = timezone.localtime()
            date_difference = (start_time - today).days
            if date_difference < 0:
                raise ValueError('파티의 시작 시간을 현재 시각보다 빠르게 설정할 수 없습니다.')
            instance.start_time = start_time

        if max_people:
            if max_people < instance.current_people:
                raise ValueError('파티의 최대 인원을 현재 인원보다 작게 설정할 수 없습니다.')
            instance.max_people = max_people
            if max_people == instance.current_people:
                instance.can_join = False

        if 'slug' in kwargs:
            raise ValueError('파티 라벨은 직접 변경 불가하고 제목 변경을 통해서만 가능합니다.')

        if title:
            instance.title = title
            instance.slug = self._generate_slug(title, instance.party_owner.username)

        for attr, value in kwargs.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def _generate_slug(self, title, owner_name):
        slug_string = '{} {} {}'.format(timezone.now(), owner_name, title)
        return slugify(slug_string, allow_unicode=True)

    def pass_party_owner(self, instance, new_owner):
        if new_owner == instance.party_owner:
            raise ValueError('자기 자신에게 위임할 수 없습니다.')
        if new_owner not in instance.participants.all():
            raise ValueError('파티에 참여해 있지 않은 사람에게 위임할 수 없습니다.')

        instance.party_owner = new_owner
        instance.slug = self._generate_slug(instance.title, new_owner.username)
        instance.save()
        return instance


class Participant(models.Model):
    party = models.ForeignKey('Party', on_delete=models.CASCADE)
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)

    class Meta:
        db_table = 'participants'


class Party(models.Model):
    title = models.CharField(max_length=20, verbose_name='파티 제목')
    slug = models.SlugField(
        max_length=100,
        allow_unicode=True,
        verbose_name='파티 라벨'
    )
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
        through=Participant,
        related_name='participants',
        # db_table='participants',
        verbose_name='파티 참가자',
    )
    start_time = models.DateTimeField(verbose_name='파티 시작 시간')
    current_people = models.PositiveSmallIntegerField(default=1, verbose_name='현재 참여 인원')
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

    def update_party_info(self):
        today = timezone.localtime()

        if self.current_people >= self.max_people:
            self.can_join = False
        else:
            self.can_join = True

        if (today - self.created_at).days > 1:
            self.is_new = False

        if (self.start_time - today).days < 0:
            self.will_start_soon = False
            self.has_started = True
            self.can_join = False
        elif (self.start_time - today).days < 1:
            self.will_start_soon = True
        else:
            self.will_start_soon = False
            self.has_started = False

        self.save()

    def add_participants(self, new_participant):
        if new_participant in self.participants.all():
            raise ValueError('이미 파티에 참여하였습니다.')

        current_people = self.current_people
        max_people = self.max_people
        if current_people >= max_people:
            raise ValueError('파티의 정원이 다 차서 참여할 수 없습니다.')

        Participant.objects.create(
            party=self,
            profile=new_participant
        )
        self.current_people += 1
        if current_people == max_people:
            self.can_join = False

        self.save()

    def remove_participants(self, participant):
        if participant == self.party_owner and self.current_people != 1:
            raise ValueError('파티의 주최자는 파티장을 위임한 후에 참여 취소해야 합니다.')

        try:
            participant_object = Participant.objects.filter(profile=participant).get(party=self)
        except Participant.DoesNotExist:
            raise ValueError('파티에 참여하지 않으셨습니다.')

        participant_object.delete()
        self.current_people -= 1
        self.can_join = True
        self.save()
