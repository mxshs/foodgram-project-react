from django.contrib.auth import get_user_model
from rest_framework import viewsets

from recipes.models import Recipe
from .serializers import UserSerializer, RecipeSerializer



User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
