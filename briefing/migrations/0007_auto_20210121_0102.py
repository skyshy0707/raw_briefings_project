# Generated by Django 3.0.3 on 2021-01-20 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('briefing', '0006_auto_20210108_0546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='briefing',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='briefing',
            name='who_respond',
        ),
    ]
