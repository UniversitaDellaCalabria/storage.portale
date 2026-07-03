import datetime
from api_docs import responses
from .docs import descriptions

from django.conf import settings
from django.db import models
from django.db.models import (
    Case,
    Exists,
    F,
    OuterRef,
    Prefetch,
    Q,
    Subquery,
    Value,
    When,
)
from django.db.models.functions import Coalesce, Concat
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from organizational_area.models import OrganizationalStructureOfficeEmployee
from cds.settings import OFFICE_CDS, OFFICE_CDS_DOCUMENTS, OFFICE_CDS_TEACHING_SYSTEM

from rest_framework import mixins, viewsets
from generics.api.labels import LABEL_MAPPING
# ~ from rest_framework.pagination import PageNumberPagination

from generics.api.pagination import PageNumberPagination, UnicalStorageApiPaginationList
from generics.utils import is_nullable
from generics.views import ClearResponseViewSet


from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from structures.models import DidatticaDipartimentoUrl
from cds.models import (
    DidatticaAttivitaFormativa,
    DidatticaAttivitaFormativaErogata,
    DidatticaAttivitaFormativaPds,
    DidatticaCds,
    DidatticaCdsAltriDati,
    DidatticaCdsCollegamento,
    DidatticaCopertura,
    DidatticaPdsRegolamento,
    DidatticaRegolamento,
    DidatticaTestiAfErogata,
    DidatticaTestiRegolamento,
    DidatticaRegolamentoAltriDati,
    DidatticaCdsLingua,
    DidatticaCdsAltriDatiUfficio,
    DidatticaCdsGruppi,
    DidatticaCdsGruppiComponenti,
    DidatticaCoperturaDettaglioOre,
    DidatticaPianiStudio,
    DidatticaPianiSchema,
    VDidatticaAfPianiStudio,
    DidatticaPianiRegSce
    # ~ DidatticaAttivitaFormativaModalita
)

from .filters import (
    CdsExpiredFilter,
    CdsFilter,
    StudyActivitiesFilter,
)
from .serializers import (
    AcademicPathwaysDetailSerializer,
    AcademicPathwaysListSerializer,
    AcademicYearsSerializer,
    CdsAreasSerializer,
    CdsExpiredSerializer,
    CdsMorphSerializer,
    CdsSerializer,
    DegreeTypeSerializer,
    StudyActivitiesDetailSerializer,
    StudyActivitiesListSerializer,
    CdsDetailSerializer,
    SortingContactsSerializer,
    StudyPlansActivitiesSerializer,
    StudyPlansSerializer,
)

