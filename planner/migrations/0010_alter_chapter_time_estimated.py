# Generated by Django 5.0 on 2023-12-12 00:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0009_alter_chapter_time_estimated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='time_estimated',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]