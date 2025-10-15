import datetime
import operator
from functools import reduce

from addressbook.utils import append_email_addresses
from django.conf import settings
from django.core.exceptions import BadRequest
from django.db.models import Exists, F, OuterRef, Q
from django.http import Http404
from structures.models import DidatticaDipartimentoUrl

from cds.models import (
    DidatticaAttivitaFormativa,
    DidatticaAttivitaFormativaModalita,
    DidatticaCds,
    DidatticaCdsAltriDati,
    DidatticaCdsAltriDatiUfficio,
    DidatticaCdsCollegamento,
    DidatticaCdsGruppi,
    DidatticaCdsGruppiComponenti,
    DidatticaCdsLingua,
    DidatticaCdsPeriodi,
    DidatticaCopertura,
    DidatticaCoperturaDettaglioOre,
    DidatticaPdsRegolamento,
    DidatticaRegolamento,
    DidatticaRegolamentoAltriDati,
    DidatticaTestiAf,
    DidatticaTestiRegolamento,
)


def build_filter_chain(params_dict, query_params, *args):
    return reduce(
        operator.and_,
        [
            Q(**{v: query_params.get(k)})
            for (k, v) in params_dict.items()
            if query_params.get(k)
        ]
        + list(args),
        Q(),
    )


class ServiceDidatticaCds:
    @staticmethod
    def cdslist(language, query_params):
        didatticacds_params_to_query_field = {
            "courseclasscod": "cla_miur_cod",
            "courseclassname": "cla_miur_des__icontains",
            "cdscod": "cds_cod",
            # 'courseclassgroup': ... unspecified atm
            "departmentid": "dip__dip_id",
            "departmentcod": "dip__dip_cod",
            "departmentname": f"dip__dip_des_{language == 'it' and 'it' or 'eng'}__icontains",
            "area": "area_cds__icontains",
        }

        didatticaregolamento_params_to_query_field = {
            "academicyear": "didatticaregolamento__aa_reg_did__exact",
            "jointdegree": "didatticaregolamento__titolo_congiunto_cod",
            "regdid": "didatticaregolamento__regdid_id",
        }

        didatticacdslingua_params_to_query_field = {
            "cdslanguage": "didatticacdslingua__iso6392_cod",
        }

        search = query_params.get("search", None)
        if search is not None:
            search = search.split(" ")

        courses_allowed = query_params.get("coursetype", "")
        if courses_allowed != "":
            courses_allowed = courses_allowed.split(",")

        q1 = build_filter_chain(didatticacds_params_to_query_field, query_params)
        q2 = build_filter_chain(
            didatticaregolamento_params_to_query_field, query_params
        )
        q3 = build_filter_chain(didatticacdslingua_params_to_query_field, query_params)

        q4 = Q()

        if search is None:
            q4 = Q(cds_id__isnull=False)
        else:
            for k in search:
                if language == "it":
                    q = Q(nome_cds_it__icontains=k)
                else:
                    q = Q(nome_cds_eng__icontains=k)
                q4 |= q

        items = DidatticaCds.objects.filter(q4, q1, q2, q3)
        # didatticacdslingua__lin_did_ord_id__isnull=False

        if not query_params.get("academicyear", ""):
            items = items.filter(didatticaregolamento__stato_regdid_cod="A")

        if courses_allowed != "":
            items = items.filter(tipo_corso_cod__in=courses_allowed)

        items = items.values(
            "didatticaregolamento__regdid_id",
            "didatticaregolamento__aa_reg_did",
            "didatticaregolamento__frequenza_obbligatoria",
            "dip__dip_id",
            "dip__dip_cod",
            "dip__dip_des_it",
            "dip__dip_des_eng",
            "cds_id",
            "cds_cod",
            "cdsord_id",
            "nome_cds_it",
            "nome_cds_eng",
            "tipo_corso_cod",
            "tipo_corso_des",
            "cla_miur_cod",
            "cla_miur_des",
            "intercla_miur_cod",
            "intercla_miur_des",
            "durata_anni",
            "valore_min",
            "codicione",
            "didatticaregolamento__titolo_congiunto_cod",
            "didatticaregolamento__stato_regdid_cod",
            "area_cds",
            "area_cds_en",
        ).distinct()
        items = (
            items.order_by("nome_cds_it")
            if language == "it"
            else items.order_by(F("nome_cds_eng").asc(nulls_last=True))
        )
        for i in items:
            erogation_mode = DidatticaRegolamento.objects.filter(
                cds_id=i["cds_id"], stato_regdid_cod__exact="A"
            ).values("modalita_erogazione")
            if len(erogation_mode) != 0:
                i["ErogationMode"] = erogation_mode
            else:
                i["ErogationMode"] = None  # pragma: no cover

        items = list(items)
        for item in items:
            item["Languages"] = (
                DidatticaCdsLingua.objects.filter(cdsord_id=item["cdsord_id"])
                .values("lingua_des_it", "lingua_des_eng")
                .distinct()
            )

            item["OtherData"] = (
                DidatticaCdsAltriDati.objects.filter(
                    regdid_id=item["didatticaregolamento__regdid_id"]
                )
                .values(
                    # 'num_posti',
                    # 'modalita_iscrizione',
                    "manifesto_studi",
                    "regolamento_didattico",
                    "ordinamento_didattico",
                )
                .distinct()
            )

            # item['OfficesData'] = DidatticaCdsAltriDatiUfficio.objects.filter(cds_id=item['cds_id']).values(
            # 'ordine',
            # 'nome_ufficio',
            # 'matricola_riferimento',
            # 'nome_origine_riferimento',
            # 'telefono',
            # 'email',
            # 'edificio',
            # 'piano',
            # 'orari',
            # 'sportello_online'
            # ).distinct()

        return items

    @staticmethod
    def cds(language, cdsid_param, only_active=True):
        res = DidatticaCds.objects.filter(didatticaregolamento__regdid_id=cdsid_param)

        langs = res.prefetch_related("didatticacdslingua")

        res = res.values(
            "didatticaregolamento__regdid_id",
            "didatticaregolamento__aa_reg_did",
            "didatticaregolamento__frequenza_obbligatoria",
            "dip__dip_id",
            "dip__dip_cod",
            "dip__dip_des_it",
            "dip__dip_des_eng",
            "cds_id",
            "cds_cod",
            "cdsord_id",
            "nome_cds_it",
            "nome_cds_eng",
            "tipo_corso_cod",
            "tipo_corso_des",
            "cla_miur_cod",
            "cla_miur_des",
            "intercla_miur_cod",
            "intercla_miur_des",
            "durata_anni",
            "valore_min",
            "codicione",
            "didatticaregolamento__titolo_congiunto_cod",
            "didatticaregolamento__stato_regdid_cod",
            "area_cds",
            "area_cds_en",
        ).distinct()

        for r in res:
            erogation_mode = DidatticaRegolamento.objects.filter(
                cds_id=r["cds_id"], stato_regdid_cod__exact="A"
            ).values("modalita_erogazione")
            if len(erogation_mode) != 0:
                r["ErogationMode"] = erogation_mode
            else:
                r["ErogationMode"] = None

        res = list(res)

        if len(res) == 0:
            return None

        texts = DidatticaTestiRegolamento.objects.filter(regdid=cdsid_param).values(
            "regdid__regdid_id",
            "clob_txt_ita",
            "clob_txt_eng",
            "testo_regdid_url",
            "tipo_testo_regdid_cod",
            "profilo",
            "profilo_eng",
        )

        other_data = DidatticaRegolamentoAltriDati.objects.filter(
            regdid=cdsid_param
        ).values(
            "regdid__regdid_id", "clob_txt_ita", "clob_txt_eng", "tipo_testo_regdid_cod"
        )

        list_profiles = {}
        last_profile = ""

        res[0]["Languages"] = langs.values(
            "didatticacdslingua__lingua_des_it", "didatticacdslingua__lingua_des_eng"
        ).distinct()

        res[0]["URL_CDS_DOC"] = None
        res[0]["URL_CDS"] = None
        res[0]["INTRO_CDS_FMT"] = None
        res[0]["URL_CDS_VIDEO"] = None
        res[0]["DESC_COR_BRE"] = None
        res[0]["OBB_SPEC"] = None
        res[0]["REQ_ACC"] = None
        res[0]["REQ_ACC_2"] = None
        res[0]["PROFILO"] = None
        res[0]["PROVA_FINALE"] = None
        res[0]["PROVA_FINALE_2"] = None

        for text in texts:
            if (
                text["tipo_testo_regdid_cod"] != "FUNZIONI"
                and text["tipo_testo_regdid_cod"] != "COMPETENZE"
                and text["tipo_testo_regdid_cod"] != "SBOCCHI"
            ):
                if (
                    text["clob_txt_eng"] is None and language != "it"
                ) or language == "it":
                    res[0][text["tipo_testo_regdid_cod"]] = text["clob_txt_ita"]
                else:
                    res[0][text["tipo_testo_regdid_cod"]] = text["clob_txt_eng"]
            else:
                if (
                    language != "it" and text["profilo_eng"] is None
                ) or language == "it":
                    if text["profilo"] != last_profile:
                        last_profile = text["profilo"]
                        list_profiles[last_profile] = {}
                elif (
                    text[f"{language == 'it' and 'profilo' or 'profilo_eng'}"]
                    != last_profile
                ):  # pragma: no cover
                    last_profile = text[
                        f"{language == 'it' and 'profilo' or 'profilo_eng'}"
                    ]
                    list_profiles[last_profile] = {}

                if (
                    text["clob_txt_eng"] is None and language != "it"
                ) or language == "it":
                    list_profiles[last_profile][text["tipo_testo_regdid_cod"]] = text[
                        "clob_txt_ita"
                    ]
                else:
                    list_profiles[last_profile][text["tipo_testo_regdid_cod"]] = text[
                        "clob_txt_eng"
                    ]

        for od in other_data:
            if (od["clob_txt_eng"] is None and language != "it") or language == "it":
                res[0][od["tipo_testo_regdid_cod"]] = od["clob_txt_ita"]
            else:
                res[0][od["tipo_testo_regdid_cod"]] = od["clob_txt_eng"]

        res[0]["PROFILO"] = list_profiles

        res[0]["OtherData"] = (
            DidatticaCdsAltriDati.objects.filter(regdid_id=cdsid_param)
            .values(
                "matricola_coordinatore",
                "nome_origine_coordinatore",
                "matricola_coordinatore__email",
                "matricola_vice_coordinatore",
                "nome_origine_vice_coordinatore",
                "matricola_vice_coordinatore__email",
                # 'num_posti',
                # 'modalita_iscrizione',
                "manifesto_studi",
                "regolamento_didattico",
                "ordinamento_didattico",
            )
            .distinct()
        )

        res[0]["OfficesData"] = (
            DidatticaCdsAltriDatiUfficio.objects.filter(cds_id=res[0]["cds_id"])
            .values(
                "ordine",
                "nome_ufficio",
                "matricola_riferimento",
                "nome_origine_riferimento",
                "telefono",
                "email",
                "edificio",
                "piano",
                "orari",
                "sportello_online",
            )
            .distinct()
        )

        query_visibile = Q(visibile=True) if only_active else Q()
        res[0]["CdsGroups"] = (
            DidatticaCdsGruppi.objects.filter(
                query_visibile, didattica_cds=res[0]["cds_id"]
            )
            .values(
                "ordine",
                "id",
                "descr_breve_it",
                "descr_breve_en",
                "descr_lunga_it",
                "descr_lunga_en",
            )
            .distinct()
        )

        res[0]["CdsPeriods"] = DidatticaCdsPeriodi.objects.filter(
            cds_cod=res[0]["cds_cod"], aa_id=res[0]["didatticaregolamento__aa_reg_did"]
        ).values(
            "ciclo_des",
            "tipo_ciclo_des",
            "tipo_ciclo_des_eng",
            "data_inizio",
            "data_fine",
        )

        res[0]["CdsCurrentPeriods"] = DidatticaCdsPeriodi.objects.filter(
            cds_cod=res[0]["cds_cod"], aa_id=settings.CURRENT_YEAR
        ).values(
            "ciclo_des",
            "tipo_ciclo_des",
            "tipo_ciclo_des_eng",
            "data_inizio",
            "data_fine",
        )

        for group in res[0]["CdsGroups"]:
            members = (
                DidatticaCdsGruppiComponenti.objects.filter(
                    query_visibile, didattica_cds_gruppi=group["id"]
                )
                .values(
                    "ordine",
                    "id",
                    "matricola",
                    "cognome",
                    "nome",
                    "funzione_it",
                    "funzione_en",
                )
                .distinct()
            )
            group["members"] = members

        return res

    @staticmethod
    def getExpiredCds(yearfrom=None, coursetypes=None):
        query_year_from = Q()
        query_course_types = Q()
        if yearfrom is not None:
            try:
                validated_year_from = int(yearfrom)
                query_year_from = Q(aa_reg_did__gte=validated_year_from)
            except ValueError:
                raise BadRequest("Parameter yearfrom must be a valid year")
        if coursetypes is not None:
            course_tyeps_list = coursetypes.split(",")
            query_course_types = Q(cds__tipo_corso_cod__in=course_tyeps_list)

        cds_morphed = DidatticaCdsCollegamento.objects.values_list(
            "cds_prec__cds_cod", flat=True
        )

        regdids = (
            DidatticaRegolamento.objects.filter(
                # Ensure it's the record with the latest year
                ~Exists(
                    DidatticaRegolamento.objects.filter(
                        cds=OuterRef("cds"),
                        aa_reg_did__gt=OuterRef("aa_reg_did"),
                    ).exclude(stato_regdid_cod="R")
                ),
                query_year_from,
                query_course_types,
                aa_reg_did__lt=settings.CURRENT_YEAR,
            )
            .exclude(stato_regdid_cod="R")
            # exclude courses that have finished their regular life cycle
            .exclude(aa_reg_did__lte=(settings.CURRENT_YEAR - F("cds__durata_anni")))
            # exclude morphed courses
            .exclude(cds__cds_cod__in=cds_morphed)
            .values("aa_reg_did", "cds__cds_cod", "cds__durata_anni")
        )

        return regdids

    @staticmethod
    def getDegreeTypes():
        query = (
            DidatticaCds.objects.values("tipo_corso_cod", "tipo_corso_des")
            .order_by("tipo_corso_des")
            .distinct()
        )
        return query

    @staticmethod
    def getAcademicYears():
        query = (
            DidatticaRegolamento.objects.values("aa_reg_did")
            .order_by("-aa_reg_did")
            .distinct()
        )
        return query

    @staticmethod
    def getCdsAreas(language='en'):
        lookup = 'area_cds_en'
        if language == 'it':
            lookup = 'area_cds'
        query = DidatticaCds.objects\
                            .filter(**{f'{lookup}__isnull': False})\
                            .values(lookup)\
                            .order_by(lookup).distinct()
        return query

    @staticmethod
    def getContacts(cdscod):
        last_year = datetime.date.today().year - 1
        current_year = datetime.date.today().year
        years = [last_year, current_year]
        query = (
            DidatticaCopertura.objects.filter(
                Q(personale__flg_cessato=0, personale__fl_docente=1)
                | ~Q(stato_coper_cod="R"),
                cds_cod=cdscod,
                aa_off_id__in=years,
            )
            .values(
                "personale__nome",
                "personale__cognome",
                "personale__middle_name",
                "personale__matricola",
                "personale__cd_uo_aff_org",
                "personale__ds_aff_org",
            )
            .order_by("personale__cognome")
        )
        for q in query:
            q["DepartmentUrl"] = DidatticaDipartimentoUrl.objects.filter(
                dip_cod=q["personale__cd_uo_aff_org"]
            ).values("dip_url")
        return query

    @staticmethod
    def getPreviousSingleCdsCods(cds_cod):
        cds = DidatticaCds.objects.filter(cds_cod=cds_cod).order_by("-cds_id").first()
        if cds is None:
            raise Http404

        previous_cds_cod_list = []
        current_cds = cds
        while current_cds:
            try:
                collegamento = DidatticaCdsCollegamento.objects.get(cds=current_cds)
                predecessor = collegamento.cds_prec
                previous_cds_cod_list.append(predecessor.cds_cod)

                current_cds = predecessor
            except DidatticaCdsCollegamento.DoesNotExist:
                break

        return previous_cds_cod_list

    @staticmethod
    def _build_cds_history(cds_cod, history=[]):
        prec = DidatticaCdsCollegamento.objects.filter(cds__cds_cod=cds_cod).first()
        if prec:
            history.append(prec.cds_prec.cds_cod)
            ServiceDidatticaCds._build_cds_history(prec.cds_prec.cds_cod, history)
        return history

    @staticmethod
    def getPreviousCdsCods():
        previous_cds_cod_dict = {}
        cds_prec_ids = DidatticaCdsCollegamento.objects.values_list(
            "cds_prec", flat=True
        )
        roots = DidatticaCdsCollegamento.objects.exclude(cds__pk__in=cds_prec_ids)
        for root in roots:
            prec_list = ServiceDidatticaCds._build_cds_history(root.cds.cds_cod, [])
            previous_cds_cod_dict[root.cds.cds_cod] = prec_list
        return previous_cds_cod_dict