from ..v1.serializers import (
    StudyActivitiesDetailSerializerV1,
    StudyActivitiesListSerializerV1,
    StudyPlansSerializerV1,
    StudyPlansActivitiesSerializerV1
)

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.DEGREETYPE_LIST_SUMMARY,
        description=descriptions.DEGREETYPE_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(
            DegreeTypeSerializer(many=True), include_bad_request=False
        ),
    )
)
class DegreeTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, ClearResponseViewSet):
    serializer_class = DegreeTypeSerializer
    queryset = (
        DidatticaCds.objects.values("tipo_corso_cod", "tipo_corso_des")
        .distinct()
        .order_by("tipo_corso_des")
    )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.ACADEMICYEAR_LIST_SUMMARY,
        description=descriptions.ACADEMICYEAR_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(
            AcademicYearsSerializer(many=True), include_bad_request=False
        ),
    )
)
class AcademicYearsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, ClearResponseViewSet):
    serializer_class = AcademicYearsSerializer
    queryset = (
        DidatticaRegolamento.objects.values("aa_reg_did")
        .distinct()
        .order_by("-aa_reg_did")
    )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.CDSAREA_LIST_SUMMARY,
        description=descriptions.CDSAREA_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(
            CdsAreasSerializer(many=True), include_bad_request=False
        ),
    )
)
class CdsAreasViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, ClearResponseViewSet):
    serializer_class = CdsAreasSerializer
    queryset = (
        DidatticaCds.objects.values("area_cds", "area_cds_en")
        .filter(area_cds__isnull=False, area_cds_en__isnull=False)
        .distinct()
    )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.CDSEXPIRED_LIST_SUMMARY,
        description=descriptions.CDSEXPIRED_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(CdsExpiredSerializer(many=True)),
    )
)
class CdsExpiredViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, ClearResponseViewSet):
    serializer_class = CdsExpiredSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CdsExpiredFilter
    queryset = DidatticaRegolamento.objects.all()

    def get_queryset(self):
        cds_morphed = DidatticaCdsCollegamento.objects.values_list(
            "cds_prec__cds_cod", flat=True
        )
        return (
            DidatticaRegolamento.objects.filter(
                ~Exists(
                    DidatticaRegolamento.objects.filter(
                        cds=OuterRef("cds"),
                        aa_reg_did__gt=OuterRef("aa_reg_did"),
                    ).exclude(stato_regdid_cod__in=["E","R"])
                ),
                aa_reg_did__lt=settings.CURRENT_YEAR,
            )
            .exclude(stato_regdid_cod__in=["E","R"])
            .exclude(aa_reg_did__lte=(settings.CURRENT_YEAR - F("cds__durata_anni")))
            .exclude(cds__cds_cod__in=cds_morphed)
        )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.CDSMORPH_LIST_SUMMARY,
        description=descriptions.CDSMORPH_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(CdsMorphSerializer(many=True)),
    ),
    retrieve=extend_schema(
        summary=descriptions.CDSMORPH_RETRIEVE_SUMMARY,
        description=descriptions.CDSMORPH_RETRIEVE_DESCRIPTION,
        responses=responses.COMMON_RETRIEVE_RESPONSES(CdsMorphSerializer),
    ),
)
class CdsMorphViewSet(ReadOnlyModelViewSet, ClearResponseViewSet):
    serializer_class = CdsMorphSerializer
    queryset = DidatticaCds.objects.all()

    def list(self, request, *args, **kwargs):
        collegamenti_prefetch = DidatticaCdsCollegamento.objects.select_related(
            "cds_prec"
        )
        roots = (
            DidatticaCdsCollegamento.objects.exclude(
                cds__pk__in=DidatticaCdsCollegamento.objects.values_list(
                    "cds_prec", flat=True
                )
            )
            .select_related("cds")
            .prefetch_related(Prefetch("cds_prec", queryset=collegamenti_prefetch))
        )

        previous_cds_cod_dict = {}
        for root in roots:
            previous_cds_cod_dict[root.cds.cds_cod] = self._build_cds_history(
                root.cds.cds_cod
            )

        return Response(previous_cds_cod_dict)

    def retrieve(self, request, *args, **kwargs):
        cds_cod = self.kwargs.get("pk")
        cds = DidatticaCds.objects.filter(cds_cod=cds_cod).order_by("-cds_id").first()

        previous_cds_cod_list = []
        if cds:
            current_cds = cds
            while current_cds:
                collegamento = DidatticaCdsCollegamento.objects.filter(
                    cds=current_cds
                ).first()
                if collegamento:
                    predecessor = collegamento.cds_prec
                    previous_cds_cod_list.append(predecessor.cds_cod)
                    current_cds = predecessor
                else:
                    break

        return Response(previous_cds_cod_list)

    def _build_cds_history(self, cds_cod, history=None):
        if history is None:
            history = []

        prec = (
            DidatticaCdsCollegamento.objects.filter(cds__cds_cod=cds_cod)
            .select_related("cds_prec")
            .first()
        )
        if prec and prec.cds_prec:
            history.append(prec.cds_prec.cds_cod)
            self._build_cds_history(prec.cds_prec.cds_cod, history)
        return history


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.CDS_LIST_SUMMARY,
        description=descriptions.CDS_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(CdsSerializer(many=True)),
    ),
    retrieve=extend_schema(
        summary=descriptions.CDS_RETRIEVE_SUMMARY,
        description=descriptions.CDS_RETRIEVE_DESCRIPTION,
        responses=responses.COMMON_RETRIEVE_RESPONSES(CdsSerializer),
    ),
)
class CdsViewSet(ReadOnlyModelViewSet, ClearResponseViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = CdsFilter
    queryset = DidatticaRegolamento.objects.all()

    def get_queryset(self):
        only_active = True
        if self.request.user.is_superuser:
            only_active = False  # pragma: no cover
        if self.request.user.is_authenticated:  # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=self.request.user,
                office__name__in=[
                    OFFICE_CDS,
                    OFFICE_CDS_DOCUMENTS,
                    OFFICE_CDS_TEACHING_SYSTEM,
                ],
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            if my_offices:
                only_active = False

        ordinamento_subquery = (
            DidatticaCdsAltriDati.objects.filter(
                regdid__cds=OuterRef("cds"), ordinamento_didattico__isnull=False
            )
            .order_by("-regdid")
            .values("ordinamento_didattico")[:1]
        )

        if self.action == "list":
            return (
                DidatticaRegolamento.objects.select_related(
                    "cds__dip", "didatticacdsaltridati"
                )
                .prefetch_related(
                    Prefetch(
                        "cds__didatticacdslingua",
                        queryset=DidatticaCdsLingua.objects.only(
                            "lingua_des_it", "lingua_des_eng"
                        ).distinct(),
                        to_attr="lingue",
                    ),
                )
                .only(
                    "regdid_id",
                    "cds__cds_id",
                    "cds__cds_cod",
                    "aa_reg_did",
                    "cds__nome_cds_it",
                    "cds__area_cds",
                    "cds__dip__dip_id",
                    "cds__dip__dip_cod",
                    "cds__dip__dip_des_it",
                    "cds__tipo_corso_cod",
                    "cds__tipo_corso_des",
                    "cds__cla_miur_cod",
                    "cds__cla_miur_des",
                    "cds__intercla_miur_cod",
                    "cds__intercla_miur_des",
                    "modalita_erogazione",
                    "frequenza_obbligatoria",
                    "cds__durata_anni",
                    "cds__valore_min",
                    "stato_regdid_cod",
                    "titolo_congiunto_cod",
                    "cds__aa_ord_id",
                    "cds__cdsord_id",
                    "didatticacdsaltridati__manifesto_studi",
                    "didatticacdsaltridati__regolamento_didattico",
                )
                .annotate(ordinamento_didattico=Subquery(ordinamento_subquery))
                .order_by("-regdid_id")
            )

        if self.action == "retrieve":
            query_visibile = Q(visibile=True) if only_active else Q()

            queryset = (
                DidatticaRegolamento.objects.select_related("cds__dip")
                .prefetch_related(
                    Prefetch(
                        "cds__didatticacdslingua",
                        queryset=DidatticaCdsLingua.objects.only(
                            "lingua_des_it", "lingua_des_eng"
                        ).distinct(),
                        to_attr="lingue",
                    ),
                    Prefetch(
                        "didatticatestiregolamento_set",
                        queryset=DidatticaTestiRegolamento.objects.only(
                            "regdid_id",
                            "clob_txt_ita",
                            "clob_txt_eng",
                            # ~ "testo_regdid_url",
                            "tipo_testo_regdid_cod",
                            # ~ "profilo",
                            # ~ "profilo_eng",
                        ),
                        to_attr="texts",
                    ),
                    Prefetch(
                        "didatticaregolamentoaltridati_set",
                        queryset=DidatticaRegolamentoAltriDati.objects.only(
                            "regdid_id",
                            "clob_txt_ita",
                            "clob_txt_eng",
                            "tipo_testo_regdid_cod",
                        ),
                        to_attr="otherDataReg",
                    ),
                    Prefetch(
                        "didatticacdsaltridati",
                        queryset=DidatticaCdsAltriDati.objects.only(
                            "matricola_coordinatore",
                            "nome_origine_coordinatore",
                            "matricola_vice_coordinatore",
                            "nome_origine_vice_coordinatore",
                            "manifesto_studi",
                            "regolamento_didattico",
                            "ordinamento_didattico",
                        ).distinct(),
                        to_attr="otherData",
                    ),
                    Prefetch(
                        "cds__didatticacdsaltridatiufficio_set",
                        queryset=DidatticaCdsAltriDatiUfficio.objects.only(
                            "ordine",
                            "nome_ufficio",
                            "matricola_riferimento",
                            "nome_origine_riferimento",
                            "telefono",
                            "email",
                            "edificio",
                            "piano",
                            "orari",
                            "sportello_online",
                        ).distinct(),
                        to_attr="officesData",
                    ),
                    Prefetch(
                        "cds__didatticacdsgruppi_set",
                        queryset=DidatticaCdsGruppi.objects.filter(query_visibile)
                        .only(
                            "ordine",
                            "id",
                            "descr_breve_it",
                            "descr_breve_en",
                            "descr_lunga_it",
                            "descr_lunga_en",
                        )
                        .distinct()
                        .prefetch_related(
                            Prefetch(
                                "didatticacdsgruppicomponenti_set",
                                queryset=DidatticaCdsGruppiComponenti.objects.filter(
                                    query_visibile
                                )
                                .only(
                                    "ordine",
                                    "id",
                                    "matricola",
                                    "cognome",
                                    "nome",
                                    "funzione_it",
                                    "funzione_en",
                                )
                                .distinct(),
                                to_attr="components",
                            ),
                        ),
                        to_attr="cdsGroups",
                    ),
                )
                .only(
                    "regdid_id",
                    "aa_reg_did",
                    "frequenza_obbligatoria",
                    "cds__dip__dip_id",
                    "cds__dip__dip_cod",
                    "cds__dip__dip_des_it",
                    "cds__dip__dip_des_eng",
                    "cds__cds_id",
                    "cds__cds_cod",
                    "cds__cdsord_id",
                    "cds__nome_cds_it",
                    "cds__nome_cds_eng",
                    "cds__tipo_corso_cod",
                    "cds__tipo_corso_des",
                    "cds__cla_miur_cod",
                    "cds__cla_miur_des",
                    "cds__intercla_miur_cod",
                    "cds__intercla_miur_des",
                    "cds__durata_anni",
                    "cds__valore_min",
                    "cds__codicione",
                    "titolo_congiunto_cod",
                    "stato_regdid_cod",
                    "cds__area_cds",
                    "cds__area_cds_en",
                )
                .distinct()
                .annotate(
                    erogationMode=Subquery(
                        DidatticaRegolamento.objects.filter(
                            cds_id=OuterRef("cds__cds_id"), stato_regdid_cod__exact="A"
                        ).values("modalita_erogazione")[:1]
                    ),
                    ordinamento_didattico=Subquery(ordinamento_subquery),
                )
            )

            return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CdsDetailSerializer
        else:
            return CdsSerializer


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.STUDYACTIVITY_LIST_SUMMARY,
        description=descriptions.STUDYACTIVITY_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(
            StudyActivitiesListSerializer(many=True)
        ),
    ),
    retrieve=extend_schema(
        summary=descriptions.STUDYACTIVITY_RETRIEVE_SUMMARY,
        description=descriptions.STUDYACTIVITY_RETRIEVE_DESCRIPTION,
        responses=responses.COMMON_RETRIEVE_RESPONSES(StudyActivitiesDetailSerializer),
    ),
)


