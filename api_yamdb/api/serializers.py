import datetime

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title, Review, Comment

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
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'rating')
        model = Title


class TitleViewSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра списка произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'rating')
        model = Title


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Недопустимые символы в username. Разрешены только буквы, цифры и символы @/./+/-/_'
        )]
    )

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
    """Сериализатор для получения JWT токена."""

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
    """Сериализатор для модели пользователя."""

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
    """Сериализатор для текущего пользователя."""

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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    def validate(self, data):
        """Запрещаем оставлять более одного отзыва на произведение."""
        if self.context['request'].method == 'POST' and Review.objects.filter(
                title=self.context['view'].kwargs['title_id'], author=self.context['request'].user).exists():
            raise ValidationError('Вы уже оставили отзыв на это произведение.')
        return data

    def create(self, validated_data):
        """При создании отзыва обновляем рейтинг произведения."""
        review = super().create(validated_data)
        self.update_title_rating(review.title)
        return review

    def update(self, instance, validated_data):
        """При обновлении отзыва обновляем рейтинг произведения."""
        review = super().update(instance, validated_data)
        self.update_title_rating(review.title)
        return review

    def update_title_rating(self, title):
        """Обновление среднего рейтинга произведения."""
        reviews = title.reviews.all()
        rating = sum([review.score for review in reviews]) / reviews.count()
        title.rating = rating
        title.save()

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментариев."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
