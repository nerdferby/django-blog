from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from blog.models import Post


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["post", "user"], name="like-post-user")
        ]
