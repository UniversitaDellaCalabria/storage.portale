from decimal import Decimal

from django import forms
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from generics.widgets import RicercaCRUDCKEditor5EmptyContentWidget
from laboratories.models import (
    LaboratorioAffiliati,
    LaboratorioAnagraficaServizi,
    LaboratorioAnagraficaUbicazioni,
    LaboratorioDatiBase,
    LaboratorioDipartimenti,
    LaboratorioInfrastruttura,
    LaboratorioResponsabile,
    LaboratorioRuolo,
    LaboratorioServizi,
    LaboratorioUbicazione,
    TraiettorieS3,
)
from research_lines.models import RicercaErc0, RicercaErc1
from structures.models import DidatticaDipartimento


def _date_widget():
    return forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")


class DateRangeValidationMixin:
    """Verifica che data_fine non preceda data_inizio."""

    def clean(self):
        cleaned_data = super().clean()
        data_inizio = cleaned_data.get("data_inizio")
        data_fine = cleaned_data.get("data_fine")
        if data_inizio and data_fine and data_fine < data_inizio:
            self.add_error(
                "data_fine",
                _("The end date cannot be earlier than the start date"),
            )
        return cleaned_data


YES_NO_CHOICES = (("SI", _("YES")), ("NO", _("NO")))


class LaboratorioDatiBaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        operator_departments_codes = kwargs.pop("allowed_department_codes", [])

        super().__init__(*args, **kwargs)

        if operator_departments_codes:
            department_choices = DidatticaDipartimento.objects.filter(
                dip_cod__in=operator_departments_codes
            ).values_list("dip_id", "dip_des_it")
        else:
            department_choices = DidatticaDipartimento.objects.all().values_list(
                "dip_id", "dip_des_it"
            )

        self.fields["choosen_department_id"] = forms.MultipleChoiceField(
            label=_("Related Department"),
            choices=tuple(department_choices),
            required=True,
        )

        # self.fields['laboratorio_interdipartimentale'] = forms.ChoiceField(
        #     label=_('Interdepartmental Laboratory'),
        #     choices=(('SI', 'SI'),('NO', 'NO')),
        # )
        self.fields["ambito_s3_prevalente"].queryset = self.fields[
            "ambito_s3_prevalente"
        ].queryset.filter(attivo=True)

        self.order_fields(
            field_order=(
                "nome_laboratorio",
                "acronimo",
                "logo_laboratorio",
                "nome_file_logo",
                "choosen_department_id",
                "infrastruttura_riferimento",
                "altre_strutture_riferimento",
                "descr_altre_strutture_riferimento_it",
                "descr_altre_strutture_riferimento_en",
                "descrizione",
                "ambito_s3_prevalente",
                "tipologia",
                "visibile",
            )
        )

    class Meta:
        model = LaboratorioDatiBase
        fields = [
            "nome_laboratorio",
            "acronimo",
            "logo_laboratorio",  # 'laboratorio_interdipartimentale',
            "altre_strutture_riferimento",
            "descr_altre_strutture_riferimento_it",
            "descr_altre_strutture_riferimento_en",  # 'ambito',
            # "finalita_servizi_it",
            # "finalita_servizi_en",
            # "finalita_ricerca_it",
            # "finalita_ricerca_en",
            # "finalita_didattica_it",
            # "finalita_didattica_en",
            # 'sede_dimensione', 'sede_note_descrittive',
            # 'strumentazione_descrizione', 'strumentazione_valore',
            "infrastruttura_riferimento",
            "sito_web",
            "nome_file_logo",
            "descrizione",
            "ambito_s3_prevalente",
            "tipologia",
            "visibile",
        ]
        labels = {
            "nome_laboratorio": _("Name"),
            "acronimo": _("Acronym"),
            "descrizione": _("Description"),
            "logo_laboratorio": _("Link Laboratory Logo"),
            "nome_file_logo": _("Logo"),
            "altre_strutture_riferimento": _("Other Structures"),
            "descr_altre_strutture_riferimento_it": _(
                "Other Structures Description (it)"
            ),
            "descr_altre_strutture_riferimento_en": _(
                "Other Structures Description (en)"
            ),
            "ambito_s3_prevalente": _("Prevalent S3 Area"),
            "tipologia": _("Type"),
            "infrastruttura_riferimento": _("Reference Infrastructure"),
            "visibile": _("Visible"),
        }
        widgets = {
            "descrizione": RicercaCRUDCKEditor5EmptyContentWidget(),
            "descr_altre_strutture_riferimento_it": RicercaCRUDCKEditor5EmptyContentWidget(),
            "descr_altre_strutture_riferimento_en": RicercaCRUDCKEditor5EmptyContentWidget(),
        }


class LaboratorioDatiBaseScientificDirectorForm(forms.Form):
    responsabile_scientifico = forms.CharField(
        label=_("Name and Surname"),
        max_length=200,
    )


