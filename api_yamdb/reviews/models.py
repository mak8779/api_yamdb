from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()

MIN_SCORE = 1
MAX_SCORE = 10


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=50,
                            verbose_name='Slug')

    class Meta:
        ordering = ['id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=50,
                            verbose_name='Slug')

    class Meta:
        ordering = ['id']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(max_length=256,
                            verbose_name='Название')
    year = models.PositiveSmallIntegerField(verbose_name='Год выпуска',
                                            db_index=True)
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание группы')
    genre = models.ManyToManyField(Genre, through="GenreTitle")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    rating = models.PositiveSmallIntegerField(default=0,
                                              verbose_name='Рейтинг')

    class Meta:
        ordering = ['id']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Связная таблица жанры-произведения."""

    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL,
                              null=True, verbose_name='Жанр')
    title = models.ForeignKey(Title, on_delete=models.SET_NULL,
                              null=True, verbose_name='Произведение')

    class Meta:
        ordering = ['id']
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанр произведений'

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(MIN_SCORE),
                    MaxValueValidator(MAX_SCORE)],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['pub_date']
        unique_together = ('title', 'author')
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев к отзывам."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
