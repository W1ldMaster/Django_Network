from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index),
    path('1', views.index2),
    path('2', views.based),
    re_path(r'.', views.index3)
    #  <pk> - переменная pk
    #  path('group/<slug:name>', views.index())  # name - переменная; slug - буквы и цифры, подчеркивания и дефисы.
]