class LaboratorioDatiBaseSafetyManagerForm(forms.Form):
    preposto_sicurezza = forms.CharField(
        label=_("Name and Surname"),
        max_length=200,
    )


class LaboratorioDatiBaseScientificDirectorChoosenPersonForm(forms.Form):
    choosen_scientific_director = forms.CharField(
        label=_("Scientific Director"), widget=forms.HiddenInput(), required=False
    )

    def __init__(self, *args, **kwargs):
        required = kwargs.pop("required", False)
        super(LaboratorioDatiBaseScientificDirectorChoosenPersonForm, self).__init__(
            *args, **kwargs
        )
        if required:
            self.fields["choosen_scientific_director"].required = True


class LaboratorioDatiBaseSafetyManagerChoosenPersonForm(forms.Form):
    choosen_safety_manager = forms.CharField(
        label=_("Safety Manager"), widget=forms.HiddenInput(), required=False
    )

    def __init__(self, *args, **kwargs):
        required = kwargs.pop("required", False)
        super(LaboratorioDatiBaseSafetyManagerChoosenPersonForm, self).__init__(
            *args, **kwargs
        )
        if required:
            self.fields["choosen_safety_manager"].required = True


class LaboratorioDatiBaseDipartimentoForm(forms.Form):
    choosen_department = forms.CharField(
        label=_("Department"), widget=forms.HiddenInput(), required=True
    )


class LaboratorioAltriDipartimentiForm(forms.Form):
    choosen_department = forms.CharField(
        label=_("Department"), widget=forms.HiddenInput(), required=True
    )


class LaboratorioPersonaleTecnicoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ruolo"] = forms.CharField(required=True, label=_("Role"))

        self.fields["percentuale_impegno"] = forms.FloatField(
            required=True, label=_("Commitment %"), min_value=0, max_value=100
        )


