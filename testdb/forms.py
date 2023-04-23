from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser, Recipe, RecipeStep


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nickname = forms.CharField(required=True)

    class Meta:
        model = MyUser
        fields = ["nickname", "email", "password1", "password2"]


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('category_id', 'name', 'servings', 'difficulty', 'time', 'description')


class RecipeStepForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        fields = ('number_order', 'description')
