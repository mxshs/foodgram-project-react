from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):

    name = models.TextField(null=False, )
    color = models.TextField(null=False, )
    slug = models.SlugField(null=False, )

    class Meta:
        indexes = [
            models.Index(fields=["name", ]),
        ]

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):

    name = models.TextField(null=False, )
    measurement_unit = models.CharField(max_length=25, null=False,)

    class Meta:
        indexes = [
            models.Index(fields=["name", ]),
        ]
        unique_together = ("name", "measurement_unit", )

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
    )

    name = models.TextField(null=False, )

    image = models.ImageField(
        upload_to="recipes/images/",
        null=False,
    )

    text = models.TextField(null=False, )

    ingredients = models.ManyToManyField(
        Ingredient,
        related_name="recipes",
        through="utilities.RecipeIngredient",
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="tagged",
        through="utilities.RecipeTag",
    )

    cooking_time = models.IntegerField(null=False, )

    is_favorited = models.ManyToManyField(
        User,
        related_name="favorited",
        blank=True,
    )

    in_shopping_cart = models.ManyToManyField(
        User,
        related_name="in_cart",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
