# Generated by Django 2.0.6 on 2018-07-02 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='slug',
        ),
    ]
