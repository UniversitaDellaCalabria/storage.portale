from decimal import Decimal

from django import forms
from django.core.validators import MinValueValidator
from django.db.models import Q
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

from .utils import RESERVED_ROLES, _still_valid


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
    """
    Dati base del laboratorio.

    allowed_department_codes:
        None  -> nessuna restrizione (tutti i dipartimenti sono selezionabili)
        lista -> solo i dipartimenti con quei codici sono modificabili; con lista
                 vuota l'operatore non può cambiare i dipartimenti (il campo
                 viene mostrato ma disabilitato)
    can_set_visibility:
        solo superuser e validatori possono impostare "visibile"; per tutti gli
        altri il campo viene rimosso (la visibilità passa dal flusso di approvazione)

    Dopo l'init, `editable_department_ids` contiene gli id dei dipartimenti che
    l'operatore può aggiungere/rimuovere.
    """

    def __init__(
        self,
        *args,
        allowed_department_codes=None,
        can_set_visibility=False,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        departments = DidatticaDipartimento.objects.all()
        if allowed_department_codes is not None:
            departments = departments.filter(dip_cod__in=allowed_department_codes)
        self.editable_department_ids = set(departments.values_list("pk", flat=True))

        # Dipartimenti attualmente associati: restano sempre tra le scelte, così
        # il form è valido anche se rientrano fuori dal perimetro dell'operatore
        current_ids = set()
        if self.instance.pk:
            current_ids = set(
                LaboratorioDipartimenti.objects.filter(
                    _still_valid(),
                    laboratorio_dati_base=self.instance,
                ).values_list("didattica_dipartimento_id", flat=True)
            )

        department_choices = (
            DidatticaDipartimento.objects.filter(
                Q(pk__in=self.editable_department_ids) | Q(pk__in=current_ids)
            )
            .order_by("dip_des_it")
            .values_list("pk", "dip_des_it")
        )

        self.fields["choosen_department_id"] = forms.MultipleChoiceField(
            label=_("Related Department"),
            choices=tuple(department_choices),
            initial=sorted(current_ids),
            required=True,
            disabled=bool(self.instance.pk) and not self.editable_department_ids,
        )

        # Un ambito disattivato già assegnato al laboratorio resta selezionabile
        self.fields["ambito_s3_prevalente"].queryset = self.fields[
            "ambito_s3_prevalente"
        ].queryset.filter(Q(attivo=True) | Q(pk=self.instance.ambito_s3_prevalente_id))

        if not can_set_visibility:
            self.fields.pop("visibile", None)

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
            "logo_laboratorio",
            "altre_strutture_riferimento",
            "descr_altre_strutture_riferimento_it",
            "descr_altre_strutture_riferimento_en",
            "infrastruttura_riferimento",
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
    """Responsabile scientifico esterno (solo nome e cognome)."""

    responsabile_scientifico = forms.CharField(
        label=_("Name and Surname"),
        max_length=200,
    )


class LaboratorioDatiBaseSafetyManagerForm(forms.Form):
    """Preposto alla sicurezza esterno (solo nome e cognome)."""

    preposto_sicurezza = forms.CharField(
        label=_("Name and Surname"),
        max_length=200,
    )


class LaboratorioDatiBaseScientificDirectorChoosenPersonForm(forms.Form):
    """Responsabile scientifico interno, scelto dalla rubrica."""

    choosen_scientific_director = forms.CharField(
        label=_("Scientific Director"), widget=forms.HiddenInput(), required=False
    )

    def __init__(self, *args, required=False, **kwargs):
        super().__init__(*args, **kwargs)
        if required:
            self.fields["choosen_scientific_director"].required = True


class LaboratorioAltriDipartimentiForm(forms.Form):
    choosen_department = forms.CharField(
        label=_("Department"), widget=forms.HiddenInput(), required=True
    )


class LaboratorioPersonaleTecnicoForm(forms.Form):
    """Ruolo (testo libero) del personale tecnico."""

    ruolo = forms.CharField(
        label=_("Role"),
        # allineato a LaboratorioRuolo.descr_ruolo_it
        max_length=2000,
        required=True,
    )

    def clean_ruolo(self):
        ruolo = self.cleaned_data["ruolo"].strip()
        reserved = {r.lower() for pair in RESERVED_ROLES for r in pair}
        if ruolo.lower() in reserved:
            raise forms.ValidationError(_("This role is reserved"))
        return ruolo


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
    sede_principale = forms.ChoiceField(
        label=_("Main Location"),
        choices=YES_NO_CHOICES,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["edificio"].required = False
        self.fields["piano"].required = False

    def clean(self):
        cleaned_data = super().clean()
        registered = cleaned_data.get("anagrafica_ubicazione")
        if registered:
            cleaned_data["edificio"] = registered.edificio
            cleaned_data["piano"] = registered.piano
        else:
            for name in ("edificio", "piano"):
                if not cleaned_data.get(name):
                    self.add_error(name, _("This field is required."))
        return cleaned_data

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
        self.fields["superficie_mq"].widget.attrs["min"] = 0


class LaboratorioServiziForm(DateRangeValidationMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name in ("laboratorio_anagrafica_servizi", "data_inizio"):
            self.fields[name].required = True

        # Una traiettoria disattivata già assegnata al servizio resta selezionabile,
        # altrimenti non sarebbe più possibile modificare quel servizio
        self.fields["traiettoria_s3"].queryset = TraiettorieS3.objects.filter(
            Q(attiva=True) | Q(pk=self.instance.traiettoria_s3_id)
        ).order_by("codice")

        for name in ("costo_interni", "costo_esterni"):
            self.fields[name].validators.append(MinValueValidator(Decimal(0)))
            self.fields[name].widget.attrs["min"] = 0

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
    def __init__(self, *args, allowed_department_codes=None, laboratory=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.laboratory = laboratory

        # None -> nessuna restrizione; lista (anche vuota) -> solo quei codici
        if allowed_department_codes is not None:
            self.fields["didattica_dipartimento"].queryset = (
                DidatticaDipartimento.objects.filter(
                    dip_cod__in=allowed_department_codes
                )
            )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("principale") and self.laboratory is not None:
            others = LaboratorioDipartimenti.objects.filter(
                _still_valid(),
                laboratorio_dati_base=self.laboratory,
                principale=True,
            )
            if self.instance.pk:
                others = others.exclude(pk=self.instance.pk)
            if others.exists():
                self.add_error(
                    "principale",
                    _("The laboratory already has a main department"),
                )
        return cleaned_data

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
