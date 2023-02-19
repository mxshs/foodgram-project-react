import base64

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import serializers
from utilities.models import RecipeIngredient

User = get_user_model()


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):

        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            extension = format.split("/")[-1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name="temp." + extension
                )

        return super().to_internal_value(data)


class TagField(serializers.PrimaryKeyRelatedField):

    def to_representation(self, data):
        tag = Tag.objects.get(pk=data.pk)
        serializer = TagSerializer(tag)
        return serializer.data

    def get_queryset(self):
        return Tag.objects.all()


class UserSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            )

    def get_is_subscribed(self, obj):

        return obj.subscribers.filter(
            subscriber=self.context["request"].user.id
            ).exists()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "color",
            "slug",
            )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "measurement_unit",
            )


class IngredientQuantitySerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source="ingredient.id")

    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit",
        required=False
        )

    name = serializers.CharField(
        source="ingredient.name",
        required=False
        )

    class Meta:
        model = RecipeIngredient
        fields = (
            "amount",
            "measurement_unit",
            "id",
            "name",
             )


class RecipeSerializer(serializers.ModelSerializer):

    author = UserSerializer(required=False)

    ingredients = IngredientQuantitySerializer(
        source="recipeingredient_set",
        many=True,
        required=True,
        )

    tags = TagField(
        many=True,
        required=True
        )

    image = Base64ImageField(required=True)
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
            "is_in_shopping_cart",
            "is_favorited",
            )

    def create(self, validated_data):

        ingredients = validated_data.pop("recipeingredient_set")
        tags = validated_data.pop("tags")
        author = self.context["request"].user

        recipe = Recipe.objects.create(
            **validated_data,
            author=author
            )

        for ingredient in ingredients:
            ingredient["recipe"] = recipe
            ingredient["ingredient"] = Ingredient.objects.get(
                id=ingredient["ingredient"]["id"]
                )

            RecipeIngredient.objects.create(**ingredient)

        recipe.tags.set(tags)

        return recipe

    def update(self, recipe, validated_data):

        ingredients = validated_data.pop("recipeingredient_set")
        tags = validated_data.pop("tags")

        for ingredient in ingredients:
            ingredient["recipe"] = recipe
            ingredient["ingredient"] = Ingredient.objects.get(
                id=ingredient["ingredient"]["id"]
                )

            RecipeIngredient.objects.get_or_create(**ingredient)

        recipe.__dict__.update(validated_data)
        recipe.tags.set(tags)
        recipe.save()

        return recipe

    def get_is_in_shopping_cart(self, obj):

        return obj.in_shopping_cart.filter(
            id=self.context["request"].user.id
            ).exists()

    def get_is_favorited(self, obj):

        return obj.is_favorited.filter(
            id=self.context["request"].user.id
            ).exists()


class RecipeShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time"
            )


class TokenCreateSerializer(serializers.Serializer):

    password = serializers.CharField()
    email = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, data):
        password = data.get("password")
        email = data.get("email")

        user = User.objects.filter(email=email)
        if not user.exists() or not user[0].check_password(password):
            raise ValidationError("Invalid credentials")

        self.user = user[0]

        return data


class SubscriptionUserSerializer(UserSerializer):

    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
            )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        limit = self.context["request"].query_params.get("recipes_limit")
        recipes = Recipe.objects.filter(author=obj)
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeShortSerializer(recipes, many=True)
        return serializer.data
