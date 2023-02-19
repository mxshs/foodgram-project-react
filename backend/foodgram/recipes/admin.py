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
    )

    inlines = [RecipeIngredients, RecipeTags, ]

    list_filter = (
        "author",
        "name",
        "tags",
    )

    def favorited_count(self, obj):
        return f"{obj.is_favorited.count()} users"

    favorited_count.short_description = "Favorited by"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "measurement_unit",
    )

    list_filter = ("name", )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "color",
        "slug",
    )

    list_filter = ("name", )
