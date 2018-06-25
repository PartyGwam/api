from django.db import models


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
        max_length=10,
        default=None,  # TODO 자동생성 메소드 추가
        allow_unicode=True,
        verbose_name='댓글 라벨',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='최초 작성된 시간')
    last_updated = models.DateTimeField(auto_now=True, verbose_name='가장 최근 수정된 시간')
    is_active = models.BooleanField(default=True, verbose_name='활성화 여부')

    class Meta:
        db_table = 'comments'
        verbose_name = '댓글'
        verbose_name_plural = '댓글들'
