from django.contrib.auth.forms import UserCreationForm, UsernameField, PasswordResetForm, AuthenticationForm

from forms_mixins import StyleFormMixin
from users.models import User


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
        #field_classes = {"username": UsernameField}


class CustomLoginForm(StyleFormMixin, AuthenticationForm):
    pass


class CustomPasswordResetForm(StyleFormMixin, PasswordResetForm):
    pass