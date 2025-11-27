from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from .docs import descriptions
from api_docs import responses
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets
from django.db.models import Prefetch

from .filters import AdvancedTrainingMastersFilter
from .serializers import (
    AdvancedTrainingMastersSerializer,
    AdvancedTrainingCourseTypesSerializer,
    ErogationModesSerializer,
)
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
        responses=responses.COMMON_RETRIEVE_RESPONSES(AdvancedTrainingMastersSerializer),
    ),
)
class AdvancedTrainingMastersViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = AdvancedTrainingMastersSerializer
    filterset_class = AdvancedTrainingMastersFilter
    queryset = (
        AltaFormazioneDatiBase.objects.prefetch_related(
            Prefetch(
                "altaformazionepartner_set",
                queryset=(
                    AltaFormazionePartner.objects.only(
                        "id", "denominazione", "tipologia", "sito_web"
                    ).distinct()
                ),
                to_attr="partners",
            ),
            Prefetch(
                "altaformazionemodalitaselezione_set",
                queryset=(
                    AltaFormazioneModalitaSelezione.objects.only(
                        "id",
                        "tipo_selezione",
                    ).distinct()
                ),
                to_attr="selections",
            ),
            Prefetch(
                "altaformazioneconsiglioscientificointerno_set",
                queryset=(
                    AltaFormazioneConsiglioScientificoInterno.objects.only(
                        "matricola_cons",
                        "nome_origine_cons",
                    )
                ),
                to_attr="internal_scientific_council",
            ),
            Prefetch(
                "altaformazioneconsiglioscientificoesterno_set",
                queryset=(
                    AltaFormazioneConsiglioScientificoEsterno.objects.only(
                        "nome_cons",
                        "ruolo_cons",
                        "ente_cons",
                    )
                ),
                to_attr="external_scientific_council",
            ),
            Prefetch(
                "altaformazionepianodidattico_set",
                queryset=(
                    AltaFormazionePianoDidattico.objects.only(
                        "id", "modulo", "ssd", "num_ore", "cfu", "verifica_finale"
                    )
                ),
                to_attr="teaching_plan",
            ),
            Prefetch(
                "altaformazioneincaricodidattico_set",
                queryset=(
                    AltaFormazioneIncaricoDidattico.objects.only(
                        "id",
                        "modulo",
                        "num_ore",
                        "docente",
                        "qualifica",
                        "ente",
                        "tipologia",
                    )
                ),
                to_attr="teaching_assignments",
            ),
            Prefetch(
                "altaformazioneattivitaformative_set",
                queryset=(
                    AltaFormazioneAttivitaFormative.objects.only(
                        "id",
                        "nome",
                        "programma",
                        "bibliografia",
                        "modalita_verifica_finale",
                        "alta_formazione_attivita_formativa_padre",
                    )
                ),
                to_attr="training_activities",
            ),
            Prefetch(
                "altaformazionestatusstorico_set",
                queryset=(
                    AltaFormazioneStatusStorico.objects.select_related(
                        "id_alta_formazione_status"
                    ).order_by("-data_status")
                ),
                to_attr="status_history",
            ),
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
            "anno_rilevazione",
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
            "matricola_proponente",
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
class AdvancedTrainingCourseTypesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = AdvancedTrainingCourseTypesSerializer
    queryset = AltaFormazioneTipoCorso.objects.only("id", "tipo_corso_descr")


class ErogationModesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = ErogationModesSerializer
    queryset = AltaFormazioneModalitaErogazione.objects.only("id", "descrizione")
