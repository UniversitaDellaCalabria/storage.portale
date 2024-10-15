import base64

from django.core.cache import cache
from django.utils import timezone
from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework.schemas.openapi_agid import AgidAutoSchema
from rest_framework.views import APIView

# University Planner utils
from up.serializers import upImpegniSerializer
from up.services import getUPImpegni

from esse3.models import DidatticaAttivitaFormativaEsse3, DidatticaCdsEsse3

from .filters import CdsWebsiteTimetableFilter
from .serializers import esse3AppelliSerializer
from .services import getEsse3Appelli


class ApiCdsWebsiteTimetable(APIView):  # pragma: no cover
    description = "Retrieves the timetable for a course of study."
    filter_backends = [CdsWebsiteTimetableFilter]
    allowed_methods = ("GET",)
    schema = AgidAutoSchema(tags=["public"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event_types = ["AD"]
        self.language = None

    def get(self, obj, **kwargs):
        if not self.language:
            lang = self.request.LANGUAGE_CODE
            self.language = self.request.query_params.get("lang", lang).lower()
        cds_cod = self.kwargs["cds_cod"]
        current_year = timezone.localtime(
            timezone.now().replace(tzinfo=timezone.utc)
        ).year
        academic_year = self.request.query_params.get("academic_year", current_year)
        try:
            year = int(self.request.query_params.get("year"))
        except Exception:
            year = 1
        # cds = ServiceDidatticaCds.getCdsWebsite(cds_cod)
        date_month = self.request.query_params.get("date_month", "")
        date_year = self.request.query_params.get("date_year", "")
        af_name = self.request.query_params.get("af_name", "")
        af_cod = self.request.query_params.get("af_cod", "")
        search_teacher = self.request.query_params.get("search_teacher", "")
        search_location = self.request.query_params.get("search_location", "")
        show_past = self.request.query_params.get("show_past", "true")
        show_past = 0 if show_past == "false" else 1

        search = {"search_teacher": search_teacher, "search_location": search_location}

        search_key = base64.b64encode(str(search).encode())
        # if cds:
        cache_key = f"cdswebsite_timetable_{cds_cod}_{academic_year}_{year}_{date_month}_{date_year}_{slugify(self.event_types)}_{af_cod}_{search_key.decode()}_{show_past}"
        if not cache.get(cache_key):
            impegni = getUPImpegni(
                request=self.request,
                aa=academic_year,
                year=year,
                date_month=date_month,
                date_year=date_year,
                cds_cod=cds_cod,
                types=self.event_types,
                af_cod=af_cod,
                filter_by_af_cod="ES" not in self.event_types,
            )
            impegni_json = upImpegniSerializer(
                impegni=impegni,
                year=year,
                af_name=af_name,
                af_cod=af_cod,
                search=search,
                show_past=show_past,
                lang=self.language,
            )

            # if Exams, search in Esse3 too
            if "ES" in self.event_types and af_cod:
                cds_id = DidatticaCdsEsse3.objects.get(cds_cod=cds_cod).cds_id_esse3
                af_esse3 = DidatticaAttivitaFormativaEsse3.objects.filter(
                    ad_cod=af_cod
                ).first()
                if af_esse3:
                    af_id = af_esse3.ad_id_esse3

                    appelli_esse3 = getEsse3Appelli(
                        request=self.request,
                        cds_id=cds_id,
                        af_id=af_id,
                        aa=academic_year,
                    )
                    appelli_esse3_json = esse3AppelliSerializer(
                        appelli=appelli_esse3, show_past=show_past
                    )

                    duplicates_to_remove = []
                    for iu in impegni_json:
                        for ae3 in appelli_esse3_json:
                            if (
                                ae3["dataInizio"] == iu["dataInizio"]
                                and ae3["orarioInizio"] == iu["orarioInizio"]
                            ):
                                if not ae3["aula"]:
                                    ae3["aula"] = iu["aula"]
                                duplicates_to_remove.append(iu)
                                break

                    for delete in duplicates_to_remove:
                        impegni_json.remove(delete)

                    all_events = impegni_json + appelli_esse3_json
                    impegni_json = sorted(
                        all_events, key=lambda x: (x["dataInizio"], x["orarioInizio"])
                    )
            cache.set(cache_key, impegni_json)

        return Response(cache.get(cache_key))


class ApiCdsWebsiteExams(ApiCdsWebsiteTimetable):  # pragma: no cover
    description = "Retrieves the exams calendar for a course of study."
    allowed_methods = ("GET",)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event_types = ["ES"]
