# Generated by Django 2.0.6 on 2018-07-03 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=20, verbose_name='댓글 라벨'),
        ),
    ]
