from django.contrib import admin
from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment

from api.models import User

admin.site.register(User)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category', 'description')
    search_fields = ('name', 'year')
    list_filter = ('year', 'category', 'genre')
    filter_horizontal = ('genre',)
    raw_id_fields = ('category',)


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('genre', 'title')
    search_fields = ('genre__name', 'title__name')
    list_filter = ('genre', 'title')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'score', 'pub_date')
    search_fields = ('author__username', 'title__name', 'text')
    list_filter = ('score', 'pub_date', 'title')
    raw_id_fields = ('author', 'title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'review', 'pub_date', 'text')
    search_fields = ('author__username', 'review__title__name', 'text')
    list_filter = ('pub_date', 'review')
    raw_id_fields = ('author', 'review')


admin.site.site_title = 'Администрирование YaMDb'
admin.site.site_header = 'Администрирование YaMDb'
