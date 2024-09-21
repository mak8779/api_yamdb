from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, UserSerializer)

from reviews.models import Category, Genre, Title, User


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет групп категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет групп жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет групп произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('category', 'genre', 'name', 'year')
