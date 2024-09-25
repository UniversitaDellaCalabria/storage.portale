import datetime

from django.http import Http404
from structures.models import (
    DidatticaDipartimento,
    DidatticaDipartimentoUrl,
    UnitaOrganizzativa,
)


class ServiceStructure:
    @staticmethod
    def getStructureChilds(structureid=None):
        child = UnitaOrganizzativa.objects.filter(
            uo_padre=structureid, dt_fine_val__gte=datetime.datetime.today()
        ).values_list("uo", flat=True)
        result = [structureid]
        for c in child:
            structures_tree = ServiceStructure.getStructureChilds(c)
            result.extend(structures_tree)
        result.extend(child)
        return result


class ServiceDipartimento:
    @staticmethod
    def getDepartmentsList(language):
        query = DidatticaDipartimento.objects.all().values(
            "dip_id", "dip_cod", "dip_des_it", "dip_des_eng", "dip_nome_breve"
        )

        query = (
            query.order_by("dip_des_it")
            if language == "it"
            else query.order_by("dip_des_eng")
        )

        for q in query:
            url = DidatticaDipartimentoUrl.objects.filter(
                dip_cod=q["dip_cod"]
            ).values_list("dip_url", flat=True)
            q["dip_url"] = url[0] if url else ""

        return query

    @staticmethod
    def getDepartment(departmentcod):
        query = DidatticaDipartimento.objects.filter(
            dip_cod__exact=departmentcod
        ).values("dip_id", "dip_cod", "dip_des_it", "dip_des_eng", "dip_nome_breve")
        if not query:
            raise Http404
        dip_cod = query.first()["dip_cod"]
        url = DidatticaDipartimentoUrl.objects.filter(dip_cod=dip_cod).values_list(
            "dip_url", flat=True
        )
        for q in query:
            q["dip_url"] = url[0] if url else ""
        return query
