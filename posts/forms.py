from django.forms import ModelForm
from django.contrib.auth import get_user_model

User = get_user_model()


class PostCreationForm(ModelForm):
    class Meta:
        pass
    pass
