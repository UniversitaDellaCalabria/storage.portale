import csv
import os

from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ricerca_app.models import DidatticaCds

from . settings import PENTAHO_ISODID_MEDIA_PATH
from . utils import *


PENTAHO_ISODID_MEDIA_PATH = getattr(settings, 'PENTAHO_ISODID_MEDIA_PATH', PENTAHO_ISODID_MEDIA_PATH)
PENTAHO_ISODID_REPORT_START_YEAR = getattr(settings, 'PENTAHO_ISODID_REPORT_START_YEAR', PENTAHO_ISODID_REPORT_START_YEAR)


class PentahoIsodid(APIView): # pragma: no cover
    allowed_methods = ('GET',)

    def get(self, obj, **kwargs):
        request = self.request

        cdscod = kwargs.get('cdscod')
        # check if cdscod is existent
        cds = DidatticaCds.objects.filter(cds_cod=cdscod)
        if not cds.exists():
            return Response("Wrong degree course code", status=status.HTTP_404_NOT_FOUND)

        # check year
        year = request.query_params.get('year')
        if not year:
            year = 2023
        else:
            if not year.isnumeric():
                return Response("Wrong year", status=status.HTTP_400_BAD_REQUEST)
            if not int(year) in range(PENTAHO_ISODID_REPORT_START_YEAR, settings.CURRENT_YEAR + 1):
                return Response(f"Year must be in ({PENTAHO_ISODID_REPORT_START_YEAR},{settings.CURRENT_YEAR + 1}) range", status=status.HTTP_400_BAD_REQUEST)
        filename = f'{PENTAHO_ISODID_MEDIA_PATH}{year}/{cdscod}.csv'
        # filename = f'/home/francesco/Scrivania/isodid_csv/{year}/{cdscod}.csv'
        result = {}
        labels = []
        try:
            if not os.path.isfile(filename):
                getIsodidReport([cdscod],[year])
            with open(filename, newline='') as csvfile:
                index = 0
                reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in reader:
                    if not index:
                        labels = [row[2], row[3], row[4]]
                        index += 1
                        continue
                    if not row[0]:
                        return Response({})
                    if row[0] not in result:
                        data_labels = [row[1]]
                        data = {labels[0]: [row[2] or '0'],
                                labels[1]: [row[3] or '0'],
                                labels[2]: [row[4] or '0']}
                        result[row[0]] = {'labels': data_labels,
                                          'data': data}
                    else:
                        result[row[0]]['labels'].append(row[1])
                        result[row[0]]['data'][labels[0]].append(row[2] or '0')
                        result[row[0]]['data'][labels[1]].append(row[3] or '0')
                        result[row[0]]['data'][labels[2]].append(row[4] or '0')
                    index = index + 1
            return Response({"data": result})
        except FileNotFoundError as fnfe:
            return Response("Bad request parameters", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Server error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
