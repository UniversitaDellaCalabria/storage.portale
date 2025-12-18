import datetime

from addressbook.models import Personale
from addressbook.settings import (
    PERSON_CONTACTS_EXCLUDE_STRINGS,
    PERSON_CONTACTS_TO_TAKE,
)
from addressbook.utils import append_email_addresses, get_personale_matricola
from cds.models import DidatticaCopertura
from django.db.models import Q
from django.http import Http404
from research_groups.models import RicercaDocenteGruppo, RicercaGruppo
from research_lines.models import (
    RicercaDocenteLineaApplicata,
    RicercaDocenteLineaBase,
    RicercaLineaApplicata,
    RicercaLineaBase,
)
from structures.models import DidatticaDipartimento, UnitaOrganizzativaFunzioni
from teachers.models import (
    DocenteMaterialeDidattico,
    DocentePtaAltriDati,
    DocentePtaBacheca,
    PubblicazioneAutori,
    PubblicazioneCommunity,
    PubblicazioneDatiBase,
)
import teachers.utils


class ServiceDocente:
    # @staticmethod
    # def getResearchGroups(teacher_id):
    #
    #     query = Personale.objects.filter(
    #         matricola__exact=teacher_id,
    #         fl_docente=1,
    #         ricercadocentegruppo__dt_fine__isnull=True) .order_by('ricercadocentegruppo__ricerca_gruppo__nome') .values(
    #         'ricercadocentegruppo__ricerca_gruppo__id',
    #         'ricercadocentegruppo__ricerca_gruppo__nome',
    #         'ricercadocentegruppo__ricerca_gruppo__descrizione').distinct()
    #
    #     return query

    @staticmethod
    def getAllResearchGroups(search, teacher, department, cod):
        if teacher:
            teacher = get_personale_matricola(teacher)

        query_search = Q()
        query_cod = Q()

        if search is not None:
            for k in search.split(" "):
                q_nome = (
                    Q(nome__icontains=k)
                    | Q(descrizione__icontains=k)
                    | Q(ricerca_erc1_id__descrizione__icontains=k)
                    | Q(ricercadocentegruppo__personale_id__cognome__istartswith=k)
                )
                query_search &= q_nome

        if cod:
            cod = cod.split(",")
            query_cod = Q(ricerca_erc1_id__cod_erc1__in=cod)

        query = (
            RicercaGruppo.objects.filter(query_search, query_cod)
            .order_by("nome")
            .values(
                "id",
                "nome",
                "descrizione",
                "ricerca_erc1_id__cod_erc1",
                "ricerca_erc1_id__descrizione",
            )
            .distinct()
        )

        if teacher is not None or department is not None:
            res = []
            for q in query:
                teachers = RicercaDocenteGruppo.objects.filter(
                    ricerca_gruppo_id=q["id"]
                ).values(
                    "personale_id__matricola",
                    "personale_id__nome",
                    "personale_id__middle_name",
                    "personale_id__cognome",
                    "personale_id__ds_sede",
                    "personale_id__sede",
                )

                q["Teachers"] = None
                if department is None:
                    for t in teachers:
                        if t["personale_id__matricola"] == teacher:
                            q["Teachers"] = teachers
                    if q["Teachers"] is not None:
                        res.append(q)
                if teacher is None:
                    for t in teachers:
                        if t["personale_id__sede"] == department:
                            q["Teachers"] = teachers

                    if q["Teachers"] is not None:
                        res.append(q)
                else:
                    for t in teachers:
                        if (
                            t["personale_id__sede"] == department
                            and t["personale_id__matricola"] == teacher
                        ):
                            q["Teachers"] = teachers

                    if q["Teachers"] is not None:
                        res.append(q)
            # eliminazione duplicati di res
            res = [i for n, i in enumerate(res) if i not in res[n + 1:]]
            return res

        else:
            for q in query:
                teachers = RicercaDocenteGruppo.objects.filter(
                    ricerca_gruppo_id=q["id"]
                ).values(
                    "personale_id__matricola",
                    "personale_id__nome",
                    "personale_id__middle_name",
                    "personale_id__cognome",
                    "personale_id__ds_sede",
                    "personale_id__sede",
                )

                if len(teachers) == 0:
                    q["Teachers"] = []
                else:
                    q["Teachers"] = teachers

            return query

    @staticmethod
    def getResearchLines(teacher_id, only_active=True):
        teacher_id = get_personale_matricola(teacher_id)

        query_is_active_app = (
            Q(ricercadocentelineaapplicata__ricerca_linea_applicata__visibile=True)
            if only_active
            else Q()
        )
        query_is_active_base = (
            Q(ricercadocentelineabase__ricerca_linea_base__visibile=True)
            if only_active
            else Q()
        )

        linea_applicata = (
            Personale.objects.filter(
                query_is_active_app,
                matricola__exact=teacher_id,
                fl_docente=1,
                ricercadocentelineaapplicata__dt_fine__isnull=True,
            )
            .order_by("ricercadocentelineaapplicata__ricerca_linea_applicata__id")
            .values(
                "ricercadocentelineaapplicata__ricerca_linea_applicata__id",
                "ricercadocentelineaapplicata__ricerca_linea_applicata__descrizione",
                "ricercadocentelineaapplicata__ricerca_linea_applicata__descr_pubblicaz_prog_brevetto",
                "ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__erc0_cod",
                "ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__description",
            )
            .distinct()
        )

        linea_base = (
            Personale.objects.filter(
                query_is_active_base,
                matricola__exact=teacher_id,
                fl_docente=1,
                ricercadocentelineabase__dt_fine__isnull=True,
            )
            .order_by("ricercadocentelineabase__ricerca_linea_base__id")
            .values(
                "ricercadocentelineabase__ricerca_linea_base__id",
                "ricercadocentelineabase__ricerca_linea_base__descrizione",
                "ricercadocentelineabase__ricerca_linea_base__descr_pubblicaz_prog_brevetto",
                "ricercadocentelineabase__ricerca_linea_base__ricerca_erc2__ricerca_erc1__ricerca_erc0_cod__erc0_cod",
                "ricercadocentelineabase__ricerca_linea_base__ricerca_erc2__ricerca_erc1__ricerca_erc0_cod__description",
            )
            .distinct()
        )

        linea_applicata = list(linea_applicata)
        for linea in linea_applicata:
            linea["Tipologia"] = "applicata"
        linea_base = list(linea_base)
        for linea in linea_base:
            linea["Tipologia"] = "base"

        for lb in linea_base:
            if lb["ricercadocentelineabase__ricerca_linea_base__id"] is None:
                linea_base.remove(lb)

        for la in linea_applicata:
            if la["ricercadocentelineaapplicata__ricerca_linea_applicata__id"] is None:
                linea_applicata.remove(la)

        linea_applicata.extend(linea_base)

        return linea_applicata

    @staticmethod
    def getAllResearchLines(
        search,
        year,
        department,
        ercs,
        asters,
        exclude_base=False,
        exclude_applied=False,
        only_active=True,
    ):
        if exclude_applied and exclude_base:
            return []

        query_search = Q()
        query_year = Q()
        query_ercs = Q()
        query_asters = Q()
        query_is_active = Q(visibile=True) if only_active else Q()

        if search:
            for k in search.split(" "):
                q_descrizione = Q(descrizione__icontains=k)
                query_search &= q_descrizione
        if year:
            query_year = Q(anno=year)
        if ercs:
            ercs = ercs.split(",")
            query_ercs = Q(ricerca_erc2_id__ricerca_erc1_id__cod_erc1__in=ercs)

        if asters:
            asters = asters.split(",")
            query_asters = Q(ricerca_aster2_id__ricerca_aster1_id__in=asters)

        linea_base = []
        linea_applicata = []

        if not exclude_base:
            linea_base = (
                RicercaLineaBase.objects.filter(
                    query_search, query_year, query_ercs, query_is_active
                )
                .order_by("descrizione")
                .values(
                    "id",
                    "descrizione",
                    "descr_pubblicaz_prog_brevetto",
                    "anno",
                    "ricerca_erc2_id__cod_erc2",
                    "ricerca_erc2_id__descrizione",
                    "ricerca_erc2_id__ricerca_erc1_id__cod_erc1",
                    "ricerca_erc2_id__ricerca_erc1_id__descrizione",
                    "ricerca_erc2_id__ricerca_erc1_id__ricerca_erc0_cod__erc0_cod",
                    "ricerca_erc2_id__ricerca_erc1_id__ricerca_erc0_cod__description",
                    "ricerca_erc2_id__ricerca_erc1_id__ricerca_erc0_cod__description_en",
                    "visibile",
                )
                .distinct()
            )

        if not exclude_applied:
            linea_applicata = (
                RicercaLineaApplicata.objects.filter(
                    query_search, query_year, query_asters, query_is_active
                )
                .order_by("descrizione")
                .values(
                    "id",
                    "descrizione",
                    "descr_pubblicaz_prog_brevetto",
                    "anno",
                    "ricerca_aster2_id__ricerca_aster1_id",
                    "ricerca_aster2_id__descrizione",
                    "visibile",
                )
                .distinct()
            )

        if ercs and asters:
            pass

        elif ercs:
            linea_applicata = []

        elif asters:
            linea_base = []

        for q in linea_base:
            teachers = RicercaDocenteLineaBase.objects.filter(
                ricerca_linea_base_id=q["id"]
            ).values(
                "personale_id__matricola",
                "personale_id__nome",
                "personale_id__middle_name",
                "personale_id__cognome",
                "personale_id__ds_sede",
                "personale_id__sede",
                "personale_id__flg_cessato",
            )

            if len(teachers) == 0:
                q["Teachers"] = []
            else:
                q["Teachers"] = teachers

        for q in linea_applicata:
            teachers = RicercaDocenteLineaApplicata.objects.filter(
                ricerca_linea_applicata_id=q["id"]
            ).values(
                "personale_id__matricola",
                "personale_id__nome",
                "personale_id__middle_name",
                "personale_id__cognome",
                "personale_id__ds_sede",
                "personale_id__sede",
                "personale_id__flg_cessato",
            )

            if len(teachers) == 0:
                q["Teachers"] = []
            else:
                q["Teachers"] = teachers

        linea_applicata = list(linea_applicata)
        for linea in linea_applicata:
            linea["Tipologia"] = "applicata"

        linea_base = list(linea_base)
        for linea in linea_base:
            linea["Tipologia"] = "base"

        if department is not None:
            res = []
            for q in linea_base:
                teachers = RicercaDocenteLineaBase.objects.filter(
                    ricerca_linea_base_id=q["id"]
                ).values(
                    "personale_id__matricola",
                    "personale_id__nome",
                    "personale_id__middle_name",
                    "personale_id__cognome",
                    "personale_id__ds_sede",
                    "personale_id__sede",
                    "personale_id__flg_cessato",
                )

                q["Teachers"] = None

                for t in teachers:
                    if t["personale_id__sede"] == department:
                        q["Teachers"] = teachers

                if q["Teachers"] is not None:
                    res.append(q)

            for q in linea_applicata:
                teachers = RicercaDocenteLineaApplicata.objects.filter(
                    ricerca_linea_applicata_id=q["id"]
                ).values(
                    "personale_id__matricola",
                    "personale_id__nome",
                    "personale_id__middle_name",
                    "personale_id__cognome",
                    "personale_id__ds_sede",
                    "personale_id__sede",
                    "personale_id__flg_cessato",
                )

                q["Teachers"] = None

                for t in teachers:
                    if t["personale_id__sede"] == department:
                        q["Teachers"] = teachers

                if q["Teachers"] is not None:
                    res.append(q)

            return res

        linea_applicata.extend(linea_base)

        linee = sorted(linea_applicata, key=lambda d: d["descrizione"])

        return linee

    @staticmethod
    def getBaseResearchLines(search, teacher, dip, year, only_active=True):
        query_search = Q()
        query_year = Q()
        query_is_active = Q(visibile=True) if only_active else Q()

        if search is not None:
            for k in search.split(" "):
                q_descrizione = Q(descrizione__icontains=k)
                query_search &= q_descrizione
        if year is not None:
            query_year = Q(anno=year)

        query = (
            RicercaLineaBase.objects.filter(query_search, query_year, query_is_active)
            .order_by("descrizione")
            .values(
                "id",
                "descrizione",
                "descr_pubblicaz_prog_brevetto",
                "anno",
                "ricerca_erc2_id__cod_erc2",
                "ricerca_erc2_id__descrizione",
                "visibile",
            )
            .distinct()
        )

        if teacher is not None or dip is not None:
            res = []
            for q in query:
                teachers = RicercaDocenteLineaBase.objects.filter(
                    ricerca_linea_base_id=q["id"]
                ).values(
                    "personale_id__matricola",
                    "personale_id__nome",
                    "personale_id__middle_name",
                    "personale_id__cognome",
                    "personale_id__ds_sede",
                    "personale_id__sede",
                )

                q["Teachers"] = None
                if dip is None:
                    for t in teachers:
                        if t["personale_id__matricola"] == teacher:
                            q["Teachers"] = teachers

                    if q["Teachers"] is not None:
                        res.append(q)

                elif teacher is None:
                    for t in teachers:
                        if t["personale_id__sede"] == dip:
                            q["Teachers"] = teachers

                    if q["Teachers"] is not None:
                        res.append(q)
                else:
                    for t in teachers:
                        if (
                            t["personale_id__sede"] == dip
                            and t["personale_id__matricola"] == teacher
                        ):
                            q["Teachers"] = teachers

                    if q["Teachers"] is not None:
                        res.append(q)

            return res

        for q in query:
            teachers = RicercaDocenteLineaBase.objects.filter(
                ricerca_linea_base_id=q["id"]
            ).values(
                "personale_id__matricola",
                "personale_id__nome",
                "personale_id__middle_name",
                "personale_id__cognome",
                "personale_id__ds_sede",
                "personale_id__sede",
            )

            if len(teachers) == 0:
                q["Teachers"] = []
            else:
                q["Teachers"] = teachers

        return query

    @staticmethod
    def getAppliedResearchLines(search, teacher, dip, year, only_active=True):
        query_search = Q()
        query_year = Q()
        query_is_active = Q(visibile=True) if only_active else Q()

        if search is not None:
            for k in search.split(" "):
                q_descrizione = Q(descrizione__icontains=k)
                query_search &= q_descrizione
        if year is not None:
            query_year = Q(anno=year)

        query = (
            RicercaLineaApplicata.objects.filter(
                query_search, query_year, query_is_active
            )
            .order_by("descrizione")
            .values(
                "id",
                "descrizione",
                "descr_pubblicaz_prog_brevetto",
                "anno",
                "ricerca_aster2_id__ricerca_aster1_id",
                "ricerca_aster2_id__descrizione",
                "visibile",
            )
            .distinct()
        )

        if teacher is not None or dip is not None:
            res = []
            for q in query:
                teachers = RicercaDocenteLineaApplicata.objects.filter(
                    ricerca_linea_applicata_id=q["id"]
                ).values(
                    "personale_id__matricola",
                    "personale_id__nome",
                    "personale_id__middle_name",
                    "personale_id__cognome",
                    "personale_id__ds_sede",
                    "personale_id__sede",
                )

                q["Teachers"] = None
                if dip is None:
                    for t in teachers:
                        if t["personale_id__matricola"] == teacher:
                            q["Teachers"] = teachers

                    if q["Teachers"] is not None:
                        res.append(q)

                elif teacher is None:
                    for t in teachers:
                        if t["personale_id__sede"] == dip:
                            q["Teachers"] = teachers

                    if q["Teachers"] is not None:
                        res.append(q)
                else:
                    for t in teachers:
                        if (
                            t["personale_id__sede"] == dip
                            and t["personale_id__matricola"] == teacher
                        ):
                            q["Teachers"] = teachers

                    if q["Teachers"] is not None:
                        res.append(q)

            return res

        for q in query:
            teachers = RicercaDocenteLineaApplicata.objects.filter(
                ricerca_linea_applicata_id=q["id"]
            ).values(
                "personale_id__matricola",
                "personale_id__nome",
                "personale_id__middle_name",
                "personale_id__cognome",
                "personale_id__ds_sede",
                "personale_id__sede",
            )

            if len(teachers) == 0:
                q["Teachers"] = []
            else:
                q["Teachers"] = teachers

        return query

    @staticmethod
    def teachersList(search, regdid, dip, role, cds, year):
        query_search = Q()
        query_roles = Q()
        query_cds = Q()
        query_regdid = Q()
        query_year = Q()

        if search is not None:
            q_cognome = Q(cognome__istartswith=search)
            query_search &= q_cognome

        if regdid:
            query_regdid = Q(didatticacopertura__af__regdid__regdid_id=regdid)
        if role:
            roles = role.split(",")
            query_roles = Q(cd_ruolo__in=roles)
        if cds:
            query_cds = Q(didatticacopertura__cds_cod=cds)
        if year:
            query_year = Q(didatticacopertura__aa_off_id=year)

        # last_academic_year = ServiceDidatticaCds.getAcademicYears()[0]['aa_reg_did']

        # se visualizzo i docenti di un corso (anche passato)
        # mostro anche quelli che sono cessati
        # altrimenti solo quelli attivi
        if not regdid and not cds:
            query = Personale.objects.filter(
                Q(fl_docente=1, flg_cessato=0)
                |
                (Q(didatticacopertura__aa_off_id=datetime.datetime.now().year) & ~Q(didatticacopertura__stato_coper_cod='R'))
                |
                (Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1) & ~Q(didatticacopertura__stato_coper_cod='R')),
                query_search,
                query_roles,
                query_year
            )
        else:
            query = Personale.objects.filter(
                Q(fl_docente=1)
                |
                ((Q(didatticacopertura__af__isnull=False) & ~Q(didatticacopertura__stato_coper_cod='R'))),
                query_search,
                query_cds,
                query_regdid,
                query_roles,
                query_year,
            )

        query = query.values(
            "id_ab",
            "matricola",
            "nome",
            "middle_name",
            "cognome",
            "cd_ruolo",
            "ds_ruolo_locale",
            "cd_ssd",
            "cd_uo_aff_org",
            "ds_ssd",
            "cv_full_it",
            "cv_short_it",
            "cv_full_eng",
            "cv_short_eng",
            "profilo",
            "ds_profilo",
            "ds_profilo_breve",
        ).order_by("cognome", "nome", "middle_name").distinct()

        if dip:
            department = (
                DidatticaDipartimento.objects.filter(dip_cod=dip)
                .values("dip_id", "dip_cod", "dip_des_it", "dip_des_eng")
                .first()
            )
            if not department:
                return None
            query = query.filter(cd_uo_aff_org=department["dip_cod"])
            query = list(query)
            for q in query:
                q["dip_id"] = department["dip_id"]
                q["dip_cod"] = department["dip_cod"]
                q["dip_des_it"] = department["dip_des_it"]
                q["dip_des_eng"] = department["dip_des_eng"]
        else:
            dip_cods = query.values_list("cd_uo_aff_org", flat=True).distinct()
            dip_cods = list(dip_cods)

            departments = DidatticaDipartimento.objects.filter(
                dip_cod__in=dip_cods
            ).values("dip_id", "dip_cod", "dip_des_it", "dip_des_eng")

            for q in query:
                found = False
                for dep in departments:
                    if dep["dip_cod"] == q["cd_uo_aff_org"]:
                        q["dip_id"] = dep["dip_id"]
                        q["dip_cod"] = dep["dip_cod"]
                        q["dip_des_it"] = dep["dip_des_it"]
                        q["dip_des_eng"] = dep["dip_des_eng"]
                        found = True
                        break

                if not found:
                    q["dip_id"] = None
                    q["dip_cod"] = None
                    q["dip_des_it"] = None
                    q["dip_des_eng"] = None

        append_email_addresses(query, "id_ab")
        return query

    @staticmethod
    def teachingCoveragesList(search, regdid, dip, role, cds, year):
        query_search = Q()
        Q()
        query_roles = Q()
        query_cds = Q()
        query_regdid = Q()
        query_year = Q()

        if search is not None:
            for k in search.split(" "):
                q_cognome = Q(cognome__icontains=k)
                query_search &= q_cognome

        if regdid:
            query_regdid = Q(didatticacopertura__af__regdid__regdid_id=regdid)
        if role:
            roles = role.split(",")
            query_roles = Q(cd_ruolo__in=roles)
        if cds:
            query_cds = Q(didatticacopertura__cds_cod=cds)
        if year:
            query_year = Q(didatticacopertura__aa_off_id=year)

        query = (
            Personale.objects.filter(
                query_search,
                query_cds,
                query_regdid,
                query_roles,
                query_year,
                didatticacopertura__af__isnull=False
            )
            .exclude(didatticacopertura__stato_coper_cod='R')
            .values(
                "id_ab",
                "matricola",
                "nome",
                "middle_name",
                "cognome",
                "cd_ruolo",
                "ds_ruolo_locale",
                "cd_ssd",
                "cd_uo_aff_org",
                "ds_ssd",
                "cv_full_it",
                "cv_short_it",
                "cv_full_eng",
                "cv_short_eng",
                "profilo",
                "ds_profilo",
                "ds_profilo_breve",
            )
            .order_by("cognome", "nome", "middle_name")
            .distinct()
        )

        if dip:
            department = (
                DidatticaDipartimento.objects.filter(dip_cod=dip)
                .values("dip_id", "dip_cod", "dip_des_it", "dip_des_eng")
                .first()
            )
            if not department:
                return None
            query = query.filter(cd_uo_aff_org=department["dip_cod"])
            query = list(query)
            for q in query:
                q["dip_id"] = department["dip_id"]
                q["dip_cod"] = department["dip_cod"]
                q["dip_des_it"] = department["dip_des_it"]
                q["dip_des_eng"] = department["dip_des_eng"]

        else:
            dip_cods = query.values_list("cd_uo_aff_org", flat=True).distinct()
            dip_cods = list(dip_cods)

            departments = DidatticaDipartimento.objects.filter(
                dip_cod__in=dip_cods
            ).values("dip_id", "dip_cod", "dip_des_it", "dip_des_eng")

            for q in query:
                found = False
                for dep in departments:
                    if dep["dip_cod"] == q["cd_uo_aff_org"]:
                        q["dip_id"] = dep["dip_id"]
                        q["dip_cod"] = dep["dip_cod"]
                        q["dip_des_it"] = dep["dip_des_it"]
                        q["dip_des_eng"] = dep["dip_des_eng"]
                        found = True
                        break

                if not found:
                    q["dip_id"] = None
                    q["dip_cod"] = None
                    q["dip_des_it"] = None
                    q["dip_des_eng"] = None

        append_email_addresses(query, "id_ab")
        return query

    @staticmethod
    def getAttivitaFormativeByDocente(teacher, year, yearFrom, yearTo):
        teacher = get_personale_matricola(teacher)

        query = DidatticaCopertura.objects.filter(
            personale__matricola__exact=teacher,
            af__isnull=False,
        ) \
        .exclude(stato_coper_cod='R') \
        .select_related("personale", "af")

        if year:
            query = query.filter(aa_off_id=year)
        elif yearFrom and yearTo:
            query = query.filter(
                aa_off_id__gte=yearFrom,
                aa_off_id__lte=yearTo,
            )
        elif yearFrom:
            query = query.filter(aa_off_id__gte=yearFrom)
        elif yearTo:
            query = query.filter(aa_off_id__lte=yearTo)

        single_id = []
        to_exclude = []

        for cop in query:
            if cop.af_id not in single_id:
                single_id.append(cop.af_id)
            else:
                to_exclude.append(cop.coper_id)
        query = query.exclude(coper_id__in=to_exclude)

        return (
            query.order_by("aa_off_id", "anno_corso", "af_gen_des", "af_gen_des_eng")
            .values(
                "af_id",
                "af_gen_cod",
                "af_gen_des",
                "af_gen_des_eng",
                "regdid_id",
                "anno_corso",
                "ciclo_des",
                "peso",
                "sett_des",
                "af__freq_obblig_flg",
                "cds_des",
                "af__cds__nome_cds_eng",
                "af__lista_lin_did_af",
                "aa_off_id",
                "cds_id",
                "cds_cod",
                "fat_part_stu_des",
                "fat_part_stu_cod",
                "part_stu_des",
                "part_stu_cod",
                "tipo_fat_stu_cod",
                "part_ini",
                "part_fine",
                "coper_peso",
                "ore",
            )
            .order_by("-aa_off_id")
        )

    @staticmethod
    def getDocenteInfo(teacher, use_this_id=False):
        if not use_this_id:
            teacher = get_personale_matricola(teacher)

        query = Personale.objects.filter(
            Q(fl_docente=1, flg_cessato=0)
            | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year) & ~Q(didatticacopertura__stato_coper_cod='R')
            | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1) & ~Q(didatticacopertura__stato_coper_cod='R'),
            matricola=teacher,
        ).distinct()

        if not query.exists():
            raise Http404

        q_contacts = query.filter(
            personalecontatti__cd_tipo_cont__descr_contatto__in=PERSON_CONTACTS_TO_TAKE,
        ).values(
            "personalecontatti__cd_tipo_cont__descr_contatto",
            "personalecontatti__contatto",
        )

        contacts = []
        already_taken_contacts = []
        for contact in q_contacts:
            if not contact["personalecontatti__contatto"]:
                continue
            res = [
                word
                for word in PERSON_CONTACTS_EXCLUDE_STRINGS
                if (word in contact["personalecontatti__contatto"])
            ]
            if (
                not bool(res)
                and contact["personalecontatti__contatto"].lower()
                not in already_taken_contacts
            ):
                contacts.append(contact)
                already_taken_contacts.append(
                    contact["personalecontatti__contatto"].lower()
                )
        # contacts = list(contacts)

        functions = UnitaOrganizzativaFunzioni.objects.filter(
            matricola=teacher,
            termine__gt=datetime.datetime.now(),
            decorrenza__lt=datetime.datetime.now(),
        ).values("ds_funzione", "cd_csa__uo", "cd_csa__denominazione")

        docente_pta_altri_dati = DocentePtaAltriDati.objects.filter(
            matricola__exact=teacher
        ).values(
            "path_foto",
            "path_cv_ita",
            "path_cv_en",
            "breve_bio",
            "breve_bio_en",
            "orario_ricevimento",
            "orario_ricevimento_en",
            "orcid",
        )

        query = query.values(
            "id_ab",
            "matricola",
            "nome",
            "middle_name",
            "cognome",
            "cd_ruolo",
            "ds_ruolo_locale",
            "cd_ssd",
            "ds_ssd",
            "cd_uo_aff_org",
            "ds_aff_org",
            "telrif",
            "email",
            "cv_full_it",
            "cv_short_it",
            "cv_full_eng",
            "cv_short_eng",
            "profilo",
            "ds_profilo",
            "ds_profilo_breve",
        )
        query = list(query)
        docente_pta_altri_dati = list(docente_pta_altri_dati)

        query[0]["ORCID"] = None
        query[0]["PHOTOPATH"] = None
        query[0]["PATHCVITA"] = None
        query[0]["PATHCVENG"] = None
        query[0]["BREVEBIO"] = None
        query[0]["BREVEBIOENG"] = None
        query[0]["ORARIORICEVIMENTO"] = None
        query[0]["ORARIORICEVIMENTOEN"] = None
        if len(docente_pta_altri_dati) > 0:
            query[0]["ORCID"] = docente_pta_altri_dati[0]["orcid"]
            query[0]["PHOTOPATH"] = docente_pta_altri_dati[0]["path_foto"]
            query[0]["PATHCVITA"] = docente_pta_altri_dati[0]["path_cv_ita"]
            query[0]["PATHCVENG"] = docente_pta_altri_dati[0]["path_cv_en"]
            query[0]["BREVEBIO"] = docente_pta_altri_dati[0]["breve_bio"]
            query[0]["BREVEBIOENG"] = docente_pta_altri_dati[0]["breve_bio_en"]
            query[0]["ORARIORICEVIMENTO"] = docente_pta_altri_dati[0][
                "orario_ricevimento"
            ]
            query[0]["ORARIORICEVIMENTOEN"] = docente_pta_altri_dati[0][
                "orario_ricevimento_en"
            ]

        for q in query:
            for c in PERSON_CONTACTS_TO_TAKE:
                q[c] = []
            for c in contacts:
                if not c["personalecontatti__contatto"]:
                    continue
                q[c["personalecontatti__cd_tipo_cont__descr_contatto"]].append(
                    c["personalecontatti__contatto"]
                )

            dep = DidatticaDipartimento.objects.filter(
                dip_cod=q["cd_uo_aff_org"]
            ).values("dip_id", "dip_cod", "dip_des_it", "dip_des_eng")
            if len(dep) == 0:
                q["dip_id"] = None
                q["dip_cod"] = None
                q["dip_des_it"] = None
                q["dip_des_eng"] = None
            else:
                dep = dep.first()
                q["dip_id"] = dep["dip_id"]
                q["dip_cod"] = dep["dip_cod"]
                q["dip_des_it"] = dep["dip_des_it"]
                q["dip_des_eng"] = dep["dip_des_eng"]

            if len(functions) == 0:
                q["Functions"] = None
            else:  # pragma: no cover
                q["Functions"] = functions

        return query

    @staticmethod
    def getDocenteMaterials(user, teacher, search=None):
        teacher = get_personale_matricola(teacher)

        query = Personale.objects.filter(
            Q(fl_docente=1, flg_cessato=0)
            | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year) & ~Q(didatticacopertura__stato_coper_cod='R')
            | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1) & ~Q(didatticacopertura__stato_coper_cod='R'),
            matricola=teacher,
        ).distinct()

        if not query.exists():
            raise Http404

        query_search = Q()
        query_is_active = Q(attivo=True)
        query_is_started = Q(dt_inizio_validita__isnull=True) | Q(
            dt_inizio_validita__lte=datetime.datetime.now()
        )
        query_is_end = Q(dt_fine_validita__isnull=True) | Q(
            dt_fine_validita__gt=datetime.datetime.now()
        )

        if teachers.utils.can_manage_teacher(user, teacher):
            query_is_active = Q()
            query_is_started = Q()
            query_is_end = Q()

        if search:
            for k in search.split(" "):  # pragma: no cover
                query_search = Q(titolo__icontains=k) | Q(titolo_en__icontains=k)

        query = DocenteMaterialeDidattico.objects.filter(
            query_search,
            query_is_active,
            query_is_started,
            query_is_end,
            matricola__exact=teacher,
        ).values(
            "id",
            "titolo",
            "titolo_en",
            "testo",
            "testo_en",
            "url_testo",
            "url_testo_en",
            "ordine",
            "attivo",
            "dt_pubblicazione",
            "dt_inizio_validita",
            "dt_fine_validita",
        )
        for q in query:
            q["DocenteRiferimentoId"] = None
            q["DocenteRiferimentoId"] = teacher

        return query

    @staticmethod
    def getDocenteNews(user, teacher, search=None):
        teacher = get_personale_matricola(teacher)

        query = Personale.objects.filter(
            Q(fl_docente=1, flg_cessato=0)
            | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year) & ~Q(didatticacopertura__stato_coper_cod='R')
            | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1) & ~Q(didatticacopertura__stato_coper_cod='R'),
            matricola=teacher,
        ).distinct()

        if not query.exists():
            raise Http404

        query_search = Q()
        query_is_active = Q(attivo=True)
        query_is_started = Q(dt_inizio_validita__isnull=True) | Q(
            dt_inizio_validita__lte=datetime.datetime.now()
        )
        query_is_end = Q(dt_fine_validita__isnull=True) | Q(
            dt_fine_validita__gt=datetime.datetime.now()
        )

        if teachers.utils.can_manage_teacher(user, teacher):
            query_is_active = Q()
            query_is_started = Q()
            query_is_end = Q()

        if search:
            for k in search.split(" "):  # pragma: no cover
                query_search = Q(titolo__icontains=k) | Q(titolo_en__icontains=k)

        query = DocentePtaBacheca.objects.filter(
            query_search,
            query_is_active,
            query_is_started,
            query_is_end,
            matricola__exact=teacher,
        ).values(
            "id",
            "tipo_testo",
            "tipo_testo_en",
            "titolo",
            "titolo_en",
            "testo",
            "testo_en",
            "url_testo",
            "url_testo_en",
            "ordine",
            "attivo",
            "dt_pubblicazione",
            "dt_inizio_validita",
            "dt_fine_validita",
        )

        return query

    @staticmethod
    def getRoles():
        query = (
            Personale.objects.all()
            .values("cd_ruolo", "ds_ruolo_locale")
            .order_by("ds_ruolo_locale")
            .distinct()
        )

        return query

    @staticmethod
    def getPublicationsList(
        teacherid=None, search=None, year=None, pub_type=None, structure=None
    ):
        if teacherid:
            teacherid = get_personale_matricola(teacherid)

        query_search = Q()
        query_year = Q()
        query_type = Q()
        query_teacher = Q()
        query_structure = Q()

        if search is not None:
            for k in search.split(" "):
                query_search = Q(title__icontains=k) | Q(contributors__icontains=k)
        if year is not None:
            query_year = Q(date_issued_year=year)
        if pub_type is not None:
            query_type = Q(collection_id__community_id__community_id=pub_type)
        if teacherid:
            personale = Personale.objects.filter(matricola=teacherid).values('cod_fis').first()
            if not personale: raise Http404
            query_teacher = Q(pubblicazioneautori__codice_fiscale=personale['cod_fis'])
        if structure:
            query_structure = Q(pubblicazioneautori__ab__cd_uo_aff_org=structure)
        query = (
            PubblicazioneDatiBase.objects.filter(
                query_search, query_year, query_type, query_teacher, query_structure
            )
            .values(
                "item_id",
                "title",
                "des_abstract",
                "des_abstracteng",
                "collection_id__collection_name",
                "collection_id__community_id__community_name",
                "pubblicazione",
                "label_pubblicazione",
                "contributors",
                "date_issued_year",
                "url_pubblicazione",
            )
            .order_by(
                "-date_issued_year",
                "collection_id__community_id__community_name",
                "title",
            )
            .distinct()
        )

        for q in query:
            if q["date_issued_year"] == 9999:
                q["date_issued_year"] = "in stampa"

        return query

    @staticmethod
    def getPublication(publicationid=None):
        query = (
            PubblicazioneDatiBase.objects.filter(item_id=publicationid)
            .values(
                "item_id",
                "title",
                "des_abstract",
                "des_abstracteng",
                "collection_id__collection_name",
                "collection_id__community_id__community_name",
                "pubblicazione",
                "label_pubblicazione",
                "contributors",
                "date_issued_year",
                "url_pubblicazione",
            )
            .order_by("date_issued_year", "title")
            .distinct()
        )
        for q in query:
            if q["date_issued_year"] == 9999:
                q["date_issued_year"] = "in stampa"

        for q in query:
            autori = PubblicazioneAutori.objects.filter(item_id=publicationid).values(
                "ab__id_ab",
                "ab__nome",
                "ab__cognome",
                "ab__middle_name",
                "ab__matricola",
                "first_name",
                "last_name",
            )
            if len(autori) == 0:
                q["Authors"] = []
            else:
                q["Authors"] = autori

        append_email_addresses(autori, "ab__id_ab")

        return query

    @staticmethod
    def getPublicationsCommunityTypesList():
        query = (
            PubblicazioneCommunity.objects.all()
            .values("community_id", "community_name")
            .order_by("community_id")
            .distinct()
        )
        return query
