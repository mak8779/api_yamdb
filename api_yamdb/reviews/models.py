from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(unique=True, max_length=50,
                            verbose_name='Slug категории')

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(unique=True, max_length=50,
                            verbose_name='Slug жанра')

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
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория произведения'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Связная таблица жанры-произведения."""
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.genre} {self.title}'
