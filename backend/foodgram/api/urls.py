from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet, RecipeViewSet

app_name = 'api'

router = SimpleRouter()
router.register('users', UserViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
