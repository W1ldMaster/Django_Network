from django.urls import path, re_path
from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.all_posts, name='index'),
    path('group/<slug:slug>', views.group_posts, name='group_list'),
    path('groups/all', views.all_groups, name='all_groups'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('posts', views.all_posts, name='post_list'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('my/profile/', views.profile, name='my_profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('author/<int:author_id>/', views.author_posts, name='author_posts'),
    path('posts/<int:post_id>/comment', views.add_comment, name='add_comment'),
    path('<str:username>/follow/', views.profile_follow, name='follow'),
    path('<str:username>/unfollow/', views.profile_unfollow, name='unfollow'),
    path('follow/index', views.followed_posts, name='follow_posts')
]