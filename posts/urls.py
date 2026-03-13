from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),  # <pk> - переменная pk
    path('group/<slug:name>', views.func)  # name - переменная; slug - буквы и цифры, подчеркивания и дефисы.
]