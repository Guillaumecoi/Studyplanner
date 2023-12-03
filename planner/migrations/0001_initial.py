# Generated by Django 4.2.7 on 2023-12-03 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('order', models.IntegerField(default=0)),
                ('content', models.TextField()),
                ('guessed_time', models.IntegerField(default=0)),
                ('time_spent', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('instructor', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('study_points', models.IntegerField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('order', models.IntegerField(default=0)),
                ('time_spent', models.IntegerField(default=0)),
                ('time_estimated', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planner.document')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('completed', models.BooleanField(default=False)),
                ('chapters', models.ManyToManyField(to='planner.chapter')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planner.document')),
                ('tasks', models.ManyToManyField(to='planner.task')),
            ],
        ),
        migrations.CreateModel(
            name='Deadline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('completed', models.BooleanField(default=False)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planner.document')),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planner.document'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='parent_chapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planner.chapter'),
        ),
    ]
