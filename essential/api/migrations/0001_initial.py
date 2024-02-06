# Generated by Django 5.0.1 on 2024-02-05 08:49

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300)),
                ('like_counter', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('replies', models.ManyToManyField(blank=True, related_name='replies', to='api.comments')),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300)),
                ('image', models.ImageField(null=True, upload_to='post_images')),
                ('like_counter', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('comments', models.ManyToManyField(blank=True, related_name='post_comments', to='api.comments')),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='api.posts'),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('college', models.CharField(default='', max_length=50, null=True)),
                ('interests', models.CharField(default='', max_length=50, null=True)),
                ('bookmarks', models.ManyToManyField(to='api.posts')),
                ('friends', models.ManyToManyField(blank=True, to='api.users')),
            ],
        ),
        migrations.AddField(
            model_name='posts',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', to='api.users'),
        ),
        migrations.AddField(
            model_name='posts',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='api.users'),
        ),
        migrations.AddField(
            model_name='comments',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='liked_comments', to='api.users'),
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to='api.users'),
        ),
    ]