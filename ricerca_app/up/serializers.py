from datetime import datetime

from django.utils import timezone


def impegniSerializer(impegni, year=None):
    impegni_up = []

    for impegno in impegni:
        if year and impegno['evento']['dettagliDidattici'][0]['annoCorso'] != year:
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

        cfu = dettagliDidattici[0]['cfu']
        insegnamento = dettagliDidattici[0]['nome']
        annoCorso  = dettagliDidattici[0]['annoCorso']

        docente = None
        aula = None
        edificio = None
        risorse = impegno['risorse']
        for risorsa in risorse:
            if risorsa.get('docente'):
                docente = risorsa['docente']['cognome'] + ' ' +  risorsa['docente']['nome']
            if risorsa.get('aula'):
                aula = risorsa['aula']['descrizione']
                edificio = risorsa['aula']['edificio']['descrizione']

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
            "edificio": edificio
        }
        impegni_up.append(impegno_dict)
    return impegni_up
