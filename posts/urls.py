from django.urls import path, re_path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:slug>', views.group_posts),
    path('group/all', views.all_groups),
]