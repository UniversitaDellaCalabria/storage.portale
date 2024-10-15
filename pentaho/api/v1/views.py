import csv
import os

from cds.models import DidatticaCds
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.schemas.openapi_agid import AgidAutoSchema
from rest_framework.views import APIView

from pentaho.settings import (
    PENTAHO_ISODID_MEDIA_PATH,
    PENTAHO_ISODID_REPORT_LEGENDA,
    PENTAHO_ISODID_REPORT_START_YEAR,
)
from pentaho.utils import getIsodidReport

from .filters import PentahoIsodidFilter

PENTAHO_ISODID_MEDIA_PATH = getattr(
    settings, "PENTAHO_ISODID_MEDIA_PATH", PENTAHO_ISODID_MEDIA_PATH
)
PENTAHO_ISODID_REPORT_LEGENDA = getattr(
    settings, "PENTAHO_ISODID_REPORT_LEGENDA", PENTAHO_ISODID_REPORT_LEGENDA
)
PENTAHO_ISODID_REPORT_START_YEAR = getattr(
    settings, "PENTAHO_ISODID_REPORT_START_YEAR", PENTAHO_ISODID_REPORT_START_YEAR
)


class ApiPentahoIsodid(APIView):  # pragma: no cover
    filter_backends = [PentahoIsodidFilter]
    allowed_methods = ("GET",)
    schema = AgidAutoSchema(tags=["public"])

    def get(self, obj, **kwargs):
        request = self.request

        cdscod = kwargs.get("cdscod")
        # check if cdscod is existent
        cds = DidatticaCds.objects.filter(cds_cod=cdscod)
        if not cds.exists():
            return Response(
                "Wrong degree course code", status=status.HTTP_404_NOT_FOUND
            )

        # check year
        year = request.query_params.get("year")
        if not year:
            year = settings.CURRENT_YEAR
        else:
            if not year.isnumeric():
                return Response("Wrong year", status=status.HTTP_400_BAD_REQUEST)
            if int(year) not in range(
                PENTAHO_ISODID_REPORT_START_YEAR, settings.CURRENT_YEAR + 1
            ):
                return Response(
                    f"Year must be in ({PENTAHO_ISODID_REPORT_START_YEAR},{settings.CURRENT_YEAR + 1}) range",
                    status=status.HTTP_400_BAD_REQUEST,
                )
        filename = f"{PENTAHO_ISODID_MEDIA_PATH}{year}/{cdscod}.csv"
        # filename = f'/home/francesco/Scrivania/isodid_csv/{year}/{cdscod}.csv'
        result = {}
        labels = []
        try:
            if not os.path.isfile(filename):
                getIsodidReport([cdscod], [year])
            with open(filename, newline="") as csvfile:
                index = 0
                reader = csv.reader(csvfile, delimiter=",", quotechar="|")
                for row in reader:
                    if not index:
                        labels = [row[2], row[3], row[4]]
                        index += 1
                        continue
                    if not row[0]:
                        return Response({})
                    if row[0] not in result:
                        data_labels = [row[1]]
                        legenda = {}
                        legenda[row[1]] = PENTAHO_ISODID_REPORT_LEGENDA.get(
                            row[1], row[1]
                        )
                        data = {
                            labels[0]: [row[2] or "0"],
                            labels[1]: [row[3] or "0"],
                            labels[2]: [row[4] or "0"],
                        }
                        result[row[0]] = {
                            "labels": data_labels,
                            "data": data,
                            "legenda": legenda,
                        }
                    else:
                        result[row[0]]["legenda"][row[1]] = (
                            PENTAHO_ISODID_REPORT_LEGENDA.get(row[1], row[1])
                        )
                        result[row[0]]["labels"].append(row[1])
                        result[row[0]]["data"][labels[0]].append(row[2] or "0")
                        result[row[0]]["data"][labels[1]].append(row[3] or "0")
                        result[row[0]]["data"][labels[2]].append(row[4] or "0")
                    index = index + 1
            return Response({"data": result})
        except FileNotFoundError:
            return Response(
                "Bad request parameters", status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            return Response(
                "Server error", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )