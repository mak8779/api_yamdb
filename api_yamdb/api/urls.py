from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from rest_framework import routers

from api.views import (CategoryViewSet, GenreViewSet, TitleViewSet)

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
