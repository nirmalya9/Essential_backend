# Generated by Django 5.0.1 on 2024-02-05 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_posts_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='posts',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
