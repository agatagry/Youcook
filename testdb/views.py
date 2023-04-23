from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegisterForm, RecipeForm, RecipeStepForm
from django.contrib.auth import login, logout, authenticate
from .models import Recipe, MyUser, RecipeStep
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    recipes = Recipe.objects.filter(deleted=False).order_by('-create_time')
    if request.user.is_authenticated:
        user = request.user.nickname
    else:
        user = None

    return render(request, 'main/index.html', {'recipes': recipes,
                                               'user': user})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


def profile(request, nickname):
    try:
        MyUser.objects.get(nickname=nickname)
    except MyUser.DoesNotExist:
        return render(request, 'main/profile_not_found.html')
    user_recipes = Recipe.objects.filter(user_id=request.user).order_by('-create_time')
    if request.user.nickname == nickname:
        return render(request, 'main/profile.html', {'user': nickname,
                                                     'recipes': user_recipes})
    else:
        return HttpResponse('Witaj na profilu '+nickname)


def recipe(request, recipe_name):
    try:
        recipe = Recipe.objects.get(name=recipe_name, deleted=False)
        return render(request, 'main/index.html')
    except Recipe.DoesNotExist:
        return render(request, 'main/recipe_not_found.html')


@login_required
def recipe_create(request):
    if request.user.is_authenticated:
        recipe_form = RecipeForm(request.POST)
        recipe_step_form = RecipeStepForm(request.POST)
        if recipe_form.is_valid() and recipe_step_form.is_valid():
            recipe = recipe_form.cleaned_data
            description = request.POST.getlist('description')
            number_order = request.POST.getlist('number_order')
            new_recipe = Recipe(user_id=request.user, category_id=recipe['category_id'], name=recipe['name'],
                                servings=recipe['servings'], difficulty=recipe['difficulty'], time=recipe['time'],
                                description=description[0])
            new_recipe.save()
            for step in range(0, len(number_order)):
                new_step = RecipeStep(recipe_id=new_recipe, number_order=number_order[step], description=description[step+1])
                new_step.save()
            return HttpResponseRedirect(f'/recipe_{new_recipe.name}')
        return render(request, 'main/new_recipe.html', {'recipe_form': recipe_form,
                                                        'recipe_step_form': recipe_step_form})
    else:
        return HttpResponse("Nie masz uprawnień, <a href='/auth/login'>zaloguj się</a>")
