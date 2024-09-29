import csv
from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (Category, Genre, GenreTitle,
                            Title, User, Review, Comment)

IMPORT_CSV_FILES = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    User: 'users.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    """Команда менеджера для импорта базы из CSV."""

    help = 'Import CSV'

    def handle(self, *args, **kwargs):
        for model, file_csv in IMPORT_CSV_FILES.items():
            print(model, file_csv)
            with open(
                f'{settings.BASE_DIR}/static/data/{file_csv}',
                'r',
                encoding='utf-8'
            ) as f:
                reader = csv.DictReader(f)
                dump = [model(**row) for row in reader]
                print(dump)
                model.objects.bulk_create(dump)
            self.stdout.write(
                self.style.SUCCESS(f'Данные для {model.__name__} загружены')
            )
