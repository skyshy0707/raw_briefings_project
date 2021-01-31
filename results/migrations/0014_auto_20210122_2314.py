# Generated by Django 3.0.3 on 2021-01-22 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('results', '0013_auto_20210122_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='results',
            name='whorespond',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
