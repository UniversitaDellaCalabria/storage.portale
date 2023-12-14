def esse3AppelliSerializer(appelli, year=None, af_id=None, search={}): # pragma: no cover
    appelli_list = []
    for appello in appelli:
        data = appello['dataInizioApp'].split(" ")[0].split("/")
        new_data = f"{data[2]}-{data[1]}-{data[0]}"
        ora = appello['oraEsa'].split(" ")[1].split(":")
        new_ora = f"{ora[0]}:{ora[1]}"
        appello_dict = {
            "insegnamento": appello['adDes'],
            "dataInizio": new_data,
            "dataFine": None,
            "orarioInizio": new_ora,
            "orarioFine": None,
            "annoCorso": None,
            "cfu": None,
            "docente": appello['presidenteCognome']+" "+appello['presidenteNome'],
            "aula": appello['note'],
            "edificio": None,
            "codice": "ESSE3_ES"
        }
        appelli_list.append(appello_dict)
    return appelli_list