class StudyActivitiesViewSet(ReadOnlyModelViewSet, ClearResponseViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudyActivitiesFilter
    
    def get_queryset(self):
        queryset = (
            DidatticaAttivitaFormativaErogata.objects
            .select_related("mod_off_id")
            .select_related("mod_off_id__af_off")
            .select_related("mod_off_id__af_off__id_cds")
            .select_related("mod_off_id__af_off__id_cds__dip")
            .select_related("mod_off_id__doc_resp_mod_id_ab")
            .prefetch_related("pds")
        ).exclude(erog_id=-999999999).order_by('mod_off_id__ana_mod_cod')
        return queryset

    def get_object(self):
        # Prendiamo l'id passato nell'URL
        af_id = self.kwargs.get("pk")

        try:
            af_id = int(af_id)
        except (TypeError, ValueError):
            raise Http404()

        prefetch_coperture = Prefetch(
            'erog_id__coperture',
            queryset=DidatticaCopertura.objects
                .exclude(Q(stato_coper_cod="R") | Q(doc_id_ab=-999999999))
                .select_related('doc_id_ab')          
                .prefetch_related('dettaglio_ore'),
            to_attr='coperture_attive'
        )

        queryset_base = DidatticaAttivitaFormativaPds.objects.filter(
            erog_id__erog_id=af_id
        ).select_related(
            "id_cds", 
            "erog_id",
            "erog_id__mod_off_id__af_off",            
            "erog_id__mod_off_id__doc_tit_id_ab",
        ).prefetch_related(
            prefetch_coperture,
            'erog_id__testi'
        )

        results = list(queryset_base)

        if not results: raise Http404()

        erog_found = True
        result = results[0]

        # pds
        pds_list = []
        for r in results:
            pds_list.append(r.pds_desc_ita)
        result.pds = set(pds_list)

        # moduli
        result.moduli = DidatticaAttivitaFormativaPds.objects.none()
        erog_master_id = DidatticaAttivitaFormativaErogata.objects.filter(
            erog_master_id=af_id
        ).exclude(erog_id=af_id).values('erog_id').first()

        # mutuazioni
        if not erog_master_id:
            mutuazioni = []
        else:
            mutuazioni = list(
                DidatticaAttivitaFormativaErogata.objects.filter(
                    erog_id=erog_master_id['erog_id']
                )
            )
        result.mutuazioni = mutuazioni

        # mutuato da
        result.mutuato_da = None
        if not result.erog_id.master:
            result.mutuato_da = list(
            DidatticaAttivitaFormativaPds.objects.filter(
                erog_id=result.erog_id.erog_master_id
            ).select_related("id_cds", "erog_id").only(
                'af_pds_id', 'erog_id', 'erog_id__erog_master_id',
                'ana_mod_desc_ita', 'ana_mod_desc_eng',
                'pds_cod', 'pds_desc_ita', 'pds_desc_eng',
                'id_cds__nome_cds_it', 'id_cds__nome_cds_eng',
                'cds_cod',
                'erog_id__part_stu_desc_ita', 'erog_id__part_stu_desc_eng',
            )
        )
        
        result.erog_found = erog_found
        return result

    def get_serializer_class(self):
        if self.action == "retrieve":
            return StudyActivitiesDetailSerializer
        return StudyActivitiesListSerializer

    @staticmethod
    def _get_request_lang(request):
        url_lang = request.query_params.get('lang') or request.GET.get('lang')
        if url_lang:
            return url_lang.lower()
        
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        if accept_language:
            return accept_language.split(',')[0].split('-')[0].lower()
            
        return 'it'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        
            lang = request.query_params.get('lang', 'ita')
            pagination_envelope = {
                "data": serializer.data,
                "language": lang
            }
            return self.get_paginated_response(pagination_envelope)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        lang = self._get_request_lang(request)

        labels = {}
        for key in data.keys():
            label = LABEL_MAPPING.get(lang, {}).get(key) or LABEL_MAPPING.get(f"{lang}a" if lang=='it' else f"{lang}g", {}).get(key)
            if not label:
                label = LABEL_MAPPING.get('en', {}).get(key) or LABEL_MAPPING.get('eng', {}).get(key)
            if not label:
                label = LABEL_MAPPING.get('it', {}).get(key) or LABEL_MAPPING.get('ita', {}).get(key)
            labels[key] = label or key

        return Response({
            "results": data,
            "labels": labels
        })
    

class StudyActivitiesViewSetV1(StudyActivitiesViewSet, ClearResponseViewSet):
    pagination_class = UnicalStorageApiPaginationList
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return StudyActivitiesDetailSerializerV1
        return StudyActivitiesListSerializerV1
        
    
@extend_schema_view(
    list=extend_schema(
        summary=descriptions.ACADEMICPATHS_LIST_SUMMARY,
        description=descriptions.ACADEMICPATHS_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(
            AcademicPathwaysListSerializer(many=True)
        ),
        parameters=[
            OpenApiParameter(
                name="regdid_id",
                type=str,
                pattern=r"^\d+$",
                required=True,
                description="A unique value identifying the Didactic regulation.",
                location=OpenApiParameter.PATH,
            )
        ],
    ),
    retrieve=extend_schema(
        summary=descriptions.ACADEMICPATHS_RETRIEVE_SUMMARY,
        description=descriptions.ACADEMICPATHS_RETRIEVE_DESCRIPTION,
        responses=responses.COMMON_RETRIEVE_RESPONSES(AcademicPathwaysDetailSerializer),
        parameters=[
            OpenApiParameter(
                name="regdid_id",
                type=str,
                pattern=r"^\d+$",
                required=True,
                description="A unique value identifying the Didactic regulation.",
                location=OpenApiParameter.PATH,
            )
        ],
    ),
)


class AcademicPathwaysViewSet(ReadOnlyModelViewSet, ClearResponseViewSet):
    pagination_class = PageNumberPagination
    queryset = DidatticaPdsRegolamento.objects.all()
    lookup_field = "pds_regdid_id"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AcademicPathwaysDetailSerializer
        else:
            return AcademicPathwaysListSerializer

    def get_queryset(self):
        if self.action == "list":
            attivita_formativa_qs = DidatticaAttivitaFormativa.objects.filter(
                regdid=self.kwargs.get("regdid_id"),
                pds_regdid=OuterRef("pds_regdid_id"),
            ).select_related("regdid__cds")
            return (
                DidatticaPdsRegolamento.objects.filter(Exists(attivita_formativa_qs))
                .annotate(
                    duration=Subquery(
                        attivita_formativa_qs.values("regdid__cds__durata_anni")[:1]
                    )
                )
                .only("pds_regdid_id", "pds_cod", "regdid", "pds_des_it")
                .order_by("pds_des_it")
            )
        elif self.action == "retrieve":
            return (
                (DidatticaPdsRegolamento.objects)
                .filter(regdid=self.kwargs.get("regdid_id"))
                .prefetch_related(
                    Prefetch(
                        "didatticaattivitaformativa_set",
                        queryset=DidatticaAttivitaFormativa.objects.filter(
                            af_id=F("af_radice_id")
                        ),
                    )
                )
            )


class SortingContactsViewSet(ReadOnlyModelViewSet, ClearResponseViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = SortingContactsSerializer

    def get_queryset(self):
        last_year = datetime.date.today().year - 1
        current_year = datetime.date.today().year
        years = [last_year, current_year]

        return (
            DidatticaCopertura.objects.filter(
                Q(personale__flg_cessato=0, personale__fl_docente=1)
                | ~Q(stato_coper_cod="R"),
                cds_cod=self.kwargs.get("cdscod"),
                aa_off_id__in=years,
            )
            .only(
                "personale__nome",
                "personale__cognome",
                "personale__middle_name",
                "personale__matricola",
                "personale__cd_uo_aff_org",
                "personale__ds_aff_org",
            )
            .order_by("personale__cognome")
            .prefetch_related(
                Prefetch(
                    "personale__dipartimentourl_set",
                    queryset=DidatticaDipartimentoUrl.objects.only("dip_url"),
                    to_attr="dip_urls",
                )
            )
        )

        
class StudyPlansActivitiesViewSet(ReadOnlyModelViewSet, ClearResponseViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = StudyPlansActivitiesSerializer

    def get_queryset(self):
        regdid_id = str(self.kwargs["regdidid"])
        if regdid_id:

            piani_studio = (
                DidatticaPianiStudio.objects.filter(
                    regdid_id__regdid_id=regdid_id,
                )
                .select_related("regdid__cds")
                .prefetch_related(
                    # 1. Sostituiamo 'schemi' semplice con il Prefetch filtrato + to_attr
                    Prefetch(
                        "schemi",
                        queryset=DidatticaPianiSchema.objects.filter(
                            flag_schema_visibile_web='Si'
                        ).prefetch_related(
                            Prefetch(
                                'regole',
                                queryset=DidatticaPianiRegSce.objects.filter(
                                    tipo_reg_sce_cod__in=["O","F"]
                                ).prefetch_related('af'),
                                to_attr='regole_filtrate'
                            ),
                        ).order_by(
                            '-flag_schema_statutario',
                            'alt_part_time_cod',
                            'schema_piano_cod',
                        ),
                        to_attr="schemi_visibili",
                    )
                )
                .order_by("piano_studio_id")
            )

            set_af_pds_id = set()
            
            for p in piani_studio:
                for s in p.schemi_visibili:
                    for r in s.regole_filtrate:
                        for af in r.af.all():
                            if af.af_pds_id:  # Evitiamo valori None o vuoti (-99999 e #NULL# da gestire?)
                                set_af_pds_id.add(af.af_pds_id)
            
            tutte_le_attivita = VDidatticaAfPianiStudio.objects.filter(
                af_pds_id__in=list(set_af_pds_id)
            ).select_related('erog_id')

            map_activities = {}
            for act in tutte_le_attivita:
                map_activities.setdefault(act.af_pds_id, []).append(act)

            for p in piani_studio:
                for s in p.schemi_visibili:
                    for r in s.regole_filtrate:
                        for af in r.af.all():
                            af.activities = map_activities.get(
                                af.af_pds_id, []
                            )

                # ~ schede = sorted(
                    # ~ list(schede),
                    # ~ key=lambda k: (
                        # ~ k["cla_m_id"] if k["cla_m_id"] else 0,
                        # ~ -k["isStatutario"],
                        # ~ k["apt_id"] if k["apt_id"] else 0,
                    # ~ ),
                # ~ )
                # ~ q.PlanTabs = schemi

        return piani_studio


class StudyPlansActivitiesViewSetV1(StudyPlansActivitiesViewSet):
    serializer_class = StudyPlansActivitiesSerializerV1
        

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.STUDYPLANS_FULL_LIST_SUMMARY,
        description=descriptions.STUDYPLANS_FULL_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(StudyPlansActivitiesSerializer(many=True)),
    ),
)
class StudyPlansViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, ClearResponseViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = StudyPlansSerializer

    def get_queryset(self):
        cds_cod = self.kwargs.get("cds_cod")
        year = self.kwargs.get("year")

        if cds_cod and year: 
            query_cds = Q(regdid__cds_id__cds_cod=cds_cod)
            query_year = Q(aa_coorte_id=year)
            
            piani_studio = (
                DidatticaPianiStudio.objects.filter(
                    query_cds,
                    query_year,
                    stato_piano_studio_cod="A",
                )
                .select_related("regdid__cds")
                .prefetch_related(
                    Prefetch(
                        "schemi",
                        queryset=DidatticaPianiSchema.objects.filter(
                            flag_schema_visibile_web='Si'
                        ).order_by(
                            '-flag_schema_statutario',
                            'schema_piano_cod',
                            'alt_part_time_cod',
                        ),
                        to_attr="schemi_visibili",
                    ),
                    'schemi_visibili__regole',
                    'schemi_visibili__regole__af',
                    'schemi_visibili__regole__blocchi',
                    'schemi_visibili__regole__blocchi__af_blocco'
                )
                .order_by("piano_studio_id")
            )

            set_af_pds_id = set()

            for p in piani_studio:
                for s in p.schemi_visibili:
                    for r in s.regole.all():
                        for af in r.af.all():
                            if is_nullable(af.af_pds_id):
                                set_af_pds_id.add(af.af_pds_id)

            tutte_le_attivita = VDidatticaAfPianiStudio.objects.filter(
                af_pds_id__in=set_af_pds_id
            ).select_related('erog_id')
            
            map_activities = {}
            for act in tutte_le_attivita:
                map_activities.setdefault(act.af_pds_id, []).append(act)
                
            for p in piani_studio:
                for s in p.schemi_visibili:
                    for r in s.regole.all():
                        for af in r.af.all():
                            af.activities = map_activities.get(
                                af.af_pds_id, []
                            )
                        for bl in r.blocchi.all():
                            for blaf in bl.af_blocco.all():
                                blaf.activities = map_activities.get(
                                    blaf.af_pds_id, []
                                )
            
            # ~ schede = sorted(
                # ~ list(schede),
                # ~ key=lambda k: (
                    # ~ k["cla_m_id"] if k["cla_m_id"] else 0,
                    # ~ -k["isStatutario"],
                    # ~ k["apt_id"] if k["apt_id"] else 0,
                # ~ ),
            # ~ )
            # ~ q.PlanTabs = schemi
        return piani_studio


class StudyPlansViewSetV1(StudyPlansViewSet):
    serializer_class = StudyPlansSerializerV1
