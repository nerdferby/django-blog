"""
Each 'model' maps to a single database table. Each attribute represents a database
field. Django handles the database queries underwater so you don't have to touch any
SQL
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        @return: Human readable title of the post
        @rtype: string
        """
        return self.title

    def get_absolute_url(self):
        """
        Get the absolute URL of a specific 'post-detail' using it's ID
        @return: absolute url of a post, including it's id  e.g. /post/463542/
        """
        return reverse("post-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author}'s comment on {self.post.title}"
