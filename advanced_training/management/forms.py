from django import forms
from django.forms import inlineformset_factory
from advanced_training.models import (
    AltaFormazioneDatiBase,
    AltaFormazioneIncaricoDidattico,
    AltaFormazionePianoDidattico,
    AltaFormazionePartner,
    AltaFormazioneModalitaSelezione,
    AltaFormazioneConsiglioScientificoEsterno,
    AltaFormazioneConsiglioScientificoInterno,
    AltaFormazioneStatusStorico,
)


class MasterDatiBaseForm(forms.ModelForm):
    tipo_selezione = forms.ModelChoiceField(
        queryset=AltaFormazioneModalitaSelezione.objects.all(),
        required=False,
        label="Modalità di selezione",
    )

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
            "tipo_selezione",
            "ore",
            "mesi",
            "data_inizio",
            "data_fine",
            "sede_corso",
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
            "nome_origine_direttore_scientifico",
            "path_piano_finanziario",
            "path_doc_delibera",
            "matricola_proponente",
            "cognome_proponente",
            "nome_proponente",
        ]
        widgets = {
            "data_inizio": forms.DateInput(attrs={"type": "date"}),
            "data_fine": forms.DateInput(attrs={"type": "date"}),
            "ore": forms.NumberInput(attrs={"min": 0}),
            "mesi": forms.NumberInput(attrs={"min": 0}),
            "num_min_partecipanti": forms.NumberInput(attrs={"min": 0}),
            "num_max_partecipanti": forms.NumberInput(attrs={"min": 0}),
            "num_max_uditori": forms.NumberInput(attrs={"min": 0}),
            "ore_stage_tirocinio": forms.NumberInput(attrs={"min": 0}),
            "cfu_stage": forms.NumberInput(attrs={"min": 0}),
            "mesi_stage": forms.NumberInput(attrs={"min": 0}),
            "uditori_ammessi": forms.CheckboxInput(),
            "doppio_titolo": forms.CheckboxInput(),
            "project_work": forms.CheckboxInput(),
            "stage_tirocinio": forms.CheckboxInput(),
            "path_piano_finanziario": forms.ClearableFileInput(),
            "path_doc_delibera": forms.ClearableFileInput(),
        }
        labels = {
            "titolo_it": "Titolo (IT)",
            "titolo_en": "Titolo (EN)",
            "anno_rilevazione": "Anno rilevazione",
            "dipartimento_riferimento": "Dipartimento di riferimento",
            "alta_formazione_tipo_corso": "Tipo di corso",
            "lingua": "Lingua",
            "alta_formazione_mod_erogazione": "Modalità di erogazione",
            "tipo_selezione": "Modalità di selezione",
            "sede_corso": "Sede del corso",
            "ore": "Ore complessive",
            "mesi": "Durata (mesi)",
            "data_inizio": "Data inizio",
            "data_fine": "Data fine",
            "num_min_partecipanti": "Numero minimo partecipanti",
            "num_max_partecipanti": "Numero massimo partecipanti",
            "uditori_ammessi": "Uditori ammessi",
            "num_max_uditori": "Numero massimo uditori",
            "quota_iscrizione": "Quota di iscrizione (€)",
            "quota_uditori": "Quota uditori (€)",
            "requisiti_ammissione": "Requisiti di ammissione",
            "titolo_rilasciato": "Titolo rilasciato",
            "doppio_titolo": "Doppio titolo",
            "funzione_lavoro": "Funzione lavoro",
            "obiettivi_formativi_corso": "Obiettivi formativi del corso",
            "obiettivi_formativi_summer_school": "Obiettivi formativi Summer School",
            "competenze": "Competenze",
            "sbocchi_occupazionali": "Sbocchi occupazionali",
            "stage_tirocinio": "Stage / Tirocinio previsto",
            "ore_stage_tirocinio": "Ore di tirocinio",
            "cfu_stage": "CFU tirocinio",
            "mesi_stage": "Mesi tirocinio",
            "tipo_aziende_enti_tirocinio": "Tipologia aziende/enti tirocinio",
            "contenuti_tempi_criteri_cfu": "Contenuti / Tempi / Criteri CFU",
            "project_work": "Project Work",
            "modalita_svolgimento_prova_finale": "Modalità svolgimento prova finale",
            "numero_moduli": "Numero moduli",
            "nome_origine_direttore_scientifico": "Nome direttore scientifico",
            "path_piano_finanziario": "Piano finanziario (allegato)",
            "path_doc_delibera": "Delibera (allegato)",
            "matricola_proponente": "Matricola proponente",
            "cognome_proponente": "Cognome proponente",
            "nome_proponente": "Nome proponente",
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

        # File e campi opzionali
        self.fields["path_piano_finanziario"].required = False
        self.fields["path_doc_delibera"].required = False

    def clean(self):
        """Validazione custom dei dati"""
        cleaned_data = super().clean()

        # Validazione date
        data_inizio = cleaned_data.get("data_inizio")
        data_fine = cleaned_data.get("data_fine")

        if data_inizio and data_fine:
            if data_inizio >= data_fine:
                raise forms.ValidationError(
                    "La data di inizio deve essere precedente alla data di fine"
                )

        # Validazione partecipanti
        num_min = cleaned_data.get("num_min_partecipanti")
        num_max = cleaned_data.get("num_max_partecipanti")

        if num_min and num_max:
            if num_min > num_max:
                raise forms.ValidationError(
                    "Il numero minimo non può superare il numero massimo di partecipanti"
                )

        # Validazione quote
        quota_iscrizione = cleaned_data.get("quota_iscrizione")
        quota_uditori = cleaned_data.get("quota_uditori")

        if quota_iscrizione and quota_iscrizione < 0:
            raise forms.ValidationError(
                "La quota di iscrizione non può essere negativa"
            )

        if quota_uditori and quota_uditori < 0:
            raise forms.ValidationError("La quota uditori non può essere negativa")

        return cleaned_data


class PianoDidatticoForm(forms.ModelForm):
    class Meta:
        model = AltaFormazionePianoDidattico
        fields = ["modulo", "ssd", "num_ore", "cfu", "verifica_finale"]
        widgets = {
            "num_ore": forms.NumberInput(attrs={"min": 0}),
            "cfu": forms.NumberInput(attrs={"min": 0}),
        }
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


class IncaricoDidatticoForm(forms.ModelForm):
    class Meta:
        model = AltaFormazioneIncaricoDidattico
        fields = ["modulo", "num_ore", "docente", "qualifica", "ente", "tipologia"]
        widgets = {
            "num_ore": forms.TextInput(attrs={"type": "number", "min": 0}),
        }
        labels = {
            "modulo": "Modulo",
            "num_ore": "Numero ore",
            "docente": "Docente",
            "qualifica": "Qualifica",
            "ente": "Ente",
            "tipologia": "Tipologia docente",
        }


IncaricoDidatticoFormSet = inlineformset_factory(
    AltaFormazioneDatiBase,
    AltaFormazioneIncaricoDidattico,
    form=IncaricoDidatticoForm,
    extra=1,
    can_delete=True,
)


class PartnerForm(forms.ModelForm):
    class Meta:
        model = AltaFormazionePartner
        fields = ["denominazione", "tipologia", "sito_web"]
        widgets = {
            "sito_web": forms.URLInput(attrs={"placeholder": "https://..."}),
        }
        labels = {
            "denominazione": "Denominazione partner",
            "tipologia": "Tipologia",
            "sito_web": "Sito web",
        }


PartnerFormSet = inlineformset_factory(
    AltaFormazioneDatiBase,
    AltaFormazionePartner,
    form=PartnerForm,
    extra=1,
    can_delete=True,
)


class ConsiglioScientificoEsternoForm(forms.ModelForm):
    class Meta:
        model = AltaFormazioneConsiglioScientificoEsterno
        fields = ["nome_cons", "ruolo_cons", "ente_cons"]
        labels = {
            "nome_cons": "Nome",
            "ruolo_cons": "Ruolo",
            "ente_cons": "Ente",
        }


ConsiglioScientificoEsternoFormSet = inlineformset_factory(
    AltaFormazioneDatiBase,
    AltaFormazioneConsiglioScientificoEsterno,
    fields=['nome_cons', 'ruolo_cons', 'ente_cons'],
    extra=1,
    can_delete=True,
)


class ConsiglioScientificoInternoForm(forms.ModelForm):
    class Meta:
        model = AltaFormazioneConsiglioScientificoInterno
        fields = ["matricola_cons", "nome_origine_cons"]
        labels = {
            "matricola_cons": "Matricola",
            "nome_origine_cons": "Nome",
        }


ConsiglioScientificoInternoFormSet = inlineformset_factory(
    AltaFormazioneDatiBase,
    AltaFormazioneConsiglioScientificoInterno,
    fields=['matricola_cons', 'nome_origine_cons'],
    extra=1,
    can_delete=True,
)


class AltaFormazioneStatusForm(forms.ModelForm):
    motivazione = forms.CharField(
        label="Motivazione",
        widget=forms.Textarea(attrs={"rows": 4}),
        required=True,
    )

    class Meta:
        model = AltaFormazioneStatusStorico
        fields = ["motivazione"]
        labels = {
            "motivazione": "Motivazione",
        }
