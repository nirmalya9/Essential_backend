from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import serializers
from .models import *


class createUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'name', 'password', 'email', 'college', 'interests')


class userLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class createPostSerializer(serializers.Serializer):
    username = serializers.CharField(allow_null=False)
    content = serializers.CharField(max_length=300, allow_null=False)


class commentSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(allow_null=False)
    username = serializers.CharField(allow_blank=False)
    content = serializers.CharField(max_length=300)


class viewPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ["id", "content", "image", "like_counter", "comment_counter", "timestamp", "posted_by"]


class viewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"


class viewUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'name']


class makeFriendSerializer(serializers.Serializer):
    your_username = serializers.CharField()
    friend_username = serializers.CharField()



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'name', 'email', 'college', 'interests', 'about', 'bookmarks']
    def to_representation(self, instance):
        context = self.context

        # Access data from the context
        additional_data = context.get('friends')

        data = super().to_representation(instance)

        # Use additional_data in the representation
        data['friends'] = additional_data

        return data