# Generated by Django 2.0.6 on 2018-07-03 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_remove_notification_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='slug',
            field=models.SlugField(allow_unicode=True, default=None, max_length=20, verbose_name='알림 라벨'),
        ),
    ]