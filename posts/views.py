from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request):
    template = 'temp.html'
    title = 'site'
    context = {
        'title': title,
        'text': 'Главная страница'
    }
    return render(request, template, context)


def index2(request):
    template = 'temp.html'
    title = 'site'
    context = {
        'title': title,
        'text': 'Вложенная страница'
    }
    return render(request, template, context)


def index3(request):
    template = 'temp.html'
    title = 'site'
    context = {
        'title': title,
        'text': 'Какая-то страница'
    }
    return render(request, template, context)


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
