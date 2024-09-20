from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, UserSerializer)

from reviews.models import Category, Genre, Title, User


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет групп категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет групп жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
