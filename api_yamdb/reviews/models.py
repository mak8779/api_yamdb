from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()

""" Для всех моделей надо добавить class Meta и в нем добавить сортировку.
Код стайл джанги такой, сначала идет класс Meta, а затем метод str
    class Meta:
        ...

    def __str__(self):
        ...  """


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(unique=True, max_length=50,
                            verbose_name='Slug категории')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(unique=True, max_length=50,
                            verbose_name='Slug жанра')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(max_length=256,
                            verbose_name='Название произведения')
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание группы')
    genre = models.ManyToManyField(Genre, through="GenreTitle")
    """ Тут лучше сделать PositiveSmallIntegerField
    Так как мы делаем поиск по году, чтобы его ускорить можно добавить индекс.
    https://ru.stackoverflow.com/questions/976248/django-db-index-in-field-%D1%87%D1%82%D0%BE-%D1%8D%D1%82%D0%BE-%D0%B8-%D0%B7%D0%B0%D1%87%D0%B5%D0%BC"""
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория произведения'
    )
    rating = models.IntegerField(default=0,
                                 verbose_name='Рейтинг произведения')  # Тут лучше сделать PositiveSmallIntegerField

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Связная таблица жанры-произведения."""

    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)  # Если добавить verbose_name  для каждого поля модели, то в админке будет удобнее управлять моделями. Они должны быть на русском языке.
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True)  # Если добавить verbose_name  для каждого поля модели, то в админке будет удобнее управлять моделями. Они должны быть на русском языке.

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )  # Если добавить verbose_name  для каждого поля модели, то в админке будет удобнее управлять моделями. Они должны быть на русском языке.
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(  # Тут лучше сделать PositiveSmallIntegerField
        validators=[MinValueValidator(1),  # Рекомендуется вынести цифры в константы и избегать использования "magic number". Константы выносим на уровень модуля. Константы должны быть в верхнем регистре.
                    MaxValueValidator(10)],  # Рекомендуется вынести цифры в константы и избегать использования "magic number". Константы выносим на уровень модуля. Константы должны быть в верхнем регистре.
        verbose_name='Оценка'
    )  
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['pub_date']
        unique_together = ('title', 'author')

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев к отзывам."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )  # Если добавить verbose_name  для каждого поля модели, то в админке будет удобнее управлять моделями. Они должны быть на русском языке.
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )  # Если добавить verbose_name  для каждого поля модели, то в админке будет удобнее управлять моделями. Они должны быть на русском языке.
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.text
