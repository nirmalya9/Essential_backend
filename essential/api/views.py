from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import *
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@api_view(["POST"])
def createUser(request):
    serializer = createUserSerializer(data=request.data)
    if (serializer.is_valid()):
        serializer.save()
        user_instance = Users.objects.get(pk = serializer.validated_data["username"])
        userprofile_instance = UserProfile.objects.create(user = user_instance)
        userprofile_instance.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def loginUser(request):
    serializer = userLoginSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user_instance = Users.objects.get(pk=serializer.validated_data['username'])
            if (user_instance.password == serializer.validated_data['password']):
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"Wrong password"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"Wrong username"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_user_data(request, username):
    try:
        user_instance = Users.objects.get(username=username)
        userprofile_instance = UserProfile.objects.filter(user = user_instance)
        profile_serializer = UserProfileSerializer(userprofile_instance[0])
        serializer = UsersSerializer(user_instance,context = {'friends':profile_serializer.data['friend']})

        return Response(serializer.data)
    except Users.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
@api_view(["GET"])
def get_user_with_similar_interests(request, username):
    try:
        reference_user = Users.objects.get(username=username)
        reference_interests = reference_user.interests.split(',')
        print(f"Reference Interests: {reference_interests}")

        similar_users = Users.objects.exclude(username=username).filter(interests__contains=reference_interests)
        print(f"Similar Users: {similar_users.values()}")

        serializer = UsersSerializer(similar_users, many=True)
        return Response(serializer.data)
    except Users.DoesNotExist:
        return Response({"error": "User not found"}, status=404)




@api_view(["POST"])
def createPost(request):
    serializer = createPostSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user_instance = Users.objects.get(pk=serializer.validated_data['username'])
            image = request.FILES.get('image')
            post = Posts.objects.create(
                posted_by=user_instance,
                content=serializer.validated_data['content'],
                image=image
            )
            post.save()
            return Response({"status": "Post has been uploaded"})
        except Exception as e:
            return Response({"status": "Some error occurred", "error": str(e)})
    else:
        return Response(serializer.errors)


@api_view(["GET"])
def getPosts(request):
    try:
        posts = Posts.objects.all()
        serializer = viewPostsSerializer(instance=posts, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"Error": str(e)})


@api_view(["POST"])
def postComment(request):
    serializer = commentSerializer(data=request.data)
    if serializer.is_valid():
        try:
            post_instance = Posts.objects.get(pk=serializer.validated_data["post_id"])
            user_instance = Users.objects.get(pk=serializer.validated_data["username"])
            create_comment = Comments.objects.create(
                post=post_instance,
                user=user_instance,
                content=serializer.validated_data["content"]
            )
            post_instance.comment_counter += 1
            create_comment.save()
            post_instance.comments.add(create_comment)
            post_instance.save()

            return Response({"status": "comment posted"})
        except Exception as e:
            return Response({"Error": str(e)})
    else:
        return Response(serializer.errors)
@api_view(["GET"])
def bookmark_post(request,username,post_id):
    try:
        user_instance = Users.objects.get(pk = username)
        post_instance = Posts.objects.get(pk = post_id)
        user_instance.bookmarks.add(post_instance)
        return Response({"status":"Post added to bookmarks"})
    except Exception as e:
        return Response({"Error": str(e)})


@api_view(["GET"])
def getComments(request,post_id):
    try:
        post_instance = Posts.objects.get(pk=post_id)
        serializer = viewCommentSerializer(instance=post_instance.post_comments.all(), many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"Error": str(e)})


@api_view(["POST"])
def likePost(request):
    try:
        post_id = request.data["post_id"]
        user = request.data["username"]
        post_instance = Posts.objects.get(pk=post_id)
        user_instance = Users.objects.get(pk=user)
        post_instance.like_counter += 1
        post_instance.liked_by.add(user_instance)
        post_instance.save()
        return Response({"status": "You liked the post"})
    except Exception as e:
        return Response({"error": str(e)})


@api_view(["GET"])
def viewWhoLikedPost(request,post_id):
    try:
        post_instance = Posts.objects.get(pk=post_id)
        users = post_instance.liked_by.all()
        serializer = viewUsersSerializer(instance=users,many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"Error":str(e)})
@api_view(["POST"])
def makeFriend(request):
    serializers = makeFriendSerializer(data=request.data)
    if serializers.is_valid():
        try:
            user_instance = Users.objects.get(pk = serializers.validated_data["your_username"])
            friend_instance = Users.objects.get(pk = serializers.validated_data["friend_username"])
            user_profile_instance = UserProfile.objects.filter(user = user_instance)
            if not user_profile_instance[0].friend.filter(pk = friend_instance.pk).exists():
                user_profile_instance[0].friend.add(friend_instance)
                return Response({"status": f"{friend_instance.name} added as friend"})
            else:
                return  Response({"status": f"{friend_instance.name} is already a friend"})
        except Exception as e:
            return Response({"Error":str(e)})
    else:
        return Response(serializers.errors)

@api_view(["GET"])
def viewFriends(request,username):
    try:
        user_instance = Users.objects.get(pk = username)
        user_profile_instance = UserProfile.objects.filter(user=user_instance)[0]
        serializers = viewWhoLikedPostSerializer(user_profile_instance.friend.all(),many=True)
        return Response(serializers.data)
    except Exception as e:
        return Response({"Error":str(e)})
