import csv
import json

from django.core.management.base import BaseCommand

from foodgram import settings
from recipes.models import *

BASE_DIR = settings.BASE_DIR + "/data/"

loader = {
    'json': (lambda f, _: json.load(f)),
    'csv': (lambda f, m: csv.DictReader(
        f=f,
        fieldnames=[
            f.name for f in m._meta.get_fields() if not f.auto_created
            ],
        delimiter=',')),
}


class Command(BaseCommand):
    help = 'Upload ingredients from csv'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)
        parser.add_argument('model', type=str)

    def handle(self, *args, **options):
        filename = options['filename']
        model = eval(options['model'])
        extension = filename.split('.')[-1]

        object_count = model.objects.count()

        with open(BASE_DIR + filename, encoding='utf-8') as f:
            data = loader[extension](f, model)

            model.objects.bulk_create(
                [model(**entry) for entry in data],
                ignore_conflicts=True,
                )

        return f"{model.objects.count() - object_count} objects loaded"
