from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
import datetime

from reviews.models import Category, Genre, Title

from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели произведений."""
    category = SlugRelatedField(slug_field='slug',
                                queryset=Category.objects.all())
    genre = SlugRelatedField(slug_field='slug',
                             queryset=Genre.objects.all(), many=True)

    def validate_year(self, value):
        if value > datetime.date.today().year:
            raise serializers.ValidationError(
                'Будущий год нельзя ставить'
            )
        return value

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class TitleViewSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра списка произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, max_length=150)

    def validate(self, data):
        email_exists = User.objects.filter(email=data['email']).exists()
        username_exists = User.objects.filter(
            username=data['username']
        ).exists()

        if email_exists and not username_exists:
            raise serializers.ValidationError(
                'Пользователь с таким email уже зарегистрирован.'
            )
        if username_exists and not email_exists:
            raise serializers.ValidationError(
                'Пользователь с таким username уже зарегистрирован.'
            )

        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True, max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise NotFound('Пользователь не найден.')

        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError('Неверный код подтверждения.')

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]