class LaboratorioDatiErc1Form(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        erc0_choices = tuple(
            RicercaErc0.objects.all().values_list("erc0_cod", "description")
        )

        erc1 = RicercaErc1.objects.all()

        def _choices(cod):
            return tuple(
                erc1.filter(ricerca_erc0_cod=cod).values_list("id", "descrizione")
            )

        self.fields["erc0_selector"] = forms.ChoiceField(
            label=_("ERC Classification"), choices=erc0_choices
        )

        self.fields["id_ricerche_erc1_ls"] = forms.MultipleChoiceField(
            label=_("ERC Classification - Life Science"),
            choices=_choices("LS"),
            required=False,
            widget=forms.CheckboxSelectMultiple(),
        )

        self.fields["id_ricerche_erc1_pe"] = forms.MultipleChoiceField(
            label=_("ERC Classification - Physical Sciences and Engineering"),
            choices=_choices("PE"),
            required=False,
            widget=forms.CheckboxSelectMultiple(),
        )

        self.fields["id_ricerche_erc1_sh"] = forms.MultipleChoiceField(
            label=_("ERC Classification - Social Sciences and Humanities"),
            choices=_choices("SH"),
            required=False,
            widget=forms.CheckboxSelectMultiple(),
        )


class LaboratorioUbicazioneForm(DateRangeValidationMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["sede_principale"] = forms.ChoiceField(
            label=_("Main Location"),
            choices=YES_NO_CHOICES,
            required=True,
        )

    class Meta:
        model = LaboratorioUbicazione
        fields = [
            "anagrafica_ubicazione",
            "edificio",
            "piano",
            "sede_principale",
            "note",
            "path_file_planimetria",
            "data_inizio",
            "data_fine",
        ]
        labels = {
            "anagrafica_ubicazione": _("Registered Location"),
            "edificio": _("Building"),
            "piano": _("Floor"),
            "sede_principale": _("Main Location"),
            "note": _("Notes"),
            "path_file_planimetria": _("Floor Plan Path"),
            "data_inizio": _("Start Date"),
            "data_fine": _("End Date"),
        }
        widgets = {
            "data_inizio": _date_widget(),
            "data_fine": _date_widget(),
        }


class LaboratorioPersonaleForm(forms.Form):
    laboratory_staff = forms.CharField(label=_("Name and Surname"), max_length=200)


class LaboratorioAnagraficaUbicazioniForm(forms.ModelForm):
    class Meta:
        model = LaboratorioAnagraficaUbicazioni
        fields = ["edificio", "piano", "superficie_mq", "descrizione"]
        labels = {
            "edificio": _("Building"),
            "piano": _("Floor"),
            "superficie_mq": _("Surface (sqm)"),
            "descrizione": _("Description"),
        }
        widgets = {
            "descrizione": RicercaCRUDCKEditor5EmptyContentWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["superficie_mq"].validators.append(MinValueValidator(Decimal(0)))


class LaboratorioServiziForm(DateRangeValidationMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["traiettoria_s3"].queryset = TraiettorieS3.objects.filter(
            attiva=True
        ).order_by("codice")

        for cost_field in ("costo_interni", "costo_esterni"):
            self.fields[cost_field].min_value = 0
            self.fields[cost_field].validators.append(MinValueValidator(Decimal(0)))

    class Meta:
        model = LaboratorioServizi
        fields = [
            "laboratorio_anagrafica_servizi",
            "traiettoria_s3",
            "data_inizio",
            "data_fine",
            "costo_interni",
            "costo_esterni",
            "descrizione_it",
            "descrizione_en",
            "parole_chiavi",
        ]
        labels = {
            "laboratorio_anagrafica_servizi": _("Service"),
            "traiettoria_s3": _("S3 Trajectory"),
            "data_inizio": _("Start Date"),
            "data_fine": _("End Date"),
            "costo_interni": _("Internal Cost"),
            "costo_esterni": _("External Cost"),
            "descrizione_it": _("Description (it)"),
            "descrizione_en": _("Description (en)"),
            "parole_chiavi": _("Keywords"),
        }
        widgets = {
            "data_inizio": _date_widget(),
            "data_fine": _date_widget(),
            "descrizione_it": RicercaCRUDCKEditor5EmptyContentWidget(),
            "descrizione_en": RicercaCRUDCKEditor5EmptyContentWidget(),
        }


class LaboratorioAnagraficaServiziForm(forms.ModelForm):
    class Meta:
        model = LaboratorioAnagraficaServizi
        fields = [
            "nome_servizio_it",
            "nome_servizio_en",
            "descrizione_servizio_it",
            "descrizione_servizio_en",
        ]
        labels = {
            "nome_servizio_it": _("Name (it)"),
            "nome_servizio_en": _("Name (en)"),
            "descrizione_servizio_it": _("Description (it)"),
            "descrizione_servizio_en": _("Description (en)"),
        }
        widgets = {
            "descrizione_servizio_it": RicercaCRUDCKEditor5EmptyContentWidget(),
            "descrizione_servizio_en": RicercaCRUDCKEditor5EmptyContentWidget(),
        }


class LaboratorioResponsabileForm(DateRangeValidationMixin, forms.ModelForm):
    class Meta:
        model = LaboratorioResponsabile
        fields = ["laboratorio_ruolo", "data_inizio", "data_fine"]
        labels = {
            "laboratorio_ruolo": _("Role"),
            "data_inizio": _("Start Date"),
            "data_fine": _("End Date"),
        }
        widgets = {
            "data_inizio": _date_widget(),
            "data_fine": _date_widget(),
        }


class LaboratorioAffiliatiForm(DateRangeValidationMixin, forms.ModelForm):
    class Meta:
        model = LaboratorioAffiliati
        fields = [
            "nome_cognome",
            "ente_provenienza",
            "laboratorio_ruolo",
            "data_inizio",
            "data_fine",
        ]
        labels = {
            "nome_cognome": _("Name and Surname"),
            "ente_provenienza": _("Home Institution"),
            "laboratorio_ruolo": _("Role"),
            "data_inizio": _("Start Date"),
            "data_fine": _("End Date"),
        }
        widgets = {
            "data_inizio": _date_widget(),
            "data_fine": _date_widget(),
        }


class LaboratorioRuoloForm(forms.ModelForm):
    class Meta:
        model = LaboratorioRuolo
        fields = ["descr_ruolo_it", "descr_ruolo_en"]
        labels = {
            "descr_ruolo_it": _("Role (it)"),
            "descr_ruolo_en": _("Role (en)"),
        }


class LaboratorioDipartimentiForm(DateRangeValidationMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        operator_departments_codes = kwargs.pop("allowed_department_codes", [])
        super().__init__(*args, **kwargs)

        if operator_departments_codes:
            self.fields["didattica_dipartimento"].queryset = (
                DidatticaDipartimento.objects.filter(
                    dip_cod__in=operator_departments_codes
                )
            )

    class Meta:
        model = LaboratorioDipartimenti
        fields = [
            "didattica_dipartimento",
            "descr_dip_lab",
            "principale",
            "data_inizio",
            "data_fine",
        ]
        labels = {
            "didattica_dipartimento": _("Department"),
            "descr_dip_lab": _("Department Description"),
            "principale": _("Main Department"),
            "data_inizio": _("Start Date"),
            "data_fine": _("End Date"),
        }
        widgets = {
            "data_inizio": _date_widget(),
            "data_fine": _date_widget(),
        }


class LaboratorioInfrastrutturaForm(forms.ModelForm):
    class Meta:
        model = LaboratorioInfrastruttura
        fields = ["nome", "descrizione_it", "descrizione_en"]
        labels = {
            "nome": _("Name"),
            "descrizione_it": _("Description (it)"),
            "descrizione_en": _("Description (en)"),
        }
        widgets = {
            "descrizione_it": RicercaCRUDCKEditor5EmptyContentWidget(),
            "descrizione_en": RicercaCRUDCKEditor5EmptyContentWidget(),
        }
