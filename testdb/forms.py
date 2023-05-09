from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser, Recipe, RecipeStep, Product, RecipeProduct


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nickname = forms.CharField(required=True)

    class Meta:
        model = MyUser
        fields = ["nickname", "email", "password1", "password2"]


class RecipeForm(forms.ModelForm):
    photo = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept': 'image/jpeg, image/png'}))

    class Meta:
        model = Recipe
        fields = ('category', 'name', 'servings', 'difficulty', 'time', 'description')


class RecipeStepForm(forms.ModelForm):
    photo = forms.FileField(required=False, widget=forms.FileInput(attrs={'name': 'step_photo',
                                                                          'accept': 'image/jpeg'}))

    class Meta:
        model = RecipeStep
        fields = ('number_order', 'description')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'manufacturer', 'name', 'calories', 'total_fat', 'saturated_fat', 'cholesterol', 'sodium',
                  'total_carbohydrate', 'sugars', 'fiber', 'protein', 'barcode')


class RecipeProductForm(forms.ModelForm):
    product = forms.CharField()

    class Meta:
        model = RecipeProduct
        fields = ('product', 'quantity', 'unit')
