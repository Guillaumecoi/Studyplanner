# Generated by Django 5.0 on 2023-12-08 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0005_rename_document_course'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='document',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='deadline',
            old_name='document',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='milestone',
            old_name='document',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='document',
            new_name='course',
        ),
    ]