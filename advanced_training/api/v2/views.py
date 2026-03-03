from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.db.models import Prefetch, Subquery, OuterRef, Q

from .docs import descriptions
from .filters import AdvancedTrainingMastersFilter
from .serializers import (
    AdvancedTrainingMastersSerializer,
    AdvancedTrainingCourseTypesSerializer,
    ErogationModesSerializer,
)
from api_docs import responses
from advanced_training.models import (
    AltaFormazioneAttivitaFormative,
    AltaFormazioneConsiglioScientificoEsterno,
    AltaFormazioneConsiglioScientificoInterno,
    AltaFormazioneDatiBase,
    AltaFormazioneIncaricoDidattico,
    AltaFormazioneModalitaErogazione,
    AltaFormazioneModalitaSelezione,
    AltaFormazionePartner,
    AltaFormazionePianoDidattico,
    AltaFormazioneTipoCorso,
    AltaFormazioneStatusStorico,
)
from structures.models import DidatticaDipartimento
from organizational_area.models import OrganizationalStructureOfficeEmployee
from advanced_training.settings import (
    OFFICE_ADVANCED_TRAINING_VALIDATOR,
    OFFICE_ADVANCED_TRAINING,
    ADVANCED_TRAINING_YEAR,
)

def _latest_status_subquery():
    """Subquery che restituisce il status_cod più recente per ogni master."""
    return (
        AltaFormazioneStatusStorico.objects.filter(
            id_alta_formazione_dati_base=OuterRef("pk")
        )
        .order_by("-data_status", "-dt_mod", "-id")
        .values("id_alta_formazione_status__status_cod")[:1]
    )


def _filter_approved(queryset):
    """Filtra solo i master approvati (status 3) o senza storico (default approvato)."""
    return queryset.annotate(
        _current_status=Subquery(_latest_status_subquery())
    ).filter(Q(_current_status="3") | Q(_current_status__isnull=True))


