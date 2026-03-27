from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=25)
    desription = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()  # max_length=int
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Post {self.pk}'
