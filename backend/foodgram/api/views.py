from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import Ingredient, Recipe, Tag
from utilities.models import RecipeIngredient, Subscription

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthorOrSafe
from .serializers import (IngredientSerializer, RecipeSerializer,
                          RecipeShortSerializer, SubscriptionUserSerializer,
                          TagSerializer, UserSerializer)
from .utils import convert_to_csv

User = get_user_model()


class UserViewSet(UserViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=["get", ],
        serializer_class=SubscriptionUserSerializer,
        permission_classes=(IsAuthenticated, ),
    )
    def subscriptions(self, request):

        user = request.user
        subs = User.objects.filter(pk__in=user.subscriptions.values("user"))
        data = self.paginate_queryset(subs)

        serializer = self.get_serializer(data, many=True)

        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=["post", "delete", ],
        serializer_class=SubscriptionUserSerializer,
        permission_classes=(IsAuthenticated, ),
    )
    def subscribe(self, request, id):

        to_sub = get_object_or_404(User, id=id)

        if request.method == "POST":

            try:

                Subscription.objects.create(
                    user=to_sub,
                    subscriber=request.user
                )

                serializer = self.get_serializer(to_sub)

                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )

            except IntegrityError:
                return Response(
                    {"errors":
                        {"user":
                            "You are already subscribed"
                         }
                     },
                    status=status.HTTP_400_BAD_REQUEST
                )

        elif request.method == "DELETE":

            try:

                Subscription.objects.get(
                    user=to_sub,
                    subscriber=request.user
                ).delete()

                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )

            except Subscription.DoesNotExist as e:
                return Response(
                    {"errors":
                        {"user": f"{e.args[0]}"}
                     },
                    status=status.HTTP_400_BAD_REQUEST
                )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = (AllowAny, )
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter, )
    search_fields = ("name", )
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = (AllowAny, )
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthorOrSafe, )
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,
                       filters.OrderingFilter)
    filterset_class = RecipeFilter

    @action(
        detail=False,
        methods=["get", ],
        permission_classes=(IsAuthenticated, ),
    )
    def download_shopping_cart(self, request):

        data = RecipeIngredient.objects.filter(
            recipe__in=Recipe.objects.filter(
                in_shopping_cart=request.user
            )
        )

        if data.exists():
            data = data.values(
                "ingredient__name",
                "ingredient__measurement_unit"
            ).annotate(total=Sum("amount"))

            fields = data[0].keys()
            response = convert_to_csv(data, fields)

            return response

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(
        detail=True,
        methods=["post", "delete", ],
        permission_classes=(IsAuthenticated, ),
    )
    def shopping_cart(self, request, pk):

        recipe = get_object_or_404(Recipe, pk=pk)
        cart_check = recipe.in_shopping_cart.filter(
            id=request.user.id
        ).exists()

        if request.method == "POST":

            if cart_check:

                return Response(
                    {"errors":
                        {"recipe":
                            "Recipe is already in shopping cart"
                         }
                     },
                    status=status.HTTP_400_BAD_REQUEST
                )

            recipe.in_shopping_cart.add(request.user)
            recipe.save()
            serializer = RecipeShortSerializer(recipe)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        elif request.method == "DELETE":

            if not cart_check:

                return Response(
                    {"errors":
                        {"recipe":
                            "Recipe is not in your shopping cart"
                         }
                     },
                    status=status.HTTP_400_BAD_REQUEST
                )

            recipe.in_shopping_cart.remove(request.user)
            recipe.save()

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

    @action(
        detail=True,
        methods=["post", "delete", ],
        permission_classes=(IsAuthenticated, ),
    )
    def favorite(self, request, pk):

        recipe = get_object_or_404(Recipe, pk=pk)
        favorites_check = recipe.is_favorited.filter(
            id=request.user.id
        ).exists()

        if request.method == "POST":

            if favorites_check:

                return Response(
                    {"errors":
                        {"recipe":
                            "Recipe is already in your favorites"
                         }
                     },
                    status=status.HTTP_400_BAD_REQUEST
                )

            recipe.is_favorited.add(request.user)
            recipe.save()
            serializer = RecipeShortSerializer(recipe)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        elif request.method == "DELETE":

            if not favorites_check:

                return Response(
                    {"errors":
                        {"recipe":
                            "Recipe is not in your favorites"
                         }
                     },
                    status=status.HTTP_400_BAD_REQUEST
                )

            recipe.is_favorited.remove(request.user)
            recipe.save()

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
