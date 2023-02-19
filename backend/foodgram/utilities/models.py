from django.db import models


class RecipeIngredient(models.Model):

    ingredient = models.ForeignKey(
        "recipes.Ingredient",
        on_delete=models.CASCADE
        )

    recipe = models.ForeignKey(
        "recipes.Recipe",
        on_delete=models.CASCADE
        )

    amount = models.IntegerField(null=False, )


class RecipeTag(models.Model):

    recipe = models.ForeignKey(
        "recipes.Recipe",
        on_delete=models.CASCADE
        )

    tag = models.ForeignKey(
        "recipes.Tag",
        on_delete=models.CASCADE
        )


class Subscription(models.Model):

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="subscribers"
        )

    subscriber = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="subscriptions"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "subscriber", ],
                name="follow_unique",
                ),
            models.CheckConstraint(
                check=~models.Q(user=models.F("subscriber")),
                name="follow_self"
                ),
        ]
