from .forms import CreationForm, EditUserForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


@login_required
def profile_edit(request):
    template = 'users/profile_edit.html'

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('posts:my_profile')
        else:
            messages.error(request, 'Исправьте ошибки в форме!')
    else:
        user_form = EditUserForm(instance=request.user)

    context = {
        'form': user_form,
    }

    return render(request, template, context)

