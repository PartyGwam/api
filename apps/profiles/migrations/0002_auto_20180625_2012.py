# Generated by Django 2.0.6 on 2018-06-25 11:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='활성화 여부'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_of_user',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='해당 프로필의 유저'),
        ),
    ]
