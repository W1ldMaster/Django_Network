from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy


class SignUp(CreateView):
    form_class = CreateView
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


