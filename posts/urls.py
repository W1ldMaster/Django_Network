from django.urls import path, re_path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.index, name='index'),
    path('1', views.index2),
    path('2', views.based),
    re_path('3', views.index3)
    #  <pk> - переменная pk
    #  path('group/<slug:name>', views.index(), name='group:name')  # name - переменная;
    #                                                               slug - буквы и цифры, подчеркивания и дефисы.
]