# Generated by Django 3.0.3 on 2021-01-07 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20210107_1938'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usualuser',
            options={'permissions': [('briefing.find_briefing', 'can find any briefing'), ('briefing.answer_briefing', 'can answer on any briefing')]},
        ),
    ]
