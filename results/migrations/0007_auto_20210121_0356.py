# Generated by Django 3.0.3 on 2021-01-20 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0006_auto_20210121_0344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='whorespond',
            field=models.IntegerField(blank=True, unique=True),
        ),
    ]
