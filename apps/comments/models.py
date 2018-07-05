from django.db import models
from django.utils.text import slugify


class CommentManager(models.Manager):
    def create_comment(self, party, author, **kwargs):
        if not party:
            raise ValueError('파티는 필수입니다.')
        if not author:
            raise ValueError('작성자는 필수입니다.')
        if author not in party.participants.all():
            raise AssertionError('파티에 참여한 사람만 댓글을 작성할 수 있습니다.')

        instance = self.model(party=party, author=author, **kwargs)
        instance.slug = self._generate_slug(kwargs['text'], author.username)
        instance.save(using=self._db)
        return instance

    def update_comment(self, instance, text):
        instance.text = text
        instance.slug = self._generate_slug(text, instance.author.username)
        instance.save()
        return instance

    def _generate_slug(self, text, author):
        return slugify(
            '{} {}'.format(author, text)[:20],
            allow_unicode=True
        )


class Comment(models.Model):
    party = models.ForeignKey(
        'parties.Party',
        on_delete=models.PROTECT,
        verbose_name='댓글이 향하는 파티'
    )
    author = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.PROTECT,
        verbose_name='댓글 작성자'
    )
    text = models.CharField(max_length=150, verbose_name='댓글 내용')
    slug = models.SlugField(
        max_length=20,
        allow_unicode=True,
        verbose_name='댓글 라벨'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='최초 작성된 시간')
    last_updated = models.DateTimeField(
        auto_now=True, verbose_name='가장 최근 수정된 시간')
    is_active = models.BooleanField(default=True, verbose_name='활성화 여부')

    objects = CommentManager()

    class Meta:
        db_table = 'comments'
        verbose_name = '댓글'
        verbose_name_plural = '댓글들'

    def __str__(self):
        return '{} 에 {} 이 남긴 댓글: {}'.format(self.party, self.author, self.text)