class ServiceDidatticaAttivitaFormativa:
    @staticmethod
    def getStudyPlans(regdid_id=None):
        query = DidatticaAttivitaFormativa.objects.filter(regdid=regdid_id)
        query = (
            query.order_by("pds_regdid_id__pds_des_it")
            .values(
                "regdid_id",
                "pds_regdid_id",
                "pds_cod",
                "pds_regdid_id__pds_des_it",
                "pds_regdid_id__pds_des_eng",
            )
            .distinct()
        )
        query = list(query)
        for q in query:
            activities = (
                ServiceDidatticaAttivitaFormativa.getAttivitaFormativaByStudyPlan(
                    q["pds_regdid_id"], group=True
                )
            )
            q["StudyActivities"] = activities  # list(activities)
        return query

    @staticmethod
    def getStudyPlan(studyplanid=None):
        query = DidatticaPdsRegolamento.objects.filter(pds_regdid_id=studyplanid)
        query = query.order_by("pds_des_it").values(
            "regdid__regdid_id", "pds_regdid_id", "pds_cod", "pds_des_it", "pds_des_eng"
        )
        query = list(query)
        for q in query:
            activities = (
                ServiceDidatticaAttivitaFormativa.getAttivitaFormativaByStudyPlan(
                    q["pds_regdid_id"], group=True
                )
            )
            q["StudyActivities"] = activities  # list(activities)
        return query

    @staticmethod
    def getAttivitaFormativaByStudyPlan(studyplanid, group=False):
        if group:
            total_years = (
                DidatticaPdsRegolamento.objects.filter(pds_regdid_id=studyplanid)
                .values("regdid__cds__durata_anni")
                .first()["regdid__cds__durata_anni"]
            )
            final_query = {}
            for i in range(total_years):
                query = DidatticaAttivitaFormativa.objects.filter(
                    pds_regdid__pds_regdid_id=studyplanid,
                    af_id__isnull=False,
                    anno_corso=(i + 1),
                )
                new_query = DidatticaAttivitaFormativa.objects.none()
                for q in query:
                    if q.checkIfMainCourse():
                        new_query = (
                            new_query
                            | DidatticaAttivitaFormativa.objects.filter(af_id=q.af_id)
                        )
                final_query[i + 1] = new_query.order_by("ciclo_des").values(
                    "af_id",
                    "af_gen_cod",
                    "des",
                    "af_gen_des_eng",
                    "cds__cds_id",
                    "cds__cds_cod",
                    "regdid__regdid_id",
                    "regdid__aa_reg_did",
                    "anno_corso",
                    "ciclo_des",
                    "peso",
                    "sett_cod",
                    "sett_des",
                    "freq_obblig_flg",
                    "cds__nome_cds_it",
                    "cds__nome_cds_eng",
                    "tipo_af_des",
                    "tipo_af_cod",
                    "tipo_af_intercla_cod",
                    "tipo_af_intercla_des",
                )
            return final_query
        else:
            query = DidatticaAttivitaFormativa.objects.filter(
                pds_regdid__pds_regdid_id=studyplanid, af_id__isnull=False
            )
            new_query = DidatticaAttivitaFormativa.objects.none()
            for q in query:
                if q.checkIfMainCourse():
                    new_query = new_query | DidatticaAttivitaFormativa.objects.filter(
                        af_id=q.af_id
                    )

            return new_query.order_by("anno_corso", "ciclo_des").values(
                "af_id",
                "af_gen_cod",
                "des",
                "af_gen_des_eng",
                "cds__cds_cod",
                "cds__cds_id",
                "regdid__regdid_id",
                "regdid__aa_reg_did",
                "anno_corso",
                "ciclo_des",
                "peso",
                "sett_cod",
                "sett_des",
                "freq_obblig_flg",
                "cds__nome_cds_it",
                "cds__nome_cds_eng",
                "tipo_af_des",
                "tipo_af_cod",
                "tipo_af_intercla_cod",
                "tipo_af_intercla_des",
            )

    @staticmethod
    def getAllActivities(
        language,
        department,
        cds,
        academic_year,
        period,
        ssd,
        teacher,
        teaching,
        course_year,
        cds_cod,
        teacher_code,
    ):
        query_department = Q()
        query_academic_year = Q()
        query_cds = Q()
        query_teacher = Q()
        query_teaching = Q()
        query_period = Q()
        query_ssd = Q()
        query_course_year = Q()
        query_cds_cod = Q()
        query_teacher_code = Q()

        if academic_year:
            query_academic_year = Q(aa_off_id=academic_year)
        if course_year:
            query_course_year = Q(anno_corso=course_year)
        if department:
            query_department = Q(cds_id__dip_id__dip_cod=department)
        if cds:
            if language == "it":  # pragma: no cover
                query_cds = Q(cds_id__nome_cds_it__icontains=cds)
            else:
                query_cds = Q(cds_id__nome_cds_eng__icontains=cds)
        # serve un collegamento tra didatticaattivitàformativa e personale con il campo matricola_resp_did
        if teacher:
            query_teacher = Q(matricola_resp_did__cognome__istartswith=teacher)
        if teaching:
            if language == "it":
                query_teaching = Q(des__icontains=teaching)
            else:
                query_teaching = Q(af_gen_des_eng__icontains=teaching)
        if ssd:
            for k in ssd.split(" "):
                q_ssd = Q(sett_cod__icontains=k)
                query_ssd &= q_ssd
        if period:
            query_period = Q(ciclo_des=period)

        if cds_cod:
            query_cds_cod = Q(cds_id__cds_cod__exact=cds_cod)

        if teacher_code:
            query_teacher_code = Q(personale_id__matricola__exact=teacher_code)

        coperture = (
            DidatticaCopertura.objects.filter(query_teacher_code)
            .exclude(stato_coper_cod="R")
            .values("af_id")
        )

        query_coperture = Q(af_id__in=coperture) | Q(af_master_id__in=coperture)

        query = (
            DidatticaAttivitaFormativa.objects.filter(
                query_department,
                query_academic_year,
                query_cds,
                query_period,
                query_ssd,
                query_teaching,
                query_course_year,
                query_coperture,
                query_teacher,
                query_cds_cod,
            )
            .values(
                "af_id",
                "af_gen_cod",
                "des",
                "af_gen_des_eng",
                "sett_cod",
                "sett_des",
                "ciclo_des",
                "lista_lin_did_af",
                "aa_off_id",
                "regdid_id",
                "cds_id",
                "cds_id__cds_cod",
                "cds_id__nome_cds_it",
                "cds_id__nome_cds_eng",
                "cds_id__dip_id__dip_cod",
                "cds_id__dip_id__dip_des_it",
                "cds_id__dip_id__dip_des_eng",
                "fat_part_stu_cod",
                "fat_part_stu_des",
                "part_stu_cod",
                "part_stu_des",
                "anno_corso",
                "matricola_resp_did",
                "matricola_resp_did__nome",
                "matricola_resp_did__cognome",
                "matricola_resp_did__middle_name",
                "pds_des",
                "af_master_id",
                "af_radice_id",
            )
            .distinct()
            .order_by("des")
        )

        radice_ids = set(obj["af_radice_id"] for obj in query if obj["af_radice_id"])
        radici = DidatticaAttivitaFormativa.objects.only("af_id", "des", "af_gen_des_eng").in_bulk(radice_ids)

        for q in query:
            if q["af_radice_id"]:
                q["Father"] = radici.get(q["af_radice_id"])
            else:
                q["Father"] = None

            if q["af_gen_cod"] is None:  # pragma: no cover
                codice = None
                codice = DidatticaCopertura.objects.filter(
                    af_id__exact=q["af_id"]
                ).values("af_gen_cod")

                codice = list(codice)
                if len(codice) > 0:
                    codice = codice[0]["af_gen_cod"]

                if codice:
                    q["af_gen_cod"] = codice
                else:
                    q["af_gen_cod"] = None

            if q["anno_corso"] is None:  # pragma: no cover
                anno = None
                anno = DidatticaCopertura.objects.filter(
                    af_id__exact=q["af_id"]
                ).values("anno_corso")

                anno = list(anno)

                if len(anno) > 0:
                    anno = anno[0]["anno_corso"]

                if anno:
                    q["anno_corso"] = anno
                else:
                    q["anno_corso"] = None

            if q["ciclo_des"] is None:  # pragma: no cover
                semestre = None
                semestre = DidatticaCopertura.objects.filter(
                    af_id__exact=q["af_id"]
                ).values("ciclo_des")

                semestre = list(semestre)

                if len(semestre) > 0:
                    semestre = semestre[0]["ciclo_des"]

                if semestre:
                    q["ciclo_des"] = semestre
                else:
                    q["ciclo_des"] = None

        # for q in query:
        #     padre = DidatticaAttivitaFormativa.objects.filter(af_id__exact=q['af_radice_id']).values(
        #     'des'
        #     )
        #
        #     if padre:
        #         q['Father'] = padre
        #     else:
        #         q['Father'] = None

        # for q in query:
        #
        #     name = Personale.objects.filter(matricola=q['matricola_resp_did']).values(
        #         'nome',
        #         'cognome',
        #         'middle_name'
        #     )
        #     if(len(name) != 0):
        #         q['DirectorName'] = name
        #     else:
        #         q['DirectorName'] = None

        return query

    @staticmethod
    def getAttivitaFormativaWithSubModules(af_id, language):
        list_submodules = (
            DidatticaAttivitaFormativa.objects.filter(
                Q(af_radice_id=af_id) | Q(af_pdr_id=af_id)
            )
            .exclude(af_id=af_id)
            .values(
                "af_id",
                "af_gen_cod",
                "des",
                "af_gen_des_eng",
                "fat_part_stu_cod",
                "lista_lin_did_af",
                "part_stu_cod",
                "part_stu_des",
                "fat_part_stu_des",
                "ciclo_des",
                "matricola_resp_did",
            )
        )

        query = (
            DidatticaAttivitaFormativa.objects.filter(af_id=af_id)
            .order_by("anno_corso", "ciclo_des")
            .values(
                "af_id",
                "af_gen_cod",
                "des",
                "af_gen_des_eng",
                "cds__cds_cod",
                "cds__cds_id",
                "lista_lin_did_af",
                "pds_cod",
                "pds_des",
                "regdid__regdid_id",
                "regdid__aa_reg_did",
                "anno_corso",
                "ciclo_des",
                "peso",
                "sett_cod",
                "sett_des",
                "freq_obblig_flg",
                "cds__nome_cds_it",
                "cds__nome_cds_eng",
                "tipo_af_des",
                "tipo_af_cod",
                "tipo_af_intercla_cod",
                "tipo_af_intercla_des",
                "matricola_resp_did",
                "mutuata_flg",
                "af_master_id",
                "af_radice_id",
                "af_pdr_id",
                "didatticacopertura__coper_peso",
                "part_stu_cod",
                "fat_part_stu_cod",
                "part_stu_des",
                "fat_part_stu_des",
            )
        )


        id_master = None
        mutuata_da = None
        if not query:
            raise Http404
        if query.first()["mutuata_flg"] == 1:
            id_master = query.first()["af_master_id"]
            mutuata_da = (
                DidatticaAttivitaFormativa.objects.filter(af_id=id_master)
                .values(
                    "af_id",
                    "af_gen_cod",
                    "des",
                    "cds__cds_cod",
                    "cds__cds_id",
                    "cds__nome_cds_it",
                    "cds__nome_cds_eng",
                    "pds_cod",
                    "pds_des",
                    "af_gen_des_eng",
                    "ciclo_des",
                    "regdid__regdid_id",
                    "regdid__aa_reg_did",
                    "anno_corso",
                    "didatticacopertura__coper_peso",
                )
                .first()
            )

        attivita_mutuate_da_questa = (
            DidatticaAttivitaFormativa.objects.filter(af_master_id=af_id, mutuata_flg=1)
            .exclude(af_id=af_id)
            .values(
                "af_id",
                "af_gen_cod",
                "des",
                "af_gen_des_eng",
                "ciclo_des",
                "regdid__regdid_id",
                "regdid__aa_reg_did",
                "anno_corso",
                "didatticacopertura__coper_peso",
                "cds__cds_cod",
                "cds__cds_id",
                "cds__nome_cds_it",
                "cds__nome_cds_eng",
                "pds_cod",
                "pds_des",
            )
        )
        radice = query.first()
        id_radice_padre = radice["af_pdr_id"]
        id_radice = radice["af_radice_id"]

        activity_root = (
            DidatticaAttivitaFormativa.objects.filter(af_id=id_radice)
            .exclude(af_id=af_id)
            .values(
                "af_id",
                "af_gen_cod",
                "des",
                "af_gen_des_eng",
                "ciclo_des",
                "regdid__regdid_id",
                "regdid__aa_reg_did",
                "anno_corso",
                "didatticacopertura__coper_peso",
                "cds__cds_cod",
                "cds__cds_id",
                "cds__nome_cds_it",
                "cds__nome_cds_eng",
                "pds_cod",
                "pds_des",
            )
        )
        if len(activity_root) == 0:
            activity_root = None
        else:
            activity_root = activity_root.first()

        activity_father = None

        if id_radice_padre and id_radice_padre != id_radice:  # pragma: no cover
            activity_father = (
                DidatticaAttivitaFormativa.objects.filter(af_id=id_radice_padre)
                .exclude(af_id=af_id)
                .values(
                    "af_id",
                    "af_gen_cod",
                    "des",
                    "af_gen_des_eng",
                    "ciclo_des",
                    "regdid__regdid_id",
                    "regdid__aa_reg_did",
                    "anno_corso",
                    "didatticacopertura__coper_peso",
                    "cds__cds_cod",
                    "cds__cds_id",
                    "cds__nome_cds_it",
                    "cds__nome_cds_eng",
                    "pds_cod",
                    "pds_des",
                )
            )
            if len(activity_father) == 0:
                activity_father = None
            else:
                activity_father = activity_father.first()

        DidatticaCopertura.objects.filter(af_id=af_id).values(
            "personale__id",
            "personale__id_ab",
            "personale__nome",
            "personale__cognome",
            "personale__middle_name",
            "personale__matricola",
            "fat_part_stu_cod",
            "fat_part_stu_des",
            "part_stu_cod",
            "part_stu_des",
        )

        query = list(query)

        filtered_hours = DidatticaCoperturaDettaglioOre.objects.filter(
            ~Q(coper_id__stato_coper_cod="R"), coper_id__af_id=af_id
        ).values(
            "tipo_att_did_cod",
            "ore",
            "coper_id__personale_id__id_ab",
            "coper_id__personale_id__matricola",
            "coper_id__personale_id__nome",
            "coper_id__personale_id__cognome",
            "coper_id__personale_id__middle_name",
            "coper_id__personale_id__flg_cessato",
            "coper_id",
        )

        append_email_addresses(filtered_hours, "coper_id__personale_id__id_ab")
        filtered_hours = list(filtered_hours)

        clean_list = []
        to_pass = []
        for index, hour in enumerate(filtered_hours):
            if index in to_pass:
                continue
            clean_list.append(hour)
            to_pass.append(index)
            for index2, hour2 in enumerate(filtered_hours):
                if index2 in to_pass:
                    continue
                c = clean_list[len(clean_list) - 1]
                if (
                    c["tipo_att_did_cod"] == hour2["tipo_att_did_cod"]
                    and c["coper_id__personale_id__matricola"]
                    and c["coper_id__personale_id__matricola"]
                    == hour2["coper_id__personale_id__matricola"]
                    and c["coper_id"] != hour2["coper_id"]
                ):  # pragma: no cover
                    c["ore"] = c["ore"] + hour2["ore"]
                    to_pass.append(index2)
        filtered_hours = clean_list

        query[0]["Hours"] = filtered_hours

        query[0]["Modalities"] = DidatticaAttivitaFormativaModalita.objects.filter(
            af_id=af_id
        ).values("mod_did_af_id", "mod_did_cod", "mod_did_des")

        query[0]["LANGUAGEIT"] = None
        query[0]["LANGUAGEEN"] = None

        # testi UGov riferiti all'insegnamento
        # carico didattico, materiale, ecc
        # dopo una modifica sul model,
        # la gestione tra i testi dell'insegnamento
        # e quelli dell'eventuale insegnamento che mutua quello attuale
        # (che prima avveniva da ETL) deve essere gestita qui.
        # I testi che non sono definiti devono essere recuperati
        # dall'eventuale insegnamento che mutua quello attuale
        texts_af = DidatticaTestiAf.objects.filter(
            af_id=af_id
        ).values(
            "tipo_testo_af_cod", "testo_af_ita", "testo_af_eng"
        )

        # dizionario mappatura
        dict_activity = {
            "CONTENUTI": "StudyActivityContent",
            "PROGR_EST": "StudyActivityProgram",
            "OBIETT_FORM": "StudyActivityLearningOutcomes",
            "METODI_DID": "StudyActivityMethodology",
            "MOD_VER_APPR": "StudyActivityEvaluation",
            "TESTI_RIF": "StudyActivityTextbooks",
            "STIMA_CAR_LAV": "StudyActivityWorkload",
            "PREREQ": "StudyActivityPrerequisites",
            "LINK_TEAMS": "StudyActivityElearningLink",
            "CODICE_TEAMS": "StudyActivityElearningInfo",
            "OB_SVIL_SOS": "StudyActivityDevelopmentGoal",
            "PROPEDE": None,
            "LINGUA_INS": None,
            "PAG_WEB_DOC": None,
            "ALTRO": None,
        }

        # se l'insegnamento è mutuato, recupero gli eventuali testi mancanti
        # dall'insegnamento principale
        if id_master and mutuata_da:
            existent_texts = texts_af.values_list('tipo_testo_af_cod', flat=True)
            missing_texts = dict_activity.keys() - existent_texts
            texts_master_af = DidatticaTestiAf.objects.filter(
                af_id=id_master,
                tipo_testo_af_cod__in=missing_texts
            ).values(
                "tipo_testo_af_cod", "testo_af_ita", "testo_af_eng"
            )
            texts_af = texts_af | texts_master_af
        # fine

        lingue = texts_af.filter(tipo_testo_af_cod="LINGUA_INS")

        for lingua in lingue:  # pragma: no cover
            query[0]["LANGUAGEIT"] = lingua["testo_af_ita"]
            query[0]["LANGUAGEEN"] = lingua["testo_af_eng"]

        query[0]["BorrowedFrom"] = mutuata_da
        query[0]["ActivitiesBorrowedFromThis"] = attivita_mutuate_da_questa

        query[0]["ActivityRoot"] = activity_root

        query[0]["ActivityFather"] = activity_father

        query[0]["StudyActivityTeacherID"] = None
        query[0]["StudyActivityTeacherName"] = None

        query[0]["PartitionCod"] = None
        query[0]["PartitionDescription"] = None
        query[0]["ExtendedPartitionCod"] = None
        query[0]["ExtendedPartitionDescription"] = None

        # for q in copertura:
        #     if q['personale__matricola'] == query[0]['matricola_resp_did']:
        #         query[0]['StudyActivityTeacherID'] = q['personale__matricola']
        #         if q['personale__cognome'] and q['personale__nome']:
        #             query[0]['StudyActivityTeacherName'] = f"{q['personale__cognome']} {q['personale__nome']}"
        #             if q['personale__middle_name']:
        #                 query[0]['StudyActivityTeacherName'] = f"{query[0]['StudyActivityTeacherName']} {q['personale__middle_name']}"
        #
        #         query[0]['PartitionCod'] = q['part_stu_cod']
        #         query[0]['PartitionDescription'] = q['part_stu_des']
        #         query[0]['ExtendedPartitionCod'] = q['fat_part_stu_cod']
        #         query[0]['ExtendedPartitionDescription'] = q['fat_part_stu_des']

        query[0]["MODULES"] = list()
        allowed = []
        for i in range(len(list_submodules)):
            (
                DidatticaCopertura.objects.filter(
                    af_id=list_submodules[i]["af_id"],
                    personale__matricola=list_submodules[i]["matricola_resp_did"],
                )
                .values(
                    "fat_part_stu_cod",
                    "fat_part_stu_des",
                    "part_stu_cod",
                    "part_stu_des",
                )
                .first()
            )

            groups = DidatticaAttivitaFormativa.objects.filter(
                af_pdr_id=list_submodules[i]["af_id"], fat_part_stu_cod="GRP"
            ).values(
                "af_id",
                "af_gen_cod",
                "des",
                "fat_part_stu_cod",
                "fat_part_stu_des",
                "part_stu_cod",
                "part_stu_des",
                "af_gen_des_eng",
            )

            groups_serialize = []
            for j in range(len(groups)):
                groups_serialize.append(
                    {
                        "StudyActivityID": groups[j]["af_id"],
                        "StudyActivityCod": groups[j]["af_gen_cod"],
                        "StudyActivityName": groups[j]["des"]
                        if language == "it" or groups[j]["af_gen_des_eng"] is None
                        else groups[j]["af_gen_des_eng"],
                        "StudyActivityPartitionCod": groups[j]["part_stu_cod"],
                        "StudyActivityPartitionDescription": groups[j]["part_stu_des"],
                        "StudyActivityExtendedPartitionCod": groups[j][
                            "fat_part_stu_cod"
                        ],
                        "StudyActivityExtendedPartitionDes": groups[j][
                            "fat_part_stu_des"
                        ],
                    }
                )
            groups = groups.values("af_id")
            groups = list(groups)
            for g in groups:
                allowed.append(g["af_id"])

            if list_submodules[i]["af_id"] not in allowed:
                query[0]["MODULES"].append(
                    {
                        "StudyActivityID": list_submodules[i]["af_id"],
                        "StudyActivityCod": list_submodules[i]["af_gen_cod"],
                        "StudyActivityName": list_submodules[i]["des"]
                        if language == "it"
                        or list_submodules[i]["af_gen_des_eng"] is None
                        else list_submodules[i]["af_gen_des_eng"],
                        "StudyActivitySemester": list_submodules[i]["ciclo_des"],
                        "StudyActivityPartitionCod": list_submodules[i]["part_stu_cod"],
                        "StudyActivityPartitionDescription": list_submodules[i][
                            "part_stu_des"
                        ],
                        "StudyActivityExtendedPartitionCod": list_submodules[i][
                            "fat_part_stu_cod"
                        ],
                        "StudyActivityExtendedPartitionDes": list_submodules[i][
                            "fat_part_stu_des"
                        ],
                        "StudyActivityGroups": groups_serialize,
                    }
                )
            elif (
                list_submodules[i]["af_id"] not in allowed
                and list_submodules[i]["fat_part_stu_cod"] == "GRP"
            ):  # pragma: no cover
                query[0]["MODULES"].append(
                    {
                        "StudyActivityID": list_submodules[i]["af_id"],
                        "StudyActivityCod": list_submodules[i]["af_gen_cod"],
                        "StudyActivityName": list_submodules[i]["des"]
                        if language == "it"
                        or list_submodules[i]["af_gen_des_eng"] is None
                        else list_submodules[i]["af_gen_des_eng"],
                        "StudyActivitySemester": list_submodules[i]["ciclo_des"],
                        "StudyActivityPartitionCod": list_submodules[i]["part_stu_cod"],
                        "StudyActivityPartitionDescription": list_submodules[i][
                            "part_stu_des"
                        ],
                        "StudyActivityExtendedPartitionCod": list_submodules[i][
                            "fat_part_stu_cod"
                        ],
                        "StudyActivityExtendedPartitionDes": list_submodules[i][
                            "fat_part_stu_des"
                        ],
                    }
                )

        query[0]["StudyActivityContent"] = None
        query[0]["StudyActivityProgram"] = None
        query[0]["StudyActivityLearningOutcomes"] = None
        query[0]["StudyActivityMethodology"] = None
        query[0]["StudyActivityEvaluation"] = None
        query[0]["StudyActivityTextbooks"] = None
        query[0]["StudyActivityWorkload"] = None
        query[0]["StudyActivityElearningLink"] = None
        query[0]["StudyActivityElearningInfo"] = None
        query[0]["StudyActivityPrerequisites"] = None
        query[0]["StudyActivityDevelopmentGoal"] = None

        for text in texts_af:
            query[0][dict_activity[text["tipo_testo_af_cod"]]] = (
                text["testo_af_ita"]
                if language == "it" or text["testo_af_eng"] is None
                else text["testo_af_eng"]
            )
        return query

    # @staticmethod
    # def getDocentiPerReg(regdid_id):
    #
    #     query = DidatticaAttivitaFormativa.objects.filter(
    #         didatticacopertura__personale__fl_docente=1,
    #         regdid__regdid_id=regdid_id,
    #         didatticacopertura__personale__isnull=False) .order_by(
    #         'didatticacopertura__personale__cd_ruolo',
    #         'didatticacopertura__personale__cognome',
    #         'didatticacopertura__personale__nome') .values(
    #         'didatticacopertura__personale__matricola',
    #         'didatticacopertura__personale__nome',
    #         'didatticacopertura__personale__cognome',
    #         'didatticacopertura__personale__middle_name',
    #         'didatticacopertura__personale__cd_ruolo',
    #         'didatticacopertura__personale__cd_ssd').distinct()
    #
    #     return query
