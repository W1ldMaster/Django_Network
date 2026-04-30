from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *


app_name = 'api'

router = DefaultRouter()

router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register('posts/(?P<post_id>\\d+)/comments', CommentViewSet, basename='comments')



urlpatterns = [
    path('', include(router.urls)),
    path('<str:author_username>/follow/', FollowViewSet.as_view({
        'post': 'create',
        'delete': 'destroy'
    }))
]


