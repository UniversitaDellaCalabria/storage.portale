from advanced_training.models import (
    AltaFormazioneDatiBase,
    AltaFormazioneIncaricoDidattico,
    AltaFormazionePianoDidattico,
)
from django import forms

from django.forms import inlineformset_factory


class MasterDatiBaseForm(forms.ModelForm):
    class Meta:
        model = AltaFormazioneDatiBase
        fields = [
            "titolo_it",
            "titolo_en",
            "anno_rilevazione",
            "dipartimento_riferimento",
            "alta_formazione_tipo_corso",
            "lingua",
            "alta_formazione_mod_erogazione",
            "ore",
            "mesi",
            "data_inizio",
            "data_fine",
            "num_min_partecipanti",
            "num_max_partecipanti",
            "uditori_ammessi",
            "num_max_uditori",
            "quota_iscrizione",
            "quota_uditori",
            "requisiti_ammissione",
            "titolo_rilasciato",
            "doppio_titolo",
            "funzione_lavoro",
            "obiettivi_formativi_corso",
            "obiettivi_formativi_summer_school",
            "competenze",
            "sbocchi_occupazionali",
            "stage_tirocinio",
            "ore_stage_tirocinio",
            "cfu_stage",
            "mesi_stage",
            "tipo_aziende_enti_tirocinio",
            "contenuti_tempi_criteri_cfu",
            "project_work",
            "modalita_svolgimento_prova_finale",
            "numero_moduli",
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
            "num_min_partecipanti": "Numero minimo partecipanti",
            "num_max_partecipanti": "Numero massimo partecipanti",
            "uditori_ammessi": "Uditori ammessi",
            "num_max_uditori": "Numero massimo uditori",
            "quota_iscrizione": "Quota di iscrizione",
            "quota_uditori": "Quota uditori",
            "requisiti_ammissione": "Requisiti di ammissione",
            "titolo_rilasciato": "Titolo rilasciato",
            "doppio_titolo": "Doppio titolo",
            "funzione_lavoro": "Funzione lavoro",
            "obiettivi_formativi_corso": "Obiettivi formativi del corso",
            "obiettivi_formativi_summer_school": "Obiettivi formativi Summer School",
            "competenze": "Competenze",
            "sbocchi_occupazionali": "Sbocchi occupazionali",
            "stage_tirocinio": "Stage / Tirocinio",
            "ore_stage_tirocinio": "Ore di tirocinio",
            "cfu_stage": "CFU tirocinio",
            "mesi_stage": "Mesi tirocinio",
            "tipo_aziende_enti_tirocinio": "Tipologia aziende/enti tirocinio",
            "contenuti_tempi_criteri_cfu": "Contenuti / Tempi / Criteri CFU",
            "project_work": "Project Work",
            "modalita_svolgimento_prova_finale": "Modalità svolgimento prova finale",
            "numero_moduli": "Numero moduli",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_fields = [
            "titolo_it",
            "anno_rilevazione",
            "dipartimento_riferimento",
            "alta_formazione_tipo_corso",
            "lingua",
            "alta_formazione_mod_erogazione",
            "data_inizio",
            "data_fine",
        ]

        for field in required_fields:
            self.fields[field].required = True


class IncaricoDidatticoForm(forms.ModelForm):
    class Meta:
        model = AltaFormazioneIncaricoDidattico
        fields = ["modulo", "num_ore", "docente", "qualifica", "ente", "tipologia"]
        labels = {
            "modulo": "Modulo",
            "num_ore": "Numero ore",
            "docente": "Docente",
            "qualifica": "Qualifica",
            "ente": "Ente",
            "tipologia": "Tipologia",
        }


IncaricoDidatticoFormSet = inlineformset_factory(
    AltaFormazioneDatiBase,
    AltaFormazioneIncaricoDidattico,
    form=IncaricoDidatticoForm,
    extra=1,
    can_delete=True,
)


class PianoDidatticoForm(forms.ModelForm):
    class Meta:
        model = AltaFormazionePianoDidattico
        fields = ["modulo", "ssd", "num_ore", "cfu", "verifica_finale"]
        labels = {
            "modulo": "Modulo",
            "ssd": "SSD",
            "num_ore": "Numero ore",
            "cfu": "CFU",
            "verifica_finale": "Verifica finale",
        }


PianoDidatticoFormSet = inlineformset_factory(
    AltaFormazioneDatiBase,
    AltaFormazionePianoDidattico,
    form=PianoDidatticoForm,
    extra=1,
    can_delete=True,
)
