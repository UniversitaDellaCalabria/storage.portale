from django.conf import settings


PENTAHO_USERNAME = getattr(settings, "PENTAHO_USERNAME", "")
PENTAHO_PASSWORD = getattr(settings, "PENTAHO_PASSWORD", "")

PENTAHO_MEDIA_PATH = getattr(settings, "PENTAHO_MEDIA_PATH", f"{settings.MEDIA_URL}pentaho/")

PENTAHO_BASE = getattr(settings, "PENTAHO_BASE", "https://repo-unical.bi.u-gov.it/pentaho/api/repos")

# ISODID
PENTAHO_ISODID_MEDIA_PATH = getattr(settings, "PENTAHO_ISODID_MEDIA_PATH", f"{PENTAHO_MEDIA_PATH}isodid/")
PENTAHO_ISODID_REPORT_NAME = getattr(settings, "PENTAHO_ISODID_REPORT_NAME", "Indice_valutazione_Corso_di_Studi_tabella")
PENTAHO_ISODID_REPORT_PATH = getattr(settings, "PENTAHO_ISODID_REPORT_PATH", f":public:spcanalisidati:Report per portale:{PENTAHO_ISODID_REPORT_NAME}.prpt")
PENTAHO_ISODID_REPORT_OUTPUT = getattr(settings, "PENTAHO_ISODID_REPORT_OUTPUT", "table/csv;page-mode=stream")
PENTAHO_ISODID_REPORT_PARAMS = getattr(settings, "PENTAHO_ISODID_REPORT_PARAMS", "&PAR_QUEST=ISODID_STUD_{}&PAR_AA={}&PAR_CDS={}")

PENTAHO_ISODID_REPORT_START_YEAR = ""

PENTAHO_ISODID_REPORT_LEGENDA = {
    "D01": "Le conoscenze preliminari possedute sono risultate sufficienti per la comprensione degli argomenti previsti nel programma d'esame?",
    "D02": "Il carico di studio dell'insegnamento è proporzionato ai crediti assegnati?",
    "D03": "Il materiale didattico (indicato e disponibile) è adeguato per lo studio della materia?",
    "D04": "Le modalità di esame sono state definite in modo chiaro?",
    "D05": "Gli orari di svolgimento delle attività didattiche sono rispettati?",
    "D06": "Il docente stimola / motiva l'interesse verso la disciplina?",
    "D07": "Il docente espone gli argomenti in modo chiaro?",
    "D08": "L'insegnamento è stato svolto in maniera coerente con quanto dichiarato sul sito Web del corso di studio?",
    "D09": "Il docente è reperibile per chiarimenti e spiegazioni?",
    "D10": "Le aule in cui si svolgono le lezioni sono adeguate (si vede, si sente)?",
    "D11": "Le attrezzature utilizzate per la didattica sono adeguate?",
    "D12": "È interessato/a agli argomenti trattati nell'insegnamento?",
    "D13": "E’ complessivamente soddisfatto di questo insegnamento?",
    "D14": "Il laboratorio ha aumentato la mia competenza nell'uso di attrezzature e materiali da laboratorio?",
    "D15": "Le attività laboratoriali sono utili all’apprendimento della materia?",
    "D16": "Le aule in cui si svolge il laboratorio sono adeguate (si vede, si sente)?",
    "D17": "Le attrezzature utilizzate sono qualitativamente adeguate?",
    "D18": "Le attrezzature utilizzate sono quantitativamente adeguate?",
    "D19": "E’ complessivamente soddisfatto rispetto a come sono state svolte le attività laboratoriali",
    "D20": "Le esercitazioni hanno un livello di difficoltà appropriato (né troppo basso né troppo alto)?",
    "D21": "Le esercitazioni sono utili all’apprendimento della materia?",
    "D22": "Le aule in cui si svolgono le esercitazioni sono adeguate (si vede, si sente, si trova posto)?",
    "D23": "Le attrezzature utilizzate per le esercitazioni sono adeguate?",
    "D24": "E’ complessivamente soddisfatto rispetto a come sono state svolte le esercitazioni?"
}
