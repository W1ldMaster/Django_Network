from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Post, Group


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
    posts = Post.objects.filter(group=group).order_by('created_at')[:10]
    context = {
        'group': group.title,
        'posts': posts,
    }
    return render(request, template, context)


def all_groups(request):
    template = 'posts/all_groups.html'
    pass


def based(request):
    template = 'homework.html'
    title = 'Yandex'
    text = 'Ссылка для перехода на официальный сайт Яндекс'
    url = 'https://ya.ru'

    context = {
        'title': title,
        'text': text,
        'url': url
    }

    return render(request, template, context)

