import csv
import codecs

from django.http import HttpResponse


def convert_to_csv(data, fields):

    response = HttpResponse(content_type="text/csv")
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    writer.writerow(fields)

    for obj in data:
        writer.writerow([obj[field] for field in fields])

    return response
