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
            name='Complain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='문의 내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='문의한 시간')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='profiles.Profile', verbose_name='문의를 작성한 유저')),
            ],
            options={
                'verbose_name': '문의',
                'verbose_name_plural': '문의들',
                'db_table': 'complains',
            },
        ),
    ]