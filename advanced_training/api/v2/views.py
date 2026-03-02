from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
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
from structures.models import DidatticaDipartimento 
from organizational_area.models import OrganizationalStructureOfficeEmployee
from advanced_training.settings import (
    OFFICE_ADVANCED_TRAINING_VALIDATOR,
    OFFICE_ADVANCED_TRAINING,
    ADVANCED_TRAINING_YEAR,
)
from django.db.models import Q


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

    @action(detail=False, methods=["get"])
    def available_years(self, request):
        """Restituisce gli anni disponibili per il filtro"""
        years = (
            AltaFormazioneDatiBase.objects.values_list("anno_erogazione", flat=True)
            .distinct()
            .order_by("-anno_erogazione")
        )
        return Response({"results": [{"year": year} for year in years if year]})

    @action(detail=False, methods=['get'])
    def available_departments(self, request):
        """Restituisce i dipartimenti disponibili per il filtro"""        
        user = request.user
        
        # Se è superuser o validatore, mostra tutti i dipartimenti
        if user.is_superuser:
            departments = DidatticaDipartimento.objects.filter(
                dip_id__in=AltaFormazioneDatiBase.objects.values_list('dipartimento_riferimento', flat=True).distinct()
            ).values('dip_id', 'dip_cod', 'dip_des_it').order_by('dip_des_it')
        else:
            user_offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=user,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            user_offices_names = list(user_offices.values_list("office__name", flat=True))
            
            if OFFICE_ADVANCED_TRAINING_VALIDATOR in user_offices_names:
                # Validatori vedono tutti i dipartimenti
                departments = DidatticaDipartimento.objects.filter(
                    dip_id__in=AltaFormazioneDatiBase.objects.values_list('dipartimento_riferimento', flat=True).distinct()
                ).values('dip_id', 'dip_cod', 'dip_des_it').order_by('dip_des_it')
            else:
                # Utenti normali vedono tutti i dipartimenti che hanno almeno un master
                departments = DidatticaDipartimento.objects.filter(
                    dip_id__in=AltaFormazioneDatiBase.objects.values_list('dipartimento_riferimento', flat=True).distinct()
                ).values('dip_id', 'dip_cod', 'dip_des_it').order_by('dip_des_it')
        
        return Response({
            'results': [
                {
                    'id': dept['dip_id'],
                    'code': dept['dip_cod'],
                    'name': dept['dip_des_it']
                }
                for dept in departments
            ]
        })

    def get_queryset(self):
        user = self.request.user
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
                # "matricola_proponente",
                "cognome_proponente",
                "nome_proponente",
                "dt_mod",
                "user_mod_id",
            )
            .order_by("titolo_it", "id")
        )

           # Filtro di default per anno corrente se non specificato nei parametri
        year_param = self.request.query_params.get('year')
        if year_param is None and ADVANCED_TRAINING_YEAR:
            try:
                queryset = queryset.filter(anno_erogazione=int(ADVANCED_TRAINING_YEAR))
            except (ValueError, TypeError):
                pass
        elif year_param:
            try:
                queryset = queryset.filter(anno_erogazione=int(year_param))
            except (ValueError, TypeError):
                pass
            
        if user.is_superuser:
            return queryset
        
        user_offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=user,
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )
        user_offices_names = list(user_offices.values_list("office__name", flat=True))

        # Se è validatore, vede tutto
        if OFFICE_ADVANCED_TRAINING_VALIDATOR in user_offices_names:
            return queryset

        user_master_offices = user_offices.filter(office__name=OFFICE_ADVANCED_TRAINING)
        if user_master_offices.exists():
            user_department_codes = list(
                user_master_offices.values_list(
                    "office__organizational_structure__unique_code", flat=True
                )
            )

            # Ottieni il parametro department dal filtro
            department_param = self.request.query_params.get('department')
            
            if department_param:
                # Se viene specificato un dipartimento nel filtro
                if department_param in user_department_codes:
                    # Se è il proprio dipartimento, mostra tutto
                    queryset = queryset.filter(dipartimento_riferimento__dip_cod=department_param)
                else:
                    # Se è un altro dipartimento, mostra solo gli approvati
                    queryset = queryset.filter(
                        dipartimento_riferimento__dip_cod=department_param,
                        altaformazionestatusstorico__id_alta_formazione_status__status_cod="3"
                    ).distinct()
            else:
                # Se non viene specificato un dipartimento, mostra:
                # - Tutti quelli del proprio dipartimento
                # - Solo approvati degli altri dipartimenti
                queryset = queryset.filter(
                    Q(dipartimento_riferimento__dip_cod__in=user_department_codes) |  # Tutti del proprio dipartimento
                    Q(altaformazionestatusstorico__id_alta_formazione_status__status_cod="3")  # Solo approvati degli altri
                ).distinct()

            return queryset
        
        # Utenti senza ufficio master: mostrano solo quelli approvati
        return queryset.filter(
            altaformazionestatusstorico__id_alta_formazione_status__status_cod="3"
        ).distinct()


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
