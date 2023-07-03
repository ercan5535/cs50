from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    content = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.author}'s post"

class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")

    def __str__(self):
        return f"{self.owner}'s like"
    
class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")
    comment = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.owner}'s comment"
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follower")

    def __str__(self):
        return f"{self.follower} is following {self.followed}"