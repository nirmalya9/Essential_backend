from django.urls import path
from . import views

urlpatterns =[
    path('user/register',views.createUser),
    path('user/login',views.loginUser),
    path('user/request_friend',views.makeFriend),
    path('user/getInfo/<str:username>',views.get_user_data),
    path('user/getUsersWithSimilarInterests/<str:username>',views.get_user_with_similar_interests),
    path('user/profile/friends/<str:username>',views.viewFriends),
    path('user/post/create',views.createPost),
    path('user/post/bookmark/<str:username>/<int:post_id>',views.bookmark_post),
    path('user/post/comment',views.postComment),
    path('user/post/like',views.likePost),
    path('post/view',views.getPosts),
    path('post/comment/view/<int:post_id>',views.getComments),
    path('post/likes/view/<int:post_id>',views.viewWhoLikedPost)
]