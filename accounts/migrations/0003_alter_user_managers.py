# Generated by Django 3.2.18 on 2023-06-08 05:28

from django.db import migrations
import schedules.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20230601_1153'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', schedules.models.CustomUserManager()),
            ],
        ),
    ]