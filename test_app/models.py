from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    content = models.TextField()


class Comment(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    content = models.TextField()

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
