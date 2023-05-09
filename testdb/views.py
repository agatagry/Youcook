from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import RegisterForm, RecipeForm, RecipeStepForm, ProductForm, RecipeProductForm
from django.contrib.auth import login, logout, authenticate
from .models import Recipe, MyUser, RecipeStep, Product, RecipeProduct, CookingUnits
from django.contrib.auth.decorators import login_required
import base64


# Create your views here.


def index(request):
    recipes = Recipe.objects.filter(deleted=False).order_by('-create_time')
    if request.user.is_authenticated:
        user = request.user.nickname
    else:
        user = None
    for recipe in recipes:
        recipe.photo = bytes(recipe.photo).decode('utf-8')
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
        return HttpResponse('Witaj na profilu ' + nickname)


def recipe(request, recipe_name, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id, name=recipe_name, deleted=False)
    except Recipe.DoesNotExist:
        return render(request, 'main/recipe_not_found.html')
    recipe_steps = RecipeStep.objects.filter(recipe_id=recipe)
    recipe.photo = bytes(recipe.photo).decode('utf-8')
    recipe_products = RecipeProduct.objects.filter(recipe_id=recipe)
    product_ids = []
    for product in recipe_products:
        product_ids.append(product.product_id)
    products = list(Product.objects.filter(pk__in=product_ids))
    for step in recipe_steps:
        if step.photo is not None:
            step_photo = bytes(step.photo).decode('utf-8')
            step.photo = step_photo
    return render(request, 'main/recipe.html', {'recipe': recipe,
                                                'recipe_steps': recipe_steps,
                                                'recipe_products': recipe_products,
                                                'products': products})


@login_required
def recipe_create(request):
    if request.user.is_authenticated:
        recipe_form = RecipeForm(request.POST, request.FILES)
        recipe_step_form = RecipeStepForm(request.POST, request.FILES)
        recipe_product_form = RecipeProductForm(request.POST)
        recipe_form.fields['photo'].required = False
        recipe_step_form.fields['photo'].required = False
        if recipe_form.is_valid() and recipe_step_form.is_valid():
            recipe = recipe_form.cleaned_data
            photos = {}
            for filename, file in request.FILES.items():
                # print(filename, file)
                photo_base64 = base64.encodebytes(file.read())
                photos[filename] = photo_base64
            description = request.POST.getlist('description')
            number_order = request.POST.getlist('number_order')
            if 'photo' in photos:
                new_recipe = Recipe(user=request.user, category=recipe['category'], name=recipe['name'],
                                    servings=recipe['servings'], difficulty=recipe['difficulty'], time=recipe['time'],
                                    photo=photos['photo'], description=description[0])
            else:
                new_recipe = Recipe(user=request.user, category=recipe['category'], name=recipe['name'],
                                    servings=recipe['servings'], difficulty=recipe['difficulty'], time=recipe['time'],
                                    description=description[0])
            new_recipe.save()
            # print(photos[f'step_photo{1}'])
            for step in range(0, len(number_order)):
                # print(photos[f'step_photo_{step}'])
                if f'step_photo_{step}' in photos:
                    # print('jest')
                    new_step = RecipeStep(recipe=new_recipe, number_order=number_order[step],
                                          description=description[step + 1], photo=photos[f'step_photo_{step}'])
                else:
                    # print('nie jest')
                    new_step = RecipeStep(recipe=new_recipe, number_order=number_order[step],
                                          description=description[step + 1])
                new_step.save()
            products = {}
            quantity = {}
            for key, value in request.POST.items():
                if key.startswith('product_'):
                    products[key] = value
                elif key.startswith('quantity_'):
                    quantity[key] = value
            print(products, quantity)
            unit_list = request.POST.getlist('unit')
            print(unit_list)
            for product in range(0, len(products)):
                name, manufacturer = products[f'product_{product}'].split(' od ')
                get_product = Product.objects.get(name=name, manufacturer=manufacturer)
                get_unit = CookingUnits.objects.get(id=unit_list[product])
                new_recipe_product = RecipeProduct(recipe=new_recipe, product=get_product,
                                                   quantity=quantity[f'quantity_{product}'], unit=get_unit)
                new_recipe_product.save()
            return HttpResponseRedirect(f'/recipe_{new_recipe.name}_{new_recipe.id}')
        return render(request, 'main/new_recipe.html', {'recipe_form': recipe_form,
                                                        'recipe_step_form': recipe_step_form,
                                                        'recipe_product_form': recipe_product_form})
    else:
        return HttpResponse("Nie masz uprawnień, <a href='/auth/login'>zaloguj się</a>")


@login_required
def product_create(request):
    if request.user.is_authenticated:
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product = product_form.cleaned_data
            new_product = Product(category=product['category'], manufacturer=product['manufacturer'],
                                  name=product['name'], calories=product['calories'], total_fat=product['total_fat'],
                                  saturated_fat=product['saturated_fat'], cholesterol=product['cholesterol'],
                                  sodium=product['sodium'], total_carbohydrate=product['total_carbohydrate'],
                                  sugars=product['sugars'], fiber=product['fiber'], protein=product['protein'],
                                  barcode=product['barcode'])
            new_product.save()
            return HttpResponseRedirect(f'/product_{new_product.name}_{new_product.id}')
        return render(request, 'main/new_product.html', {'product_form': product_form})
    else:
        return HttpResponse("Nie masz uprawnień, <a href='/auth/login'>zaloguj się</a>")


def product(request, product_name, product_id):
    try:
        product = Product.objects.get(id=product_id, name=product_name)
    except Product.DoesNotExist:
        return render(request, 'main/product_not_found.html')
    return render(request, 'main/product.html', {'product': product})


def search_product(request):
    name = request.GET.get("name")
    namelist = []
    if name:
        product_objects = Product.objects.filter(name__icontains=name)
        for product in product_objects:
            label = f'{product.name} od {product.manufacturer}'
            namelist.append({'label': label, 'value': product.__str__()})
    return JsonResponse({'status': 200, 'name': namelist})
