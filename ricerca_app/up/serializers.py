from datetime import datetime

from django.utils import timezone


def upImpegniSerializer(impegni, year=None, af_name=None, search={}): # pragma: no cover
    impegni_up = []

    search_teaching = search.get('search_teaching', '')
    search_teacher = search.get('search_teacher', '')
    search_location = search.get('search_location', '')

    for impegno in impegni:
        if year and impegno['evento']['dettagliDidattici'][0]['annoCorso'] != year:
            continue

        if af_name and impegno['evento']['dettagliDidattici'][0]['nome'].lower() != af_name.lower():
            continue

        dataInizio = impegno['dataInizio'][0:10]
        dataFine = impegno['dataFine'][0:10]

        inizio = datetime.strptime(impegno['orarioInizio'], "%Y-%m-%dT%H:%M:00.000Z")
        fine = datetime.strptime(impegno['orarioFine'], "%Y-%m-%dT%H:%M:00.000Z")
        inizio_tz = timezone.localtime(inizio.replace(tzinfo=timezone.utc))
        fine_tz = timezone.localtime(fine.replace(tzinfo=timezone.utc))
        orarioInizio = f"{str(inizio_tz.hour).zfill(2)}:{str(inizio_tz.minute).zfill(2)}"
        orarioFine = f"{str(fine_tz.hour).zfill(2)}:{str(fine_tz.minute).zfill(2)}"

        dettagliDidattici = impegno['evento']['dettagliDidattici']

        cfu = dettagliDidattici[0].get('cfu', None)
        insegnamento = dettagliDidattici[0]['nome']

        if search_teaching and not search_teaching.lower() in insegnamento.lower():
            continue

        annoCorso  = dettagliDidattici[0]['annoCorso']

        docente = ''
        aula = ''
        edificio = ''
        risorse = impegno['risorse']
        for risorsa in risorse:
            if risorsa.get('docente'):
                docente = risorsa['docente']['cognome'] + ' ' +  risorsa['docente']['nome']
            if risorsa.get('aula'):
                aula = risorsa['aula']['descrizione']
                edificio = risorsa['aula']['edificio']['descrizione']

        if search_teacher and search_teacher.lower() not in docente.lower():
            continue
        if search_location and search_location.lower() not in aula.lower():
            continue

        impegno_dict = {
            "insegnamento": insegnamento,
            "dataInizio": dataInizio,
            "dataFine": dataFine,
            "orarioInizio": orarioInizio,
            "orarioFine": orarioFine,
            "annoCorso": annoCorso,
            "cfu": cfu,
            "docente": docente,
            "aula": aula,
            "edificio": edificio,
            "codice": f"UP_{impegno['evento']['tipoEvento']['codice']}"
        }
        impegni_up.append(impegno_dict)
    return impegni_up
