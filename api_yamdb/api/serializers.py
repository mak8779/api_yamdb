from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField
from rest_framework.validators import UniqueTogetherValidator

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


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели произведений."""
    category = SlugRelatedField(slug_field='category', read_only=True)
    genres = GenresSerializer(read_only=True, many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genres', 'category')
        model = Title


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователей."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
