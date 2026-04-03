from django.db import models
from django.contrib.auth import get_user_model
from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=25)
    desription = models.TextField()

    def __str__(self):
        return self.title


class Post(CreatedModel):
    text = models.TextField(verbose_name='Текст поста', help_text='Введите текст поста')  # max_length=int
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    # pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='posts/', blank=True)

    def __str__(self):
        returntext = self.text[:15] if len(str(self.text)) <= 15 else f'{self.text[:15]}...'
        return returntext


class Comment(CreatedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField('Текст комментария', max_length=300)

    def __str__(self):
        returntext = self.text[:15] if len(str(self.text)) <= 15 else f'{self.text[:15]}...'
        return returntext


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')




