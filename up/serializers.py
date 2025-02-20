from datetime import date, datetime

from django.utils import timezone


def upImpegniSerializer(
    impegni, lang, year=None, af_name=None, af_cod=None, search={}, show_past=False
):  # pragma: no cover
    impegni_up = []
    search_teacher = search.get("search_teacher", "")
    search_location = search.get("search_location", "")

    for impegno in impegni:
        dettagliDidattici = impegno["evento"]["dettagliDidattici"]

        code = dettagliDidattici[0].get("codiceAF")
        name = dettagliDidattici[0].get("nome")

        # UP non restituisce sempre il codice dell'attività
        # (quando si recuperano gli esami non c'è!)
        if code and af_cod and code != af_cod:
            continue
        if not code and af_name and not name.lower().startswith(af_name.lower()):
            continue

        dataInizio = impegno["dataInizio"][0:10]
        dataFine = impegno["dataFine"][0:10]

        inizio = datetime.strptime(impegno["orarioInizio"], "%Y-%m-%dT%H:%M:00.000Z")
        fine = datetime.strptime(impegno["orarioFine"], "%Y-%m-%dT%H:%M:00.000Z")
        inizio_tz = timezone.localtime(inizio.replace(tzinfo=timezone.utc))
        fine_tz = timezone.localtime(fine.replace(tzinfo=timezone.utc))
        orarioInizio = (
            f"{str(inizio_tz.hour).zfill(2)}:{str(inizio_tz.minute).zfill(2)}"
        )
        orarioFine = f"{str(fine_tz.hour).zfill(2)}:{str(fine_tz.minute).zfill(2)}"

        cfu = dettagliDidattici[0].get("cfu", None)
        insegnamento = (
            dettagliDidattici[0]["nome"]
            if lang == "it" or not dettagliDidattici[0].get("nome_EN")
            else dettagliDidattici[0].get("nome_EN")
        )

        annoCorso = dettagliDidattici[0]["annoCorso"]

        docenti = []
        aule = []
        risorse = impegno["risorse"]
        for risorsa in risorse:
            if risorsa.get("docenteId"):
                docenti.append(
                    risorsa["docente"]["cognome"] + " " + risorsa["docente"]["nome"]
                )
            if risorsa.get("aula"):
                aule.append(
                    {
                        "nome": risorsa["aula"]["descrizione"],
                        "edificio": risorsa["aula"]["edificio"]["descrizione"]
                    }
                )

        if search_teacher:
            teacher_found = False
            for docente in docenti:
                if search_teacher.lower() in docente.lower():
                    teacher_found = True
                    break
            if not teacher_found:
                continue

        if search_location:
            aula_found = False
            for aula in aule:
                if search_location.lower() in aula['nome'].lower():
                    aula_found = True
                    break
            if not aula_found:
                continue

        if not show_past and dataInizio < date.today().strftime("%Y-%m-%d"):
            continue

        extra = {}

        teledidattica = impegno.get('teledidattica', False)
        link_teledidattica = impegno.get('linkTeledidattica', '')
        if teledidattica and link_teledidattica:
            extra['link_teledidattica'] = link_teledidattica

        notePubbliche = impegno.get("notePubbliche", "")
        if notePubbliche:
            extra["note"] = notePubbliche

        impegno_dict = {
            "insegnamento": insegnamento,
            "codice_insegnamento": code,
            "dataInizio": dataInizio,
            "dataFine": dataFine,
            "orarioInizio": orarioInizio,
            "orarioFine": orarioFine,
            "annoCorso": annoCorso,
            "cfu": cfu,
            "docenti": docenti,
            "aule": aule,
            "codice": f"UP_{impegno['evento']['tipoEvento']['codice']}",
            "extra": extra,
        }
        impegni_up.append(impegno_dict)
    return impegni_up
