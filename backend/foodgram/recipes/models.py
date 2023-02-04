from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.TextField()
    color = models.TextField()
    slug = models.SlugField()


class Ingredient(models.Model):
    name = models.TextField()
    measurement_unit = models.CharField(max_length=10)


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    name = models.TextField()
    image = models.ImageField()
    text = models.TextField()
    ingredients = models.ManyToManyField("Ingredient", through="utilities.Quantity")
    tags = models.ManyToManyField(Tag)
    cooking_time = models.IntegerField()
