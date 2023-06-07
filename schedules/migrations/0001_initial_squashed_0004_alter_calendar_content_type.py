# Generated by Django 3.2.18 on 2023-06-08 02:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('schedules', '0001_initial'), ('schedules', '0002_auto_20230608_1126'), ('schedules', '0003_alter_calendar_content_type'), ('schedules', '0004_alter_calendar_content_type')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='새 캘린더', max_length=255)),
                ('color', models.CharField(default='', max_length=6)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'accounts'), ('model', 'user')), models.Q(('app_label', 'groups'), ('model', 'group')), _connector='OR'), on_delete=django.db.models.deletion.DO_NOTHING, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('summary', models.CharField(blank=True, default='', max_length=150)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('location', models.CharField(blank=True, default='', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attendee', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='schedules.calendar')),
            ],
        ),
    ]
