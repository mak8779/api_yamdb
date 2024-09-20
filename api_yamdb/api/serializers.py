from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, GenreTitle, Title, User


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


class GenreTitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели жанров."""
    slug = serializers.SlugField(read_only=True, required=False)

    class Meta:
        fields = ('id', 'name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели произведений."""
    category = SlugRelatedField(slug_field='category', queryset=Category.objects.all())
    genre = GenreTitleSerializer(required=False, many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)

        # Для каждого достижения из списка достижений
        for genre in genres:
            # Создадим новую запись или получим существующий экземпляр из БД
            current_genre, status = Genre.objects.get_or_create(
                **genre)
            # Поместим ссылку на каждое достижение во вспомогательную таблицу
            # Не забыв указать к какому котику оно относится
            GenreTitle.objects.create(
                genre=current_genre, title=title)
        return title


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователей."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
