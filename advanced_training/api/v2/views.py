from django_filters.rest_framework import DjangoFilterBackend

# from drf_spectacular.utils import (
#     extend_schema,
#     extend_schema_view,
# )
# from .docs import descriptions
# from api_docs import responses
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets
from django.db.models import Prefetch

from .filters import HighFormationMastersFilter
from .serializers import (
    HighFormationMastersSerializer,
    HighFormationCourseTypesSerializer,
    ErogationModesSerializer,
)
from advanced_training.models import (
    AltaFormazioneConsiglioScientificoEsterno,
    AltaFormazioneConsiglioScientificoInterno,
    AltaFormazioneDatiBase,
    AltaFormazioneIncaricoDidattico,
    AltaFormazioneModalitaErogazione,
    AltaFormazioneModalitaSelezione,
    AltaFormazionePartner,
    AltaFormazionePianoDidattico,
    AltaFormazioneTipoCorso,
)


class HighFormationMastersViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = HighFormationMastersSerializer
    filterset_class = HighFormationMastersFilter
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
        )
        .order_by("titolo_it", "id")
    )


class HighFormationCourseTypesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = HighFormationCourseTypesSerializer
    queryset = AltaFormazioneTipoCorso.objects.only("id", "tipo_corso_descr")


class ErogationModesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = ErogationModesSerializer
    queryset = AltaFormazioneModalitaErogazione.objects.only("id", "descrizione")
