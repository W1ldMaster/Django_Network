from django.urls import path, re_path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.all_posts, name='index'),
    path('group/<slug:slug>', views.group_posts, name='group_list'),
    path('groups', views.all_groups, name='group_list'),
    path('group/all', views.all_groups),
    path('post/new/', views.post_create, name='post_create'),
    path('post/edit/', views.post_edit, name='post_edit'),
    path('posts', views.all_posts, name='post_list')
]