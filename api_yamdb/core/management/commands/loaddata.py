import os

from django.core.management.base import BaseCommand
from django.conf import settings
import csv

from api.serializers import UserSerializer


class Command(BaseCommand):
    help = 'Load data from csv to db'

    DATA_SERIALIZERS = {
        'category.csv': ('CategorySerializer', 'category'),
        'comments.csv': ('CategorySerializer', 'comment'),
        'genre.csv': ('CategorySerializer', 'genre'),
        'genre_title.csv': ('CategorySerializer', 'genre_title'),
        'review.csv': ('CategorySerializer', 'review'),
        'titles.csv': ('CategorySerializer', 'title'),
        'users.csv': (UserSerializer, 'user'),
    }

    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='+', type=str)

    def handle(self, *args, **options):
        file_names = options['file_name']

        for name in file_names:
            path = os.path.join(settings.BASE_DIR, 'static/data/', name)

            with open(path, newline='') as csvfile:
                data = csv.DictReader(csvfile)

                for each in data:
                    serializer_class, data_name = (
                        self.DATA_SERIALIZERS[name]
                    )

                    serializer = serializer_class(data=each)

                    if serializer.is_valid():
                        serializer.save()
                        self.stdout.write(
                            self.style.SUCCESS(
                                'Successfully added {} {}'.format(
                                    data_name,
                                    serializer.data
                                )
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(serializer.errors)
                        )
