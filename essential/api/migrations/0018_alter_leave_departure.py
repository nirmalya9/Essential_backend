# Generated by Django 5.0.1 on 2024-02-10 08:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_alter_leave_departure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='departure',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 10, 8, 9, 47, 211064, tzinfo=datetime.timezone.utc)),
        ),
    ]