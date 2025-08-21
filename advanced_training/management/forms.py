from advanced_training.models import AltaFormazioneDatiBase
from django import forms

# 🔹 1. Dati generali
class MasterDatiGeneraliForm(forms.ModelForm):
    class Meta:
        model = AltaFormazioneDatiBase
        fields = [
            "titolo_it", "titolo_en", "anno_rilevazione",
            "dipartimento_riferimento", "alta_formazione_tipo_corso",
            "lingua", "alta_formazione_mod_erogazione",
            "ore", "mesi", "data_inizio", "data_fine",
        ]
        labels = {
            "titolo_it": "Titolo (IT)",
            "titolo_en": "Titolo (EN)",
            "anno_rilevazione": "Anno rilevazione",
            "dipartimento_riferimento": "Dipartimento di riferimento",
            "alta_formazione_tipo_corso": "Tipo di corso",
            "lingua": "Lingua",
            "alta_formazione_mod_erogazione": "Modalità di erogazione",
            "ore": "Ore complessive",
            "mesi": "Durata (mesi)",
            "data_inizio": "Data inizio",
            "data_fine": "Data fine",
        }


# 🔹 2. Iscrizioni e partecipanti
class MasterIscrizioniForm(forms.ModelForm):
    class Meta:
        model = AltaFormazioneDatiBase
        fields = [
            "num_min_partecipanti", "num_max_partecipanti",
            "uditori_ammessi", "num_max_uditori",
            "quota_iscrizione", "quota_uditori",
        ]
        labels = {
            "num_min_partecipanti": "Numero minimo partecipanti",
            "num_max_partecipanti": "Numero massimo partecipanti",
            "uditori_ammessi": "Uditori ammessi",
            "num_max_uditori": "Numero massimo uditori",
            "quota_iscrizione": "Quota di iscrizione",
            "quota_uditori": "Quota uditori",
        }


# 🔹 3. Contenuti e obiettivi
class MasterContenutiForm(forms.ModelForm):
    class Meta:
        model = AltaFormazioneDatiBase
        fields = [
            "requisiti_ammissione", "titolo_rilasciato", "doppio_titolo",
            "funzione_lavoro", "obiettivi_formativi_corso",
            "obiettivi_formativi_summer_school", "competenze",
            "sbocchi_occupazionali",
        ]
        labels = {
            "requisiti_ammissione": "Requisiti di ammissione",
            "titolo_rilasciato": "Titolo rilasciato",
            "doppio_titolo": "Doppio titolo",
            "funzione_lavoro": "Funzione lavoro",
            "obiettivi_formativi_corso": "Obiettivi formativi del corso",
            "obiettivi_formativi_summer_school": "Obiettivi formativi Summer School",
            "competenze": "Competenze",
            "sbocchi_occupazionali": "Sbocchi occupazionali",
        }


# 🔹 4. Stage, tirocinio e project work
class MasterStageForm(forms.ModelForm):
    class Meta:
        model = AltaFormazioneDatiBase
        fields = [
            "stage_tirocinio", "ore_stage_tirocinio", "cfu_stage",
            "mesi_stage", "tipo_aziende_enti_tirocinio",
            "contenuti_tempi_criteri_cfu", "project_work",
        ]
        labels = {
            "stage_tirocinio": "Stage / Tirocinio",
            "ore_stage_tirocinio": "Ore di tirocinio",
            "cfu_stage": "CFU tirocinio",
            "mesi_stage": "Mesi tirocinio",
            "tipo_aziende_enti_tirocinio": "Tipologia aziende/enti tirocinio",
            "contenuti_tempi_criteri_cfu": "Contenuti / Tempi / Criteri CFU",
            "project_work": "Project Work",
        }


# 🔹 5. Altro
class MasterAltroForm(forms.ModelForm):
    class Meta:
        model = AltaFormazioneDatiBase
        fields = [
            "modalita_svolgimento_prova_finale", "numero_moduli",
        ]
        labels = {
            "modalita_svolgimento_prova_finale": "Modalità svolgimento prova finale",
            "numero_moduli": "Numero moduli",
        }
