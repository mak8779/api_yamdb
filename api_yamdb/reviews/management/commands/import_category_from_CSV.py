import csv
from django.conf import settings

from django.core.management.base import BaseCommand, CommandParser

from reviews.models import Category


class Command(BaseCommand):
    help = 'Import CSV'

    # def add_arguments(self, parser):
    #     parser.add_argument('category', nargs='?', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        #category = kwargs['category']
        with open('settings.BASE_DIR/static/data/category.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            Category.objects.bulk_create(Category(**row) for row in reader)
                # category = Category()
                # category.name = row[0]
                # category.slug = row[1]
                # category.save()
        self.stdout.write(self.style.SUCCESS('Все данные загружены'))
