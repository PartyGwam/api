# Generated by Django 2.0.6 on 2018-06-24 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100, verbose_name='알림 내용')),
                ('is_read', models.BooleanField(default=False, verbose_name='읽었는지 여부')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='알림 생성 시간')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile', verbose_name='푸시 알림을 보낼 유저')),
            ],
            options={
                'verbose_name': '알림',
                'verbose_name_plural': '알림들',
                'db_table': 'notifications',
            },
        ),
    ]