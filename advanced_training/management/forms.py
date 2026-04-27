from django import forms
from django.db.models import Sum
from django.forms import inlineformset_factory
from advanced_training.models import (
    AltaFormazioneDatiBase,
    AltaFormazioneIncaricoDidattico,
    AltaFormazionePianoDidattico,
    AltaFormazionePartner,
    AltaFormazioneConsiglioScientificoEsterno,
    AltaFormazioneConsiglioScientificoInterno,
    AltaFormazioneStatusStorico,
)
from structures.models import DidatticaDipartimento

class MasterTirocinioForm(forms.ModelForm):
    class Meta:
        model = AltaFormazioneDatiBase
        fields = [
            "stage_tirocinio",
            "ore_stage_tirocinio",
            "cfu_stage",
            "mesi_stage",
            "tipo_aziende_enti_tirocinio",
            "project_work",
        ]
        widgets = {
            "ore_stage_tirocinio": forms.NumberInput(attrs={"min": 0, "step": 1}),
            "cfu_stage": forms.NumberInput(attrs={"min": 0}),
            "mesi_stage": forms.NumberInput(attrs={"min": 0}),
        }

class MasterProvaFinaleForm(forms.ModelForm):
    class Meta:
        model = AltaFormazioneDatiBase
        fields = [
            "modalita_svolgimento_prova_finale",
        ]

class MasterDatiBaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["data_inizio"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        self.fields["data_fine"].input_formats = ["%Y-%m-%d", "%d/%m/%Y"]

    class Meta:
        model = AltaFormazioneDatiBase
        fields = [
            "titolo_it",
            "titolo_en",
            "anno_erogazione",
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
            # "stage_tirocinio",
            # "ore_stage_tirocinio",
            # "cfu_stage",
            # "mesi_stage",
            # "tipo_aziende_enti_tirocinio",
            # "contenuti_tempi_criteri_cfu",
            # "project_work",
            # "modalita_svolgimento_prova_finale",
            "numero_moduli",
            "path_piano_finanziario",
            "path_doc_delibera",
        ]
        widgets = {
            "data_inizio": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "data_fine": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "ore": forms.NumberInput(attrs={"min": 0, "step": 1}),
            "mesi": forms.NumberInput(attrs={"min": 0}),
            "num_min_partecipanti": forms.NumberInput(attrs={"min": 0}),
            "num_max_partecipanti": forms.NumberInput(attrs={"min": 0}),
            "num_max_uditori": forms.NumberInput(attrs={"min": 0}),
            # "ore_stage_tirocinio": forms.NumberInput(attrs={"min": 0, "step": 1}),
            # "cfu_stage": forms.NumberInput(attrs={"min": 0}),
            # "mesi_stage": forms.NumberInput(attrs={"min": 0}),
            # ~ "uditori_ammessi": forms.CheckboxInput(),
            # ~ "doppio_titolo": forms.CheckboxInput(),
            # ~ "project_work": forms.CheckboxInput(),
            # ~ "stage_tirocinio": forms.CheckboxInput(),
            # ~ "path_piano_finanziario": forms.ClearableFileInput(),
            # ~ "path_doc_delibera": forms.ClearableFileInput(),
            "tipo_selezione": forms.Select(),
        }
        labels = {
            "titolo_it": "Titolo (IT)",
            "titolo_en": "Titolo (EN)",
            "anno_erogazione": "Anno accademico",
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
            # "stage_tirocinio": "Stage / Tirocinio previsto",
            # "ore_stage_tirocinio": "Ore di tirocinio",
            # "cfu_stage": "CFU tirocinio",
            # "mesi_stage": "Mesi tirocinio",
            # "tipo_aziende_enti_tirocinio": "Tipologia aziende/enti tirocinio",
            # "contenuti_tempi_criteri_cfu": "Contenuti / Tempi / Criteri CFU",
            # "project_work": "Project Work",
            # "modalita_svolgimento_prova_finale": "Modalità svolgimento prova finale",
            "numero_moduli": "Numero moduli",
            "path_piano_finanziario": "Piano finanziario (allegato)",
            "path_doc_delibera": "Delibera (allegato)",
        }

    def __init__(self, *args, allowed_department_codes=None, **kwargs):
        super().__init__(*args, **kwargs)

        if allowed_department_codes:
            self.fields["dipartimento_riferimento"].queryset = (
                DidatticaDipartimento.objects.filter(
                    dip_cod__in=allowed_department_codes
                )
            )

        required_fields = [
            "titolo_it",
            "anno_erogazione",
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

        ore_stage_new = cleaned_data.get("ore_stage_tirocinio") or 0

        if self.instance and self.instance.pk:
            ore_moduli = (
                self.instance.altaformazionepianodidattico_set
                .aggregate(tot=Sum("num_ore"))["tot"] or 0
            )
            totale = ore_moduli + ore_stage_new

            if totale > 1500:
                self.add_error(
                    "ore_stage_tirocinio",
                    f"Il totale ore piano didattico ({ore_moduli} h) + tirocinio "
                    f"({ore_stage_new} h) supera 1500 ({totale} h). "
                    f"Riduci le ore di tirocinio o modifica il piano didattico."
                )

        return cleaned_data


class PianoDidatticoForm(forms.ModelForm):
    verifica_finale = forms.TypedChoiceField(
        choices=[(True, "Sì"), (False, "No")],
        coerce=lambda x: x == "True",
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Verifica finale",
    )

    class Meta:
        model = AltaFormazionePianoDidattico
        fields = ["modulo", "ssd", "num_ore", "cfu", "verifica_finale"]
        widgets = {
            "num_ore": forms.NumberInput(attrs={"min": 0, "step": 1}),
            "cfu": forms.NumberInput(attrs={"min": 0}),
        }
        labels = {
            "modulo": "Modulo",
            "ssd": "SSD",
            "num_ore": "Numero ore",
            "cfu": "CFU",
            "verifica_finale": "Verifica finale",
        }

    def __init__(self, *args, master=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._master = master 

    def clean(self):
        cleaned_data = super().clean()
        num_ore_new = cleaned_data.get("num_ore") or 0
        cfu_new = cleaned_data.get("cfu") or 0

        if self._master:
            qs = self._master.altaformazionepianodidattico_set.all()
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            ore_altri_moduli = qs.aggregate(tot=Sum("num_ore"))["tot"] or 0
            cfu_altri_moduli = qs.aggregate(tot_cfu=Sum("cfu"))["tot_cfu"] or 0
            
            ore_tirocinio = self._master.ore_stage_tirocinio or 0
            totale = ore_altri_moduli + num_ore_new + ore_tirocinio
            tot_cfu = cfu_altri_moduli + cfu_new

            # if totale > 1500:
            #     self.add_error(
            #         "num_ore",
            #         f"Attenzione: il totale ore piano didattico + tirocinio "
            #         f"supererebbe 1500 ({totale} ore). "
            #         f"Verifica i dati prima di salvare.",
            #     )
                
            # if tot_cfu > 60:
            #     self.add_error(
            #         "cfu",
            #         f"Attenzione: il totale dei CFU del piano didattico "
            #         f"supererebbe i 60 ({tot_cfu}). "
            #         f"Verifica i dati prima di salvare.",
            #     )

        return cleaned_data


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
        fields = ["modulo", "num_ore", "docente", "path_cv", "qualifica", "ente", "tipologia"]
        widgets = {
            "num_ore": forms.NumberInput(attrs={"min": 0, "step": 1}),
        }
        labels = {
            "modulo": "Modulo",
            "num_ore": "Numero ore",
            "docente": "Docente",
            "qualifica": "Qualifica",
            "ente": "Ente",
            "tipologia": "Tipologia docente",
            "path_cv": "Curriculum Vitae"
        }
        help_texts = {"path_cv": "Carica il file se il docente è esterno"}


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
    fields=["nome_cons", "ruolo_cons", "ente_cons"],
    extra=1,
    can_delete=True,
)


class ConsiglioInternoEsternoForm(forms.ModelForm):
    class Meta:
        model = AltaFormazioneConsiglioScientificoInterno
        fields = ["nome_origine_cons"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nome_origine_cons"].required = True
        self.fields["nome_origine_cons"].label = "Nome e Cognome"
        self.fields["nome_origine_cons"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Inserisci nome e cognome del membro esterno",
            }
        )


class ProponenteEsternoForm(forms.Form):
    nome_proponente = forms.CharField(label="Nome proponente", required=True)
    cognome_proponente = forms.CharField(label="Cognome proponente", required=True)


class ChoosenPersonForm(forms.Form):
    choosen_person = forms.CharField(
        label="Seleziona Personale Interno", required=False, widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        required = kwargs.pop("required", False)
        super().__init__(*args, **kwargs)
        self.fields["choosen_person"].required = required


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


class DirettoreScientificoEsternoForm(forms.ModelForm):
    class Meta:
        model = AltaFormazioneDatiBase
        fields = ["nome_origine_direttore_scientifico"]
        labels = {
            "nome_origine_direttore_scientifico": "Nome e Cognome",
        }


# ~ class IncaricoDidatticoEsternoForm(forms.Form):
    # ~ docente = forms.CharField(label="Docente", required=False)
    # ~ qualifica = forms.CharField(label="Qualifica", required=False)
    # ~ ente = forms.CharField(label="Ente", required=False)


class ConsiglioScientificoEsternoForm(forms.ModelForm):
    class Meta:
        model = AltaFormazioneConsiglioScientificoEsterno
        fields = ["nome_cons", "ruolo_cons", "ente_cons"]
        labels = {
            "nome_cons": "Nome e Cognome",
            "ruolo_cons": "Ruolo",
            "ente_cons": "Ente",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nome_cons"].required = True
