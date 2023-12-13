from datetime import datetime

from django.utils import timezone


def impegniSerializer(impegni, year=None, af_id=None, search={}): # pragma: no cover
    impegni_esse3 = []

    for impegno in impegni:

        data = impegno['dataInizioApp'].split(" ")[0].split("/")
        new_data = data[2] + "-" + data[1] + "-" + data[0]


        impegno_dict = {
            "insegnamento": impegno['adDes'],
            "dataInizio": new_data,
            "dataFine": None,
            "orarioInizio": impegno['oraEsa'].split(" ")[1],
            "orarioFine": None,
            "annoCorso": None,
            "cfu": None,
            "docente": impegno['presidenteCognome']+" "+impegno['presidenteNome'],
            "aula": impegno['note'],
            "edificio": None,
            "codice": "ESSE3_ES"
        }
        impegni_esse3.append(impegno_dict)
    return impegni_esse3

import json
def eventiSerializer(eventi, year=None): # pragma: no cover
    eventi_up = []

    for evento in eventi:
        json_formatted_str = json.dumps(evento, indent=2)
        print(json_formatted_str)
        # if evento['tipoEvento']['codice'] == 'ES':
            # print(json_formatted_str)
