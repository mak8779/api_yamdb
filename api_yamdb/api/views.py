from rest_framework import filters, mixins, viewsets
#from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, TitleViewSerializer,
                             UserSerializer)

from reviews.models import Category, Genre, Title, User

from api.permissions import IsAdminOrReadOnly


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass



class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет групп категорий."""

    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    # pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет групп жанров."""

    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    # pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет групп произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('category', 'genre', 'name', 'year')
    # pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleViewSerializer
        return TitleSerializer
