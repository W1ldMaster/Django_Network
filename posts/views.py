from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView

from .forms import CommentForm, PostCreateForm
from .models import Comment, Follow, Group, Post, User


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_list.html'
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = f'Записи сообщества: {slug}'
    context = {
        'title': title,
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def all_groups(request):
    template = 'posts/all_groups.html'
    groups = Group.objects.all()
    context = {
        'groups': groups
    }
    return render(request, template, context)


@cache_page(60)
def all_posts(request):
    keyword = request.GET.get('q', None)
    template = 'posts/index.html'
    title = 'Главная страница'
    if keyword:
        posts = (Post.objects.filter(Q(text__icontains=keyword) |
                                     Q(author__username__icontains=keyword) |
                                     Q(author__first_name__icontains=keyword) |
                                     Q(author__last_name__icontains=keyword)).select_related('author'))
    else:
        posts = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'title': title
    }
    return render(request, template, context)


@login_required
def followed_posts(request):
    template = 'posts/index.html'
    title = 'Избранные авторы'

    folllowing = Follow.objects.filter(author_id=request.user.id).values_list('user_id')
    posts = Post.objects.filter(author__id__in=folllowing).order_by('-pub_date')

    #  print(f"Количество запросов: {len(connection.queries)}")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'title': title
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    groups = Group.objects.all()
    if request.method == 'POST':
        form = PostCreateForm(
            request.POST, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save()
            return redirect('posts:profile', request.user.username)
            # return redirect('posts:post_detail', post.post_id)
    form = PostCreateForm()
    return render(request, template,
                  {'form': form, 'groups': groups})


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponse('Редактировать пост может только его автор')

    form = PostCreateForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'post': post,
        'form': form,
        'is_edit': True,
    }

    return render(request, template, context)


def profile(request, username=None):
    if not username:
        username = request.user.username

    author = get_object_or_404(User, username=username)
    try:
        following = Follow.objects.get(author=request.user, user=author)
    except ObjectDoesNotExist:
        following = False
    posts = Post.objects.filter(author__username=username).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    sum_of_posts = len(posts)

    template = 'posts/profile.html'
    context = {
        'username': username,
        'posts': posts,
        'sum_of_posts': sum_of_posts,
        'page_obj': page_obj,
        'following': following
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm()
    comments = Comment.objects.filter(post_id=post_id)
    author = post.author
    all_posts = Post.objects.filter(author=author)
    sum_of_posts = len(all_posts)
    context = {
        'post': post,
        'sum': sum_of_posts,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)


def author_posts(request, author_id):
    template = 'posts/author_posts.html'
    posts = Post.objects.filter(author_id=author_id)
    context = {
        'posts': posts,
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def profile_follow(request, username):
    follow_author = get_object_or_404(User, username=username)
    if request.user != follow_author:
        Follow.objects.get_or_create(author=request.user, user=follow_author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    unfollow_from_author = get_object_or_404(User, username=username)
    Follow.objects.filter(author=request.user).filter(
        user=unfollow_from_author).delete()
    return redirect('posts:profile', username=username)


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'posts/create_post.html'
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('posts:profile')