def _get_departments_for_masters():
    """Restituisce i dipartimenti che hanno almeno un master."""
    return (
        DidatticaDipartimento.objects.filter(
            dip_id__in=AltaFormazioneDatiBase.objects.values_list(
                "dipartimento_riferimento", flat=True
            ).distinct()
        )
        .values("dip_id", "dip_cod", "dip_des_it")
        .order_by("dip_des_it")
    )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.ADVANCEDTRAINING_MASTERS_LIST_SUMMARY,
        description=descriptions.ADVANCEDTRAINING_MASTERS_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(
            AdvancedTrainingMastersSerializer(many=True)
        ),
    ),
    retrieve=extend_schema(
        summary=descriptions.ADVANCEDTRAINING_MASTERS_RETRIEVE_SUMMARY,
        description=descriptions.ADVANCEDTRAINING_MASTERS_RETRIEVE_DESCRIPTION,
        responses=responses.COMMON_RETRIEVE_RESPONSES(
            AdvancedTrainingMastersSerializer
        ),
    ),
)
class AdvancedTrainingMastersViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = AdvancedTrainingMastersSerializer
    filterset_class = AdvancedTrainingMastersFilter

    def _get_user_office_names(self, user):
        return list(
            OrganizationalStructureOfficeEmployee.objects.filter(
                employee=user,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            ).values_list("office__name", flat=True)
        )

    def _get_default_status_for_offices(self, office_names):
        if OFFICE_ADVANCED_TRAINING_VALIDATOR in office_names:
            return "1"
        if OFFICE_ADVANCED_TRAINING in office_names:
            return "2"
        return "3"

    def _pks_with_status(self, queryset, status_cod):
        """Restituisce i PK del queryset il cui status corrente è status_cod."""
        return set(
            queryset.annotate(_cs=Subquery(_latest_status_subquery()))
            .filter(_cs=status_cod)
            .values_list("pk", flat=True)
        )
    
    @action(detail=False, methods=["get"])
    def available_years(self, request):
        """Restituisce gli anni disponibili per il filtro."""
        years = (
            AltaFormazioneDatiBase.objects.values_list("anno_erogazione", flat=True)
            .distinct()
            .order_by("-anno_erogazione")
        )
        return Response({"results": [{"year": y} for y in years if y]})

    @action(detail=False, methods=["get"])
    def available_departments(self, request):
        """Restituisce i dipartimenti disponibili per il filtro."""
        departments = _get_departments_for_masters()
        return Response(
            {
                "results": [
                    {"id": d["dip_id"], "code": d["dip_cod"], "name": d["dip_des_it"]}
                    for d in departments
                ]
            }
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        if (
            not response.data.get("results")
            and request.query_params.get("status") is None
            and not request.user.is_superuser
        ):
            office_names = self._get_user_office_names(request.user)
            default_status = self._get_default_status_for_offices(office_names)
            response.data["empty_message"] = EMPTY_MESSAGES.get(default_status, "")

        return response

    def get_queryset(self):
        user = self.request.user
        base_qs = self._build_base_queryset()
        base_qs = self._apply_year_filter(base_qs)

        if user.is_superuser:
            return base_qs

        office_names = self._get_user_office_names(user)
        status_param = self.request.query_params.get("status")

        # Validatori: default → In Validazione (1)
        if OFFICE_ADVANCED_TRAINING_VALIDATOR in office_names:
            if status_param is None:
                return base_qs.filter(pk__in=self._pks_with_status(base_qs, "1"))
            return base_qs

        # Utenti ufficio master
        user_offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=user,
            office__is_active=True,
            office__organizational_structure__is_active=True,
            office__name=OFFICE_ADVANCED_TRAINING,
        )
        if user_offices.exists():
            return self._queryset_for_office_user(base_qs, user_offices, status_param)

        # Utenti senza ufficio master: solo approvati
        approved_pks = set(_filter_approved(base_qs).values_list("pk", flat=True))
        return base_qs.filter(pk__in=approved_pks)

    def _queryset_for_office_user(self, base_qs, user_offices, status_param):
        """Logica di visibilità per gli utenti dell'ufficio master."""
        user_dept_codes = list(
            user_offices.values_list(
                "office__organizational_structure__unique_code", flat=True
            )
        )
        department_param = self.request.query_params.get("department")

        own_qs = base_qs.filter(dipartimento_riferimento__dip_cod__in=user_dept_codes)
        other_qs = base_qs.exclude(
            dipartimento_riferimento__dip_cod__in=user_dept_codes
        )

        if department_param:
            if department_param in user_dept_codes:
                # Proprio dipartimento: default → Da Correggere (2)
                own_qs = own_qs.filter(
                    dipartimento_riferimento__dip_cod=department_param
                )
                if status_param is None:
                    return base_qs.filter(pk__in=self._pks_with_status(own_qs, "2"))
                return own_qs
            else:
                # Dipartimento altrui: sempre solo approvati
                other_qs = other_qs.filter(
                    dipartimento_riferimento__dip_cod=department_param
                )
                approved_pks = set(
                    _filter_approved(other_qs).values_list("pk", flat=True)
                )
                return base_qs.filter(pk__in=approved_pks)

        # Nessun dipartimento selezionato: proprio → default (2), altri → approvati
        own_pks = (
            self._pks_with_status(own_qs, "2")
            if status_param is None
            else set(own_qs.values_list("pk", flat=True))
        )
        approved_pks = set(_filter_approved(other_qs).values_list("pk", flat=True))
        return base_qs.filter(pk__in=own_pks | approved_pks)

    def _apply_year_filter(self, queryset):
        year_param = self.request.query_params.get("year")
        year = year_param if year_param is not None else ADVANCED_TRAINING_YEAR
        if year:
            try:
                queryset = queryset.filter(anno_erogazione=int(year))
            except (ValueError, TypeError):
                pass
        return queryset

    def _build_base_queryset(self):
        return (
            AltaFormazioneDatiBase.objects.prefetch_related(
                Prefetch(
                    "altaformazionepartner_set",
                    queryset=AltaFormazionePartner.objects.only(
                        "id", "denominazione", "tipologia", "sito_web"
                    ).distinct(),
                    to_attr="partners",
                ),
                Prefetch(
                    "altaformazionemodalitaselezione_set",
                    queryset=AltaFormazioneModalitaSelezione.objects.only(
                        "id", "tipo_selezione"
                    ).distinct(),
                    to_attr="selections",
                ),
                Prefetch(
                    "altaformazioneconsiglioscientificointerno_set",
                    queryset=AltaFormazioneConsiglioScientificoInterno.objects.only(
                        "matricola_cons", "nome_origine_cons"
                    ),
                    to_attr="internal_scientific_council",
                ),
                Prefetch(
                    "altaformazioneconsiglioscientificoesterno_set",
                    queryset=AltaFormazioneConsiglioScientificoEsterno.objects.only(
                        "nome_cons", "ruolo_cons", "ente_cons"
                    ),
                    to_attr="external_scientific_council",
                ),
                Prefetch(
                    "altaformazionepianodidattico_set",
                    queryset=AltaFormazionePianoDidattico.objects.only(
                        "id", "modulo", "ssd", "num_ore", "cfu", "verifica_finale"
                    ),
                    to_attr="teaching_plan",
                ),
                Prefetch(
                    "altaformazioneincaricodidattico_set",
                    queryset=AltaFormazioneIncaricoDidattico.objects.only(
                        "id",
                        "modulo",
                        "num_ore",
                        "docente",
                        "qualifica",
                        "ente",
                        "tipologia",
                    ),
                    to_attr="teaching_assignments",
                ),
                Prefetch(
                    "altaformazioneattivitaformative_set",
                    queryset=AltaFormazioneAttivitaFormative.objects.only(
                        "id",
                        "nome",
                        "programma",
                        "bibliografia",
                        "modalita_verifica_finale",
                        "alta_formazione_attivita_formativa_padre",
                    ),
                    to_attr="training_activities",
                ),
                Prefetch(
                    "altaformazionestatusstorico_set",
                    queryset=AltaFormazioneStatusStorico.objects.select_related(
                        "id_alta_formazione_status"
                    ).order_by("-data_status"),
                    to_attr="status_history",
                ),
            )
            .select_related(
                "dipartimento_riferimento",
                "alta_formazione_tipo_corso",
                "alta_formazione_mod_erogazione",
            )
            .only(
                "id",
                "titolo_it",
                "titolo_en",
                "alta_formazione_tipo_corso",
                "alta_formazione_tipo_corso__tipo_corso_descr",
                "alta_formazione_mod_erogazione",
                "alta_formazione_mod_erogazione__descrizione",
                "lingua",
                "ore",
                "mesi",
                "anno_erogazione",
                "dipartimento_riferimento",
                "dipartimento_riferimento__dip_cod",
                "dipartimento_riferimento__dip_des_it",
                "dipartimento_riferimento__dip_des_eng",
                "data_inizio",
                "data_fine",
                "sede_corso",
                "num_min_partecipanti",
                "num_max_partecipanti",
                "uditori_ammessi",
                "num_max_uditori",
                "requisiti_ammissione",
                "titolo_rilasciato",
                "doppio_titolo",
                "matricola_direttore_scientifico",
                "nome_origine_direttore_scientifico",
                "quota_iscrizione",
                "quota_uditori",
                "funzione_lavoro",
                "obiettivi_formativi_summer_school",
                "competenze",
                "sbocchi_occupazionali",
                "obiettivi_formativi_corso",
                "modalita_svolgimento_prova_finale",
                "numero_moduli",
                "stage_tirocinio",
                "ore_stage_tirocinio",
                "cfu_stage",
                "mesi_stage",
                "tipo_aziende_enti_tirocinio",
                "contenuti_tempi_criteri_cfu",
                "project_work",
                "path_piano_finanziario",
                "path_doc_delibera",
                "cognome_proponente",
                "nome_proponente",
                "dt_mod",
                "user_mod_id",
            )
            .order_by("titolo_it", "id")
        )

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.ADVANCEDTRAINING_COURSE_TYPES_LIST_SUMMARY,
        description=descriptions.ADVANCEDTRAINING_COURSE_TYPES_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(
            AdvancedTrainingCourseTypesSerializer(many=True)
        ),
    ),
)
class AdvancedTrainingCourseTypesViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = AdvancedTrainingCourseTypesSerializer
    queryset = AltaFormazioneTipoCorso.objects.only("id", "tipo_corso_descr")


class ErogationModesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = ErogationModesSerializer
    queryset = AltaFormazioneModalitaErogazione.objects.only("id", "descrizione")
