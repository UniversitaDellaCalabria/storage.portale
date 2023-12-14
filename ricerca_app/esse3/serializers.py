def esse3AppelliSerializer(appelli, year=None, af_id=None, search={}): # pragma: no cover
    appelli_list = []
    for appello in appelli:
        data = appello['dataInizioApp'].split(" ")[0].split("/")
        new_data = data[2] + "-" + data[1] + "-" + data[0]
        appello_dict = {
            "insegnamento": appello['adDes'],
            "dataInizio": new_data,
            "dataFine": None,
            "orarioInizio": appello['oraEsa'].split(" ")[1],
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
