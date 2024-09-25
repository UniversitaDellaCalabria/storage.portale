from companies.models import (
    SpinoffStartupDatiBase,
    SpinoffStartupDipartimento,
    TipologiaAreaTecnologica,
)
from django.db.models import Q


class ServiceCompany:
    @staticmethod
    def getCompanies(
        search, techarea, spinoff, startup, q_departments, only_active=True
    ):
        query_search = Q()
        query_techarea = Q()
        query_spinoff = Q()
        query_startup = Q()
        query_is_active = Q(is_active=True) if only_active else Q()

        if search is not None:
            for k in search.split(" "):
                q_nome = Q(descrizione_ita__icontains=k) | Q(nome_azienda__icontains=k)
                query_search &= q_nome
        if techarea:
            query_techarea = Q(id_area_tecnologica=techarea)
        if spinoff:
            query_spinoff = Q(is_spinoff=spinoff)
        if startup:
            query_startup = Q(is_startup=startup)

        query = (
            SpinoffStartupDatiBase.objects.filter(
                query_search,
                query_techarea,
                query_spinoff,
                query_startup,
                query_is_active,
            )
            .values(
                "id",
                "piva",
                "nome_azienda",
                "nome_file_logo",
                "url_sito_web",
                "descrizione_ita",
                "descrizione_eng",
                "referente_unical",
                "matricola_referente_unical",
                "id_area_tecnologica",
                "id_area_tecnologica__descr_area_ita",
                "id_area_tecnologica__descr_area_eng",
                "is_startup",
                "is_spinoff",
                "is_active",
            )
            .distinct()
        )

        for q in query:
            departments = SpinoffStartupDipartimento.objects.filter(
                id_spinoff_startup_dati_base__exact=q["id"]
            ).values(
                "id_didattica_dipartimento__dip_cod",
                "id_didattica_dipartimento__dip_des_it",
                "id_didattica_dipartimento__dip_des_eng",
                "id_didattica_dipartimento__dip_nome_breve",
            )

            if len(departments) == 0:
                q["Departments"] = []
            else:
                q["Departments"] = departments

        if q_departments:
            dep = q_departments.split(",")
            final_query = []
            for q in query:
                for d in q["Departments"]:
                    if d["id_didattica_dipartimento__dip_cod"] in dep:
                        final_query.append(q)
            return final_query

        return query

    @staticmethod
    def getCompanyDetail(companyid):
        query = SpinoffStartupDatiBase.objects.filter(
            id=companyid, is_active=True
        ).values(
            "id",
            "piva",
            "nome_azienda",
            "nome_file_logo",
            "url_sito_web",
            "descrizione_ita",
            "descrizione_eng",
            "referente_unical",
            "matricola_referente_unical",
            "id_area_tecnologica",
            "id_area_tecnologica__descr_area_ita",
            "id_area_tecnologica__descr_area_eng",
            "is_startup",
            "is_spinoff",
            "is_active",
        )
        for q in query:
            departments = SpinoffStartupDipartimento.objects.filter(
                id_spinoff_startup_dati_base__exact=q["id"]
            ).values(
                "id_didattica_dipartimento__dip_cod",
                "id_didattica_dipartimento__dip_des_it",
                "id_didattica_dipartimento__dip_des_eng",
                "id_didattica_dipartimento__dip_nome_breve",
            )

            if len(departments) == 0:
                q["Departments"] = []
            else:
                q["Departments"] = departments

        return query

    @staticmethod
    def getTechAreas():
        query = TipologiaAreaTecnologica.objects.values(
            "id",
            "descr_area_ita",
            "descr_area_eng",
        ).distinct()

        return query
