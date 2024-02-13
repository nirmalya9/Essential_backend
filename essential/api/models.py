from django.db import models
from django.utils import timezone

class Users(models.Model):
    username = models.CharField(null=False, primary_key=True, max_length=50)
    name = models.CharField(null=False, max_length=150)
    pfp = models.ImageField(null=True, default="",upload_to='face_id/')
    password = models.CharField(null=False, max_length=128)
    email = models.EmailField(null=False)
    college = models.CharField(null=True, default="", max_length=50)
    interests = models.TextField(null=True, default="", max_length=50)
    about = models.TextField(default="")
    bookmarks = models.ManyToManyField('api.Posts',blank=True)


class UserProfile(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="user_profile")
    friend = models.ManyToManyField('api.Users',blank = True, symmetrical=False)

class Comments(models.Model):
    id = models.AutoField(primary_key = True)
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name="replies",null=True)
    post = models.ForeignKey('api.Posts', on_delete=models.CASCADE, related_name="post_comments")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_comments")
    content = models.CharField(max_length=300)
    like_counter = models.IntegerField(default=0)
    #liked_by = models.ManyToManyField(Users, blank=True, symmetrical=False, related_name="liked_comments")
    timestamp = models.DateTimeField(default=timezone.now)
    #replies = models.ManyToManyField('self', blank=True)

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    posted_by = models.ForeignKey(Users, on_delete=models.CASCADE,related_name="posts")
    content = models.CharField(max_length=300, null=False)
    image = models.ImageField(upload_to='post_images/',blank=True,default="")  # Specify a directory to store images
    like_counter = models.IntegerField(default=0)
    comment_counter = models.IntegerField(default=0)
    liked_by = models.ManyToManyField('api.Users',null=True, related_name="liked_posts")
    timestamp = models.DateTimeField(default=timezone.now, blank=True, null=True)
    comments = models.ManyToManyField('api.Comments', related_name="post_comments", null = True)

class Warden(models.Model):
    id = models.CharField(primary_key=True,max_length=50)
    name = models.TextField(null=False)
    password = models.CharField(null=False, max_length=60)
class Leave(models.Model):
    id = models.AutoField(primary_key = True)
    student = models.ForeignKey('api.Users',blank = False,related_name= "leave_forms",on_delete=models.CASCADE)
    warden = models.ForeignKey('api.Users',blank = True,related_name="approved_leaves",on_delete=models.CASCADE)
    reason = models.TextField(null = False, default='')
    departure = models.DateTimeField(null=False,default=timezone.now())
    arrival = models.DateTimeField(null = False, default= "")
    denial_reason = models.TextField(default="")
    status = models.CharField(max_length=20, default="pending")

class HostelProfile(models.Model):
    student = models.ForeignKey('api.Users',on_delete=models.CASCADE,null=False)
    room = models.CharField(max_length=5,)
