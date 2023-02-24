from django.contrib import admin

from .models import Ingredient, Recipe, Tag


class RecipeIngredients(admin.TabularInline):
    model = Recipe.ingredients.through


class RecipeTags(admin.TabularInline):
    model = Recipe.tags.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ("favorited_count", )

    list_display = (
        "name",
        "author",
        "ingredients_set",
        "tags_set",
    )

    inlines = [RecipeIngredients, RecipeTags, ]

    list_filter = (
        "author",
        "name",
        "tags",
    )

    search_fields = ("name", )

    def favorited_count(self, obj):
        return f"{obj.is_favorited.count()} users"

    def ingredients_set(self, obj):
        return [ingredient for ingredient in obj.ingredients.all()]

    def tags_set(self, obj):
        return [tag for tag in obj.tags.all()]

    favorited_count.short_description = "Favorited by"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "measurement_unit",
    )

    list_filter = ("name", )

    search_fields = ("name", )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "color",
        "slug",
    )

    list_filter = ("name", )

    search_fields = ("name", )
