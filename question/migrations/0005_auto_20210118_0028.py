# Generated by Django 3.0.3 on 2021-01-17 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0004_remove_question_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='date_create',
            field=models.DateField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name='variant_ans',
            name='is_oneVar',
            field=models.BooleanField(),
        ),
    ]