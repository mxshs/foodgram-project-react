from django.db import models


class Quantity(models.Model):
    ingredient = models.ForeignKey("recipes.Ingredient", on_delete=models.CASCADE)
    recipe = models.ForeignKey("recipes.Recipe", on_delete=models.CASCADE)
    quantity = models.IntegerField()
