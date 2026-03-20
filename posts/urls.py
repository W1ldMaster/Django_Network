from django.urls import path, re_path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:slug>', views.group_posts, name='see_group'),
    path('groups', views.all_groups, name='group_list'),
    path('group/all', views.all_groups),
    path('posts', views.all_posts, name='post_list')
]