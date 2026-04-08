from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


User = get_user_model()


class CreationForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_email])

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')

        return email
