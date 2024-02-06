# Generated by Django 5.0.1 on 2024-02-05 14:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_posts_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='replies',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='comments',
        ),
        migrations.AddField(
            model_name='comments',
            name='reply',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='api.comments'),
        ),
    ]
