# Generated by Django 3.0.3 on 2021-01-20 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0007_auto_20210121_0356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='whorespond',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
