from django.db import models


class Complain(models.Model):
    author = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.PROTECT,
        verbose_name='문의를 작성한 유저'
    )
    text = models.TextField(verbose_name='문의 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='문의한 시간')

    class Meta:
        db_table = 'complains'
        verbose_name = '문의'
        verbose_name_plural = '문의들'
