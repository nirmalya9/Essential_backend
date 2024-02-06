from django.test import TestCase
from django.utils import timezone
from .models import Users, Posts, Comments

class ModelTestCase(TestCase):
    def setUp(self):
        # Create 10 test users
        self.users = [Users.objects.create(username=f'user{i}', name=f'User {i}', password=f'password{i}', email=f'user{i}@example.com') for i in range(1, 11)]

        # Create test post
        self.post = Posts.objects.create(posted_by=self.users[0], content='Test Post', like_counter=0)

        # Create test comment
        self.comment = Comments.objects.create(post=self.post, user=self.users[1], content='Test Comment', like_counter=0)

    def test_user_creation(self):
        user_count = Users.objects.count()
        self.assertEqual(user_count, 10)  # Check if ten users are created

    def test_post_creation(self):
        post_count = Posts.objects.count()
        self.assertEqual(post_count, 1)  # Check if one post is created

    def test_comment_creation(self):
        comment_count = Comments.objects.count()
        self.assertEqual(comment_count, 1)  # Check if one comment is created

    def test_user_friends(self):
        # Add user2 as a friend of user1
        self.users[0].friends.add(self.users[1])
        friends = self.users[0].friends.all()
        self.assertIn(self.users[1], friends)  # Check if user2 is a friend of user1

    def test_post_likes(self):
        # Add user1 as a user who liked the post
        self.post.liked_by.add(self.users[0])
        liked_users = self.post.liked_by.all()
        self.assertIn(self.users[0], liked_users)  # Check if user1 liked the post

    def test_comment_replies(self):
        # Add a reply to the comment
        reply = Comments.objects.create(post=self.post, user=self.users[0], content='Test Reply', like_counter=0)
        self.comment.replies.add(reply)
        replies = self.comment.replies.all()
        self.assertIn(reply, replies)  # Check if the reply is associated with the comment

    def test_timestamps(self):
        # Check if timestamps are set correctly for Comments model
        now = timezone.now()
        self.assertLessEqual(self.comment.timestamp, now)

    def test_related_names(self):
        # Check if related names work as expected
        posts = self.users[0].posts.all()
        liked_posts = Posts.objects.filter(liked_by=self.users[0])
        post_comments = self.post.post_comments.all()
        user_comments = self.users[1].user_comments.all()

        # Explicitly add the post to the liked_by field of user1
        self.post.liked_by.add(self.users[0])

        # Create a new comment associated with the user
        new_comment = Comments.objects.create(post=self.post, user=self.users[1], content='Another Comment',
                                              like_counter=0)
        liked_comments = Comments.objects.filter(liked_by=self.users[1])

        self.assertIn(self.post, posts)
        self.assertIn(self.post, liked_posts)
        self.assertIn(self.comment, post_comments)
        self.assertIn(self.comment, user_comments)



