# Generated by Django 2.0.6 on 2018-06-29 03:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, verbose_name='파티 제목')),
                ('place', models.CharField(max_length=25, verbose_name='파티 장소')),
                ('description', models.TextField(
                    blank=True, null=True, verbose_name='파티 설명')),
                ('start_time', models.DateTimeField(verbose_name='파티 시작 시간')),
                ('current_people', models.PositiveSmallIntegerField(
                    default=1, verbose_name='현재 참여 인원')),
                ('max_people', models.PositiveSmallIntegerField(
                    verbose_name='최대 참여 가능 인원')),
                ('created_at', models.DateTimeField(
                    auto_now_add=True, verbose_name='생성된 시간')),
                ('last_updated', models.DateTimeField(
                    auto_now=True, verbose_name='마지막으로 수정된 시간')),
                ('is_new', models.BooleanField(
                    default=True, verbose_name='최근 개설된 파티인지 여부')),
                ('will_start_soon', models.BooleanField(
                    default=False, verbose_name='곧 시작하는 파티인지 여부')),
                ('has_started', models.BooleanField(
                    default=False, verbose_name='이미 시작된 파티인지 여부')),
                ('can_join', models.BooleanField(
                    default=True, verbose_name='참여 가능한지 여부')),
                ('participants', models.ManyToManyField(db_table='participants', limit_choices_to={
                 'is_active', True}, related_name='participants', to='profiles.Profile', verbose_name='파티 참가자')),
                ('party_owner', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT,
                                                  related_name='owner', to='profiles.Profile', verbose_name='파티 주최자')),
            ],
            options={
                'verbose_name': '파티',
                'verbose_name_plural': '파티들',
                'db_table': 'parties',
            },
        ),
    ]
