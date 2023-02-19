from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters import rest_framework as filters
from recipes.models import Recipe

User = get_user_model()


class RecipeFilter(filters.FilterSet):

    is_in_shopping_cart = filters.BooleanFilter(
        field_name="in_shopping_cart",
        method="filter_cart",
        )

    is_favorited = filters.BooleanFilter(
        field_name="is_favorited",
        method="filter_favorites",
        )

    tags = filters.CharFilter(
        field_name="tags__slug",
        method="filter_tags",
        )

    class Meta:
        model = Recipe
        fields = (
            "tags",
            "author",
            "is_favorited",
            "is_in_shopping_cart",
            )

    def filter_tags(self, queryset, name, tags):
        return queryset.filter(tags__slug__contains=tags)

    def filter_favorites(self, queryset, name, value):
        if value:
            return queryset.filter(is_favorited=self.request.user)
        return queryset.filter(~Q(is_favorited=self.request.user))

    def filter_cart(self, queryset, name, value):
        if value:
            return queryset.filter(in_shopping_cart=self.request.user)
        return queryset.filter(~Q(in_shopping_cart=self.request.user))
