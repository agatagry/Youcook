# Generated by Django 4.1.3 on 2023-04-13 19:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CookingUnits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('type', models.BooleanField()),
                ('fraction_of_base', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.CharField(max_length=100, unique=True)),
                ('nickname', models.CharField(max_length=40, unique=True)),
                ('is_verified', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(max_length=45)),
                ('calories', models.IntegerField()),
                ('total_fat', models.DecimalField(decimal_places=2, max_digits=5)),
                ('saturated_fat', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cholesterol', models.DecimalField(decimal_places=2, max_digits=5)),
                ('sodium', models.DecimalField(decimal_places=2, max_digits=5)),
                ('total_carbohydrate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('sugars', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fiber', models.DecimalField(decimal_places=2, max_digits=5)),
                ('protein', models.DecimalField(decimal_places=2, max_digits=5)),
                ('barcode', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('description', models.CharField(max_length=250)),
                ('density', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('servings', models.IntegerField()),
                ('difficulty', models.CharField(choices=[('easiest', 'Easiest'), ('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard'), ('extremely hard', 'Extremely hard')], default='Easy', max_length=14)),
                ('time', models.IntegerField()),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testdb.myuser')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingListProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='testdb.product')),
                ('shopping_list_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testdb.shoppinglist')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_order', models.IntegerField()),
                ('description', models.CharField(max_length=255)),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='testdb.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField()),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='testdb.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('product_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='testdb.product')),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testdb.recipe')),
                ('unit_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='testdb.cookingunits')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(max_length=255)),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='testdb.recipe')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='testdb.myuser')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='testdb.recipecategory'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='testdb.myuser'),
        ),
        migrations.AddField(
            model_name='product',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='testdb.productcategory'),
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('meal_type', models.CharField(choices=[('breakfast', 'Breakfast'), ('second breakfast', 'Second breakfast'), ('brunch', 'Brunch'), ('snack', 'Snack'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('supper', 'Supper')], max_length=16)),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testdb.recipe')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testdb.myuser')),
            ],
        ),
    ]
