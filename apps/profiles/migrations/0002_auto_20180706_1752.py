# Generated by Django 2.0.6 on 2018-07-06 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default=None, null=True, upload_to='assets/images/', verbose_name='프로필 사진'),
        ),
    ]
