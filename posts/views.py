from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Post, Group
from django.core.paginator import Paginator


def index(request):
    template = 'temp.html'
    title = 'site'
    context = {
        'title': title,
        'text': 'Главная страница'
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_list.html'
    posts = Post.objects.filter(group=group).order_by('-created_at')[:10]
    context = {
        'group': group.title,
        'posts': posts,
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
    template = 'posts/all_posts.html'

    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)

