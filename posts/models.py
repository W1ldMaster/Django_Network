from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    text = models.TextField() # max_length=int
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
#     comments =
#     group =
#     image =
#
#
# class Comment(models.Model):
#     text =
#     author =
#     created_at =
#     updated_at =
#     to_post =
#
#
# class Follow(models.Model):  # f = follow
#     id_fing =
#     id_fed =
#     created_at =
#
