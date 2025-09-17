import datetime

from addressbook.models import (
    Personale,
    PersonaleAttivoTuttiRuoli,
    PersonalePrioritaRuolo,
)
from addressbook.settings import (
    PERSON_CONTACTS_EXCLUDE_STRINGS,
    PERSON_CONTACTS_TO_TAKE,
)
from addressbook.utils import get_personale_matricola
from django.db.models import CharField, Q, Value
from django.http import Http404
from structures.api.v1.serializers import StructuresSerializer
from structures.api.v1.services import ServiceStructure
from structures.models import (
    DidatticaDipartimentoUrl,
    UnitaOrganizzativa,
    UnitaOrganizzativaFunzioni,
    UnitaOrganizzativaTipoFunzioni,
)


class ServicePersonale:
    @staticmethod
    def getAddressbook(
        search=None,
        structureid=None,
        structuretypes=None,
        role=None,
        structuretree=None,
        phone=None,
        taxpayer_id=None,
        full=False,
    ):
        query_search = Q()
        role = role.split(",") if role else []

        if search is not None:
            query_search = Q(cognome__istartswith=search)

        if taxpayer_id is not None:
            query_search = Q(cod_fis=taxpayer_id)

        query = (
            Personale.objects.filter(
                query_search,
                # flg_cessato=0,
                # cd_uo_aff_org__isnull=False,
                Q(flg_cessato=0, dt_rap_fin__gte=datetime.datetime.today()) |
                Q(didatticacopertura__aa_off_id=datetime.datetime.now().year) & ~Q(didatticacopertura__stato_coper_cod='R') |
                Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1) & ~Q(didatticacopertura__stato_coper_cod='R'),
            ).values(
                "nome",
                "middle_name",
                "cognome",
                # "cd_uo_aff_org",
                # 'cd_uo_aff_org__denominazione',
                # 'cd_uo_aff_org__cd_tipo_nodo',
                # 'cd_uo_aff_org__ds_tipo_nodo',
                "id_ab",
                "matricola",
                "cod_fis",
                "personalecontatti__cd_tipo_cont__descr_contatto",
                "personalecontatti__contatto",
                "personalecontatti__prg_priorita",
                "fl_docente",
                # ~ "profilo",
                # ~ "ds_profilo",
                # ~ "ds_profilo_breve",
                "cd_ruolo",
                "ds_ruolo_locale",
                "dt_rap_ini"
            ).order_by("cognome", "nome")
        )

        grouped = {}
        last_id = -1
        final_query = []

        ruoli = (
            PersonaleAttivoTuttiRuoli.objects.values(
                "matricola",
                "cd_ruolo",
                "ds_ruolo",
                "cd_uo_aff_org",
                "ds_aff_org",
                "cd_uo_aff_org__cd_tipo_nodo",
                "dt_rap_ini",
                "sede",
                "cd_profilo",
                "ds_profilo"
            )
            .filter(cd_uo_aff_org__isnull=False)
            .distinct()
        )

        ruoli_dict = {}
        for r in ruoli:
            if not ruoli_dict.get(r["matricola"]):
                ruoli_dict[r["matricola"]] = []
            l_data = [
                r["cd_ruolo"],
                r["ds_ruolo"],
                r["cd_uo_aff_org"],
                r["ds_aff_org"],
                r["cd_uo_aff_org__cd_tipo_nodo"],
                r["sede"],
                r["cd_profilo"],
                r["ds_profilo"],
            ]
            if full:
                l_data.append(r["dt_rap_ini"])

            ruoli_dict[r["matricola"]].append(l_data)

        priorita_tmp = PersonalePrioritaRuolo.objects.values("cd_ruolo", "priorita")

        priorita = {}

        for p in priorita_tmp:
            priorita.update({p["cd_ruolo"]: p["priorita"]})

        already_taken_contacts = {}
        for q in query:
            if q["id_ab"] not in grouped:
                grouped[q["id_ab"]] = {
                    "id_ab": q["id_ab"],
                    "nome": q["nome"],
                    "middle_name": q["middle_name"],
                    "cognome": q["cognome"],
                    # 'cd_uo_aff_org': q['cd_uo_aff_org'],
                    "matricola": q["matricola"],
                    "cod_fis": q["cod_fis"],
                    # 'Struttura': q['cd_uo_aff_org__denominazione'],
                    # 'TipologiaStrutturaCod': q['cd_uo_aff_org__cd_tipo_nodo'],
                    # 'TipologiaStrutturaNome': q['cd_uo_aff_org__ds_tipo_nodo'],
                    # 'fl_docente': q['fl_docente'],
                    # ~ "profilo": q["profilo"],
                    # ~ "ds_profilo": q["ds_profilo"],
                    # ~ "ds_profilo_breve": q["ds_profilo_breve"],
                    "Roles": [],
                }
                already_taken_contacts[q["id_ab"]] = []

                for c in PERSON_CONTACTS_TO_TAKE:
                    grouped[q["id_ab"]][c] = []

            if (
                q["personalecontatti__cd_tipo_cont__descr_contatto"]
                in PERSON_CONTACTS_TO_TAKE
            ):
                if q["personalecontatti__contatto"]:
                    res = [
                        word
                        for word in PERSON_CONTACTS_EXCLUDE_STRINGS
                        if (word.lower() in q["personalecontatti__contatto"].lower())
                    ]
                    if (
                        not bool(res)
                        and f'{q["personalecontatti__cd_tipo_cont__descr_contatto"].lower()}-{q["personalecontatti__contatto"].lower()}'
                        not in already_taken_contacts[q["id_ab"]]
                    ):
                        grouped[q["id_ab"]][
                            q["personalecontatti__cd_tipo_cont__descr_contatto"]
                        ].append(q["personalecontatti__contatto"])
                        already_taken_contacts[q["id_ab"]].append(
                            f'{q["personalecontatti__cd_tipo_cont__descr_contatto"].lower()}-{q["personalecontatti__contatto"].lower()}'
                        )

            if last_id == -1 or last_id != q["id_ab"]:
                last_id = q["id_ab"]

                ruoli_dip = ruoli_dict.get(q["matricola"]) or []
                roles = []
                for r in ruoli_dip:
                    d_data = {
                        "matricola": q["matricola"],
                        "cd_ruolo": r[0],
                        "ds_ruolo": r[1],
                        "priorita": priorita.get(r[0]) or 10,
                        "cd_uo_aff_org": r[2],
                        "ds_aff_org": r[3],
                        "cd_tipo_nodo": r[4],
                        "sede": r[5],
                        "cd_profilo": r[6],
                        "ds_profilo": r[7],
                    }
                    if full:
                        d_data["dt_rap_ini"] = r[5]

                    roles.append(d_data)

                if not roles:
                    roles = [{"matricola": q["matricola"],
                             "cd_ruolo": q["cd_ruolo"],
                             "ds_ruolo": q["ds_ruolo_locale"],
                             "priorita": 1,
                             "cd_uo_aff_org": None,
                             "ds_aff_org": None,
                             "cd_tipo_nodo": None,
                             "sede": None,
                             "cd_profilo": None,
                             "ds_profilo": None,
                             "dt_rap_ini": q["dt_rap_ini"]}]

                roles.sort(key=lambda x: x["priorita"])
                grouped[q["id_ab"]]["Roles"] = roles
                final_query.append(grouped[q["id_ab"]])

        filtered = []
        if phone:
            for item in final_query:
                numbers = item.get("Telefono Cellulare Ufficio", []) + item.get(
                    "Telefono Ufficio", []
                )
                if any(phone in string for string in numbers):
                    filtered.append(item)
        else:
            filtered = final_query

        filtered2 = []
        if role:
            roles = []
            for k in role:
                roles.append(k)
            for item in filtered:
                final_roles = []
                for r in item["Roles"]:
                    final_roles.append(r["cd_ruolo"])
                # ~ final_roles.append(item["profilo"])
                final_roles.append(r["cd_profilo"])
                if set(roles).intersection(set(final_roles)):
                    filtered2.append(item)
        else:
            filtered2 = filtered

        filtered3 = []

        if structuretypes:
            s = []
            for k in structuretypes.split(","):
                s.append(k)
            for item in filtered2:
                final_structures = []
                for r in item["Roles"]:
                    # ~ if r["cd_ruolo"] in role or item["profilo"] in role or not role:
                    if r["cd_ruolo"] in role or r["cd_profilo"] in role or not role:
                        final_structures.append(r["cd_tipo_nodo"])
                if set(s).intersection(set(final_structures)):
                    filtered3.append(item)
        else:
            filtered3 = filtered2

        filtered4 = []
        if structureid:
            for item in filtered3:
                for r in item["Roles"]:
                    if r["cd_uo_aff_org"] == structureid or r["sede"] == structureid:
                        # ~ if not role or r["cd_ruolo"] in role or item["profilo"] in role:
                        if not role or r["cd_ruolo"] in role or r["cd_profilo"] in role:
                            filtered4.append(item)
                            break
        else:
            filtered4 = filtered3

        filtered5 = []
        if structuretree:
            query_structuretree = ServiceStructure.getStructureChilds(structuretree)
            for item in filtered4:
                if item["Roles"] and len(item["Roles"]) != 0:
                    for r in item["Roles"]:
                        if (
                            r["cd_uo_aff_org"] in query_structuretree
                            or r["sede"] in query_structuretree
                        ):
                            if (
                                r["cd_ruolo"] in role
                                # ~ or item["profilo"] in role
                                or r["cd_profilo"] in role
                                or not role
                            ):
                                filtered5.append(item)
                                break
        else:
            filtered5 = filtered4

        return filtered5

    @staticmethod
    def getStructuresList(search=None, father=None, type=None, depth=0):
        query_search = Q()
        query_father = Q()
        query_type = Q()

        if father == "None":
            query_father = Q(uo_padre__isnull=True)
        elif father:
            query_father = Q(uo_padre=father)

        if search is not None:
            for k in search.split(" "):
                q_denominazione = Q(denominazione__icontains=k)
                query_search &= q_denominazione

        if type:
            for k in type.split(","):
                q_type = Q(cd_tipo_nodo=k)
                query_type |= q_type

        query = (
            UnitaOrganizzativa.objects.filter(
                query_search,
                query_father,
                query_type,
                dt_fine_val__gte=datetime.datetime.today(),
            )
            .values("uo", "denominazione", "ds_tipo_nodo", "cd_tipo_nodo")
            .distinct()
            .order_by("denominazione")
        )

        for q in query:
            url = DidatticaDipartimentoUrl.objects.filter(dip_cod=q["uo"]).values_list(
                "dip_url", flat=True
            )
            q["dip_url"] = url[0] if url else ""

            if depth == "1":
                q["childs"] = []
                sub_query = (
                    UnitaOrganizzativa.objects.filter(
                        query_search,
                        query_type,
                        uo_padre=q["uo"],
                        dt_fine_val__gte=datetime.datetime.today(),
                    )
                    .values("uo", "denominazione", "ds_tipo_nodo", "cd_tipo_nodo")
                    .distinct()
                    .order_by("denominazione")
                )
                for sq in sub_query:
                    q["childs"].append(StructuresSerializer.to_dict(sq))
        return query

    @staticmethod
    def getStructureTypes(father=None):
        father_query = Q()
        if father is not None:
            father_query = Q(uo_padre=father)
        query = (
            UnitaOrganizzativa.objects.filter(father_query)
            .values("ds_tipo_nodo", "cd_tipo_nodo")
            .distinct()
        )
        return query

    @staticmethod
    def getStructureFunctions():
        query = (
            UnitaOrganizzativaTipoFunzioni.objects.values(
                "cd_tipo_nod", "funzione", "descr_funzione"
            )
            .distinct()
            .order_by("cd_tipo_nod")
        )

        return query

    @staticmethod
    def getPersonale(personale_id, full=False):
        if full:
            query = Personale.objects.filter(
                Q(matricola=personale_id) |
                Q(cod_fis=personale_id),
                Q(flg_cessato=0) |
                Q(didatticacopertura__aa_off_id=datetime.datetime.now().year) & ~Q(didatticacopertura__stato_coper_cod='R') |
                Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1) & ~Q(didatticacopertura__stato_coper_cod='R')
            )
        else:
            personale_id = get_personale_matricola(personale_id)
            query = Personale.objects.filter(
                Q(flg_cessato=0) |
                Q(didatticacopertura__aa_off_id=datetime.datetime.now().year) & ~Q(didatticacopertura__stato_coper_cod='R') |
                Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1) & ~Q(didatticacopertura__stato_coper_cod='R'),
                matricola=personale_id,
            )
        if not query:
            raise Http404

        personale_id = query[0].matricola

        if query.values("cd_uo_aff_org").first()["cd_uo_aff_org"] is None:
            query = (
                query.annotate(Struttura=Value(None, output_field=CharField()))
                .annotate(TipologiaStrutturaCod=Value(None, output_field=CharField()))
                .annotate(TipologiaStrutturaNome=Value(None, output_field=CharField()))
                .annotate(CodStruttura=Value(None, output_field=CharField()))
            )
        else:
            query = query.extra(
                select={
                    "Struttura": "UNITA_ORGANIZZATIVA.DENOMINAZIONE",
                    "CodStruttura": "UNITA_ORGANIZZATIVA.UO",
                    "TipologiaStrutturaCod": "UNITA_ORGANIZZATIVA.CD_TIPO_NODO",
                    "TipologiaStrutturaNome": "UNITA_ORGANIZZATIVA.DS_TIPO_NODO",
                },
                tables=["UNITA_ORGANIZZATIVA"],
                where=[
                    "UNITA_ORGANIZZATIVA.UO=PERSONALE.CD_UO_AFF_ORG",
                ],
            )

        contacts = (
            query.filter(
                personalecontatti__cd_tipo_cont__descr_contatto__in=PERSON_CONTACTS_TO_TAKE
            )
            .values(
                "personalecontatti__cd_tipo_cont__descr_contatto",
                "personalecontatti__contatto",
            )
            .order_by("personalecontatti__prg_priorita")
        )

        contacts = list(contacts)

        functions = UnitaOrganizzativaFunzioni.objects.filter(
            matricola=personale_id,
            termine__gt=datetime.datetime.now(),
            decorrenza__lt=datetime.datetime.now(),
        ).values(
            "ds_funzione",
            "funzione",
            "cd_csa__uo",
            "cd_csa__denominazione",
        )

        query = query.values(
            "id_ab",
            "matricola",
            "cod_fis",
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
            "Struttura",
            "CodStruttura",
            "TipologiaStrutturaCod",
            "TipologiaStrutturaNome",
            "unitaorganizzativafunzioni__ds_funzione",
            "unitaorganizzativafunzioni__termine",
            "fl_docente",
            "cv_full_it",
            "cv_short_it",
            "cv_full_eng",
            "cv_short_eng",
            # ~ "profilo",
            # ~ "ds_profilo",
            # ~ "ds_profilo_breve",
            "cd_genere"
        )

        ruoli = (
            PersonaleAttivoTuttiRuoli.objects.filter(matricola=personale_id)
            .values_list(
                "matricola",
                "cd_ruolo",
                "ds_ruolo",
                "cd_uo_aff_org",
                "ds_aff_org",
                "cd_uo_aff_org__cd_tipo_nodo",
                "cd_profilo",
                "ds_profilo",
                "dt_rap_ini",
            )
            .filter(cd_uo_aff_org__isnull=False)
            .distinct()
        )

        priorita_tmp = PersonalePrioritaRuolo.objects.values("cd_ruolo", "priorita")

        priorita = {}

        for p in priorita_tmp:
            priorita.update({p["cd_ruolo"]: p["priorita"]})

        roles = []

        for r in ruoli:
            d_data = {
                "matricola": r[0],
                "cd_ruolo": r[1],
                "ds_ruolo": r[2],
                "priorita": priorita.get(r[1]) or 10,
                "cd_uo_aff_org": r[3],
                "ds_aff_org": r[4],
                "cd_tipo_nodo": r[5],
                "cd_profilo": r[6],
                "ds_profilo": r[7]
            }
            if full:
                d_data["dt_rap_ini"] = r[8]

            roles.append(d_data)
        roles.sort(key=lambda x: x["priorita"])

        already_taken_contacts = []
        for q in query:
            for c in PERSON_CONTACTS_TO_TAKE:
                q[c] = []
            for c in contacts:
                if not c["personalecontatti__contatto"]:
                    continue
                res = [
                    word
                    for word in PERSON_CONTACTS_EXCLUDE_STRINGS
                    if (word.lower() in c["personalecontatti__contatto"].lower())
                ]
                if (
                    not bool(res)
                    and f'{c["personalecontatti__cd_tipo_cont__descr_contatto"].lower()}-{c["personalecontatti__contatto"].lower()}'
                    not in already_taken_contacts
                ):
                    q[c["personalecontatti__cd_tipo_cont__descr_contatto"]].append(
                        c["personalecontatti__contatto"]
                    )
                    already_taken_contacts.append(
                        f'{c["personalecontatti__cd_tipo_cont__descr_contatto"].lower()}-{c["personalecontatti__contatto"].lower()}'
                    )

            if len(functions) == 0:
                q["Functions"] = None
            else:
                q["Functions"] = functions

            if len(roles) == 0:
                q["Roles"] = [{"matricola": q["matricola"],
                         "cd_ruolo": q["cd_ruolo"],
                         "ds_ruolo": q["ds_ruolo_locale"],
                         "priorita": 1,
                         "cd_uo_aff_org": None,
                         "ds_aff_org": None,
                         "cd_tipo_nodo": None,
                         "sede": None,
                         "cd_profilo": None,
                         "ds_profilo": None,
                         }]
            else:
                q["Roles"] = roles

            q["cop_teacher"] = False
            if not q["fl_docente"]:
                query_teacher = Personale.objects.filter(
                    Q(didatticacopertura__aa_off_id=datetime.datetime.now().year)
                    | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1),
                    didatticacopertura__af__isnull=False,
                    matricola__exact=personale_id,
                ).exists()
                if query_teacher:
                    q["cop_teacher"] = True

        if not query:
            raise Http404
        return query

    @staticmethod
    def getStructure(structureid):
        query = UnitaOrganizzativa.objects.filter(
            uo__exact=structureid, dt_fine_val__gte=datetime.datetime.today()
        )
        contacts_to_take = [
            "EMAIL",
            "PEC",
            "TFR",
        ]
        contacts = query.filter(
            unitaorganizzativacontatti__cd_tipo_cont__in=contacts_to_take
        ).values(
            "unitaorganizzativacontatti__cd_tipo_cont",
            "unitaorganizzativacontatti__contatto",
        )
        contacts = list(contacts)
        query = query.values(
            "uo",
            "denominazione",
            "uo_padre",
            "denominazione_padre",
            "ds_tipo_nodo",
            "cd_tipo_nodo",
            "ds_mission",
            "cd_csa",
        )
        for q in query:
            for c in contacts_to_take:
                q[c] = []
            for c in contacts:
                q[c["unitaorganizzativacontatti__cd_tipo_cont"]].append(
                    c["unitaorganizzativacontatti__contatto"]
                )
            funzioni_personale = UnitaOrganizzativaFunzioni.objects.filter(
                cd_csa=q["cd_csa"],
                cod_fis__flg_cessato=False,
                termine__gt=datetime.datetime.now(),
            ).values(
                "ds_funzione",
                "funzione",
                "cod_fis__nome",
                "cod_fis__cognome",
                "cod_fis__middle_name",
                "cod_fis__matricola",
            )
            if len(funzioni_personale) > 0:
                q["FunzioniPersonale"] = funzioni_personale
            else:
                q["FunzioniPersonale"] = None

            url = DidatticaDipartimentoUrl.objects.filter(dip_cod=q["uo"]).values_list(
                "dip_url", flat=True
            )
            q["dip_url"] = url[0] if url else ""
        return query

    @staticmethod
    def getStructurePersonnelChild(
        structures_tree, structureid=None
    ):  # pragma: no cover
        child_structures = UnitaOrganizzativa.objects.filter(
            uo_padre=structureid
        ).values("uo")

        for child in child_structures:
            structures_tree |= Q(cd_uo_aff_org=child["uo"])
            structures_tree = ServicePersonale.getStructurePersonnelChild(
                structures_tree, child["uo"]
            )
        return structures_tree

    @staticmethod
    def getAllStructuresList(search=None, father=None, type=None):
        query_search = Q()
        query_father = Q()
        query_type = Q()

        if father == "None":
            query_father = Q(uo_padre__isnull=True)
        elif father:
            query_father = Q(uo_padre=father)

        if search is not None:
            for k in search.split(" "):
                q_denominazione = Q(denominazione__icontains=k)
                query_search &= q_denominazione

        if type:
            for k in type.split(","):
                q_type = Q(cd_tipo_nodo=k)
                query_type |= q_type

        query = UnitaOrganizzativa.objects.filter(
            query_search,
            query_father,
            query_type,
            dt_fine_val__gte=datetime.datetime.today(),
        ).extra(
            select={
                "matricola": "PERSONALE.MATRICOLA",
                "cd_uo_aff_org": "PERSONALE.CD_UO_AFF_ORG",
            },
            tables=["PERSONALE"],
            where=[
                "UNITA_ORGANIZZATIVA.UO=PERSONALE.CD_UO_AFF_ORG",
                "PERSONALE.FLG_CESSATO=0",
                "PERSONALE.CD_UO_AFF_ORG is not NULL",
            ],
        )

        query = query.values(
            "uo",
            "denominazione",
            "cd_tipo_nodo",
            "ds_tipo_nodo",
        ).distinct()

        return query

    @staticmethod
    def getPersonnelCfs(roles):
        query_roles = Q()

        if roles is not None:
            roles = roles.split(",")
            query_roles = Q(cd_ruolo__in=roles)

        query = Personale.objects.filter(
            query_roles,
            flg_cessato=0,
            dt_rap_fin__gte=datetime.datetime.today()
        )

        query = query.values(
            "nome",
            "middle_name",
            "cognome",
            "cod_fis",
            "cd_ruolo",
            "ds_ruolo_locale",
            "cd_uo_aff_org",
            "ds_aff_org",
            "matricola",
        ).order_by("cognome")

        return query
