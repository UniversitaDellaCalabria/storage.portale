from datetime import date


def esse3AppelliSerializer(
    appelli, year=None, af_id=None, search={}, show_past=0
):  # pragma: no cover
    appelli_list = []
    for appello in appelli:
        data = appello["dataInizioApp"].split(" ")[0].split("/")
        new_data = f"{data[2]}-{data[1]}-{data[0]}"

        if not show_past and new_data < date.today().strftime("%Y-%m-%d"):
            continue

        if not appello["oraEsa"]:
            continue

        ora = appello["oraEsa"].split(" ")[1].split(":")
        new_ora = f"{ora[0]}:{ora[1]}"
        appello_dict = {
            "insegnamento": appello["adDes"],
            "codice_insegnamento": appello["adCod"],
            "dataInizio": new_data,
            "dataFine": None,
            "orarioInizio": new_ora,
            "orarioFine": None,
            "annoCorso": None,
            "cfu": None,
            "docente": appello["presidenteCognome"] + " " + appello["presidenteNome"],
            "aule": [{"nome": appello["note"], "edificio": None}],
            "codice": "ESSE3_ES",
            "extra": {
                "descr": appello["desApp"],
                "dataInizioIscrizioni": appello["dataInizioIscr"].split(" ")[0],
                "dataFineIscrizioni": appello["dataFineIscr"].split(" ")[0],
                "stato": appello["statoDes"],
            },
        }
        appelli_list.append(appello_dict)
    return appelli_list
