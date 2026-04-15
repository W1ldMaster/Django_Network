from django.test import TestCase
from django.db import connection, reset_queries
from time import sleep
from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth import get_user_model
from .models import Post

# Create your tests here.


class CacheTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные
        from .models import Post
        from django.contrib.auth.models import User

        # Создаем автора
        cls.author = User.objects.create_user(username='testuser', password='12345')
        Post.objects.create(text=f'Test Content', author=cls.author)

    def setUp(self):
        cache.clear()

    def test_CachetAllPosts(self):
        url = reverse('posts:index')
        response = self.client.get(url)
        first_connections = len(connection.queries)
        reset_queries()
        response = self.client.get(url)
        second_connections = len(connection.queries)
        self.assertNotEqual(first_connections, second_connections, 'Кэш не работает')



