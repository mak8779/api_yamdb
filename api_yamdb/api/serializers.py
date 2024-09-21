from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title, User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели категорий."""

    class Meta:
        fields = ('id', 'name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели жанров."""

    class Meta:
        fields = ('id', 'name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели произведений."""
    category = SlugRelatedField(slug_field='slug',
                                queryset=Category.objects.all())
    genre = SlugRelatedField(slug_field='slug',
                             queryset=Genre.objects.all(), many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователей."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
