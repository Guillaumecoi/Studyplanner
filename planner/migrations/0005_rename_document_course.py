# Generated by Django 5.0 on 2023-12-08 12:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0004_document_date_modified'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Document',
            new_name='Course',
        ),
    ]
