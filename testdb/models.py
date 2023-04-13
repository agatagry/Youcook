from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone


class MyUser(AbstractBaseUser):
    email = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=40, unique=True)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'nickname']


class ProductCategory(models.Model):
    """
    Product category model:
        name: short name for category, example: yogurt, flour, mayonnaise etc.
        description: short desctription for category, example: Food produced by bacterial fermentation of milk.
        density: density in g/ml, density = mass/volume. Used for calculator mass <-> volume
    """
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=250)
    density = models.FloatField()


class Product(models.Model):
    category_id = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING)
    manufacturer = models.CharField(max_length=45, blank=False, null=False)
    calories = models.IntegerField()
    total_fat = models.DecimalField(max_digits=5, decimal_places=2)
    saturated_fat = models.DecimalField(max_digits=5, decimal_places=2)
    cholesterol = models.DecimalField(max_digits=5, decimal_places=2)
    sodium = models.DecimalField(max_digits=5, decimal_places=2)
    total_carbohydrate = models.DecimalField(max_digits=5, decimal_places=2)
    sugars = models.DecimalField(max_digits=5, decimal_places=2)
    fiber = models.DecimalField(max_digits=5, decimal_places=2)
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    barcode = models.CharField(max_length=100)


class CookingUnits(models.Model):
    """
    Cooking Units model:
        name: short name for unit, example: cup, table spoon, mililiters, grams,
        type: 1 for volume (cup, liter etc.), 0 for mass (kilograms, grams etc.)
        fraction_of_base: base units are mililiters and grams, e.g. for kilogram is 0.001, international ounce is 28,34952
    """
    name = models.CharField(max_length=30)
    type = models.BooleanField()
    fraction_of_base = models.FloatField()


class RecipeCategory(models.Model):
    """
    Recipe category model:
        name: short name for category, example: dinner, breakfest, party
        description: short description for category, example: Below you find recipes for tasty dinner.
    """
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=250)


class Recipe(models.Model):
    DIFFICULTY = [
        ('easiest', 'Easiest'),
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('extremely hard', 'Extremely hard'),
    ]
    user_id = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, blank=False, null=False)
    category_id = models.ForeignKey(RecipeCategory, on_delete=models.DO_NOTHING, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    servings = models.IntegerField(blank=False, null=False)
    difficulty = models.CharField(max_length=14, choices=DIFFICULTY, default='Easy', blank=False, null=False)
    time = models.IntegerField(blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    modify_time = models.DateTimeField(default=timezone.now, blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.modify_time = timezone.now


class RecipeStep(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING, blank=False, null=False)
    number_order = models.IntegerField(blank=False, null=False)
    description = models.CharField(max_length=255, blank=False, null=False)


class RecipeRate(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING)
    rate = models.IntegerField()


class RecipeProduct(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING, blank=True, null=True)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE, blank=False, null=False)
    unit_id = models.ForeignKey(CookingUnits, on_delete=models.DO_NOTHING, blank=False, null=False)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)


class RecipeComment(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING, blank=False, null=False)
    user_id = models.ForeignKey(MyUser, on_delete=models.SET_NULL, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=255, blank=False, null=False)


class Calendar(models.Model):
    MEAL_TYPE = [
        ('breakfast', 'Breakfast'),
        ('second breakfast', 'Second breakfast'),
        ('brunch', 'Brunch'),
        ('snack', 'Snack'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('supper', 'Supper'),
    ]
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=False, null=False)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)
    meal_type = models.CharField(max_length=16, choices=MEAL_TYPE, blank=False, null=False)


class ShoppingList(models.Model):
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(max_length=50, blank=False, null=False)


class ShoppingListProduct(models.Model):
    shopping_list_id = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, blank=False, null=False)
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING, blank=False, null=False)
    quantity = models.IntegerField()
