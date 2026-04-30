from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from posts.models import Comment, Group, Post, Follow
from django.contrib.auth import get_user_model

from .serializers import CommentSerializer, GroupSerializer, PostSerializer, FollowSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.use)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = self.kwargs.get("post_id")
        new_queryset = Comment.objects.filter(post_id=post)
        return new_queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user,post=post)

class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self):
        return self.request.user.following.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), author__username=self.kwargs['author_username'])
        return obj

    def destroy(self, request, *args, **kwargs):

        instance = get_object_or_404(Follow, user__username=self.kwargs["author_username"])
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.kwargs["author_username"])

        if self.request.user.following.filter(user=user).exists():
            raise ValidationError(code='conflict')

        serializer.save(author=self.request.user, user=user)

