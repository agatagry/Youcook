from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nickname = forms.CharField(required=True)

    class Meta:
        model = MyUser
        fields = ["nickname", "email", "password1", "password2"]
