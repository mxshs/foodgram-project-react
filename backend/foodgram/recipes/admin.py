from django.contrib import admin

from .models import Recipe, Ingredient


class RecipeIngredients(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
    )

    inlines = [RecipeIngredients, ]

    list_filter = ('author', 'name', 'tags')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )

    list_filter = ('name', )
