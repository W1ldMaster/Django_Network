from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from .models import Post, Group, User, Comment
from django.core.paginator import Paginator
from .forms import PostCreateForm, CommentForm


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


def all_posts(request):
    template = 'posts/index.html'
    posts = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
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
        'page_obj': page_obj
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





