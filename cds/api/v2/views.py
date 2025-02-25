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
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from organizational_area.models import OrganizationalStructureOfficeEmployee
from cds.settings import OFFICE_CDS, OFFICE_CDS_DOCUMENTS, OFFICE_CDS_TEACHING_SYSTEM

from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from structures.models import DidatticaDipartimentoUrl
from cds.models import (
    DidatticaAttivitaFormativa,
    DidatticaCds,
    DidatticaCdsAltriDati,
    DidatticaCdsCollegamento,
    DidatticaCopertura,
    DidatticaPdsRegolamento,
    DidatticaRegolamento,
    DidatticaTestiRegolamento,
    DidatticaRegolamentoAltriDati,
    DidatticaCdsLingua,
    DidatticaCdsAltriDatiUfficio,
    DidatticaCdsGruppi,
    DidatticaCdsGruppiComponenti
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
    SortingContactsSerializer
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
class DegreeTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
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
class AcademicYearsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
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
class CdsAreasViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
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
class CdsExpiredViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CdsExpiredSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CdsExpiredFilter
    queryset = DidatticaRegolamento.objects.all()

    def get_queryset(self):
        cds_morphed = DidatticaCdsCollegamento.objects.values_list(
            "cds_prec__cds_cod", flat=True
        )
        return (DidatticaRegolamento.objects.filter(
                ~Exists(
                    DidatticaRegolamento.objects.filter(
                        cds=OuterRef("cds"),
                        aa_reg_did__gt=OuterRef("aa_reg_did"),
                    ).exclude(stato_regdid_cod="R")
                ),
                aa_reg_did__lt=settings.CURRENT_YEAR,
            )
            .exclude(stato_regdid_cod="R")
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
class CdsMorphViewSet(ReadOnlyModelViewSet):
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
        cds = (
            DidatticaCds.objects.filter(cds_cod=cds_cod).order_by("-cds_id").first()
        )

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
class CdsViewSet(ReadOnlyModelViewSet):
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
                        queryset=DidatticaCdsLingua.objects.only("lingua_des_it", "lingua_des_eng").distinct(),
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
            
            queryset = (DidatticaRegolamento.objects.select_related("cds__dip")
                .prefetch_related(
                    Prefetch(
                        "cds__didatticacdslingua",
                        queryset=DidatticaCdsLingua.objects.only("lingua_des_it", "lingua_des_eng").distinct(),
                        to_attr="lingue",
                    ),
                    Prefetch(
                        "didatticatestiregolamento_set",
                        queryset=DidatticaTestiRegolamento.objects.only(
                            "regdid_id",
                            "clob_txt_ita",
                            "clob_txt_eng",
                            "testo_regdid_url",
                            "tipo_testo_regdid_cod",
                            "profilo",
                            "profilo_eng",
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
                        to_attr="officesData"
                    ),
                    Prefetch(
                        "cds__didatticacdsgruppi_set",
                        queryset=DidatticaCdsGruppi.objects.filter(query_visibile).only(
                            "ordine",
                            "id",
                            "descr_breve_it",
                            "descr_breve_en",
                            "descr_lunga_it",
                            "descr_lunga_en",
                        ).distinct()
                        .prefetch_related(
                            Prefetch(
                                "didatticacdsgruppicomponenti_set",
                                queryset=DidatticaCdsGruppiComponenti.objects.filter(query_visibile).only(
                                    "ordine",
                                    "id",
                                    "matricola",
                                    "cognome",
                                    "nome",
                                    "funzione_it",
                                    "funzione_en",
                                ).distinct(),
                                to_attr="components"
                            ),
                        ),
                        to_attr="cdsGroups"
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
                    erogationMode = Subquery(
                            DidatticaRegolamento.objects.filter(cds_id=OuterRef("cds__cds_id"), stato_regdid_cod__exact="A").values("modalita_erogazione")[:1]
                        ),
                    ordinamento_didattico=Subquery(ordinamento_subquery)
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
class StudyActivitiesViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudyActivitiesFilter
    queryset = DidatticaAttivitaFormativa.objects.all()

    # def get_submodules(self, af_id):
    #     return (DidatticaAttivitaFormativa.objects.filter(Q(af_radice_id=af_id) | Q(af_pdr_id=af_id))
    #             .exclude(af_id=af_id)
    #             .values(
    #                 "af_id",
    #                 "af_gen_cod",
    #                 "des",
    #                 "af_gen_des_eng",
    #                 "fat_part_stu_cod",
    #                 "lista_lin_did_af",
    #                 "part_stu_cod",
    #                 "part_stu_des",
    #                 "fat_part_stu_des",
    #                 "ciclo_des",
    #                 "matricola_resp_did",
    #             )
    #     )
    
    # def get_mutuata_da(self, id_master):
    #     return (DidatticaAttivitaFormativa.objects.filter(af_id=id_master)
    #         .values(
    #             "af_id",
    #             "af_gen_cod",
    #             "des",
    #             "cds__cds_cod",
    #             "cds__cds_id",
    #             "cds__nome_cds_it",
    #             "cds__nome_cds_eng",
    #             "pds_cod",
    #             "pds_des",
    #             "af_gen_des_eng",
    #             "ciclo_des",
    #             "regdid__regdid_id",
    #             "regdid__aa_reg_did",
    #             "anno_corso",
    #             "didatticacopertura__coper_peso",
    #         )
    #         .first()
    #     )
    # def get_mutuata_da_questa(self, af_id):
    #     return (DidatticaAttivitaFormativa.objects.filter(af_master_id=af_id, mutuata_flg=1)
    #         .exclude(af_id=af_id)
    #         .values(
    #             "af_id",
    #             "af_gen_cod",
    #             "des",
    #             "af_gen_des_eng",
    #             "ciclo_des",
    #             "regdid__regdid_id",
    #             "regdid__aa_reg_did",
    #             "anno_corso",
    #             "didatticacopertura__coper_peso",
    #             "cds__cds_cod",
    #             "cds__cds_id",
    #             "cds__nome_cds_it",
    #             "cds__nome_cds_eng",
    #             "pds_cod",
    #             "pds_des",
    #         )
    #     )
    
    # def get_activity_root(self, af_id, id_radice):
    #     activity_root = (DidatticaAttivitaFormativa.objects.filter(af_id=id_radice)
    #         .exclude(af_id=af_id)
    #         .values(
    #             "af_id",
    #             "af_gen_cod",
    #             "des",
    #             "af_gen_des_eng",
    #             "ciclo_des",
    #             "regdid__regdid_id",
    #             "regdid__aa_reg_did",
    #             "anno_corso",
    #             "didatticacopertura__coper_peso",
    #             "cds__cds_cod",
    #             "cds__cds_id",
    #             "cds__nome_cds_it",
    #             "cds__nome_cds_eng",
    #             "pds_cod",
    #             "pds_des",
    #         ).first()
    #     )
    #     return None if len(activity_root) == 0 else activity_root
    
    # def get_activity_father(self, af_id, id_radice_padre):
    #     activity_father =  (
    #             DidatticaAttivitaFormativa.objects.filter(af_id=id_radice_padre)
    #             .exclude(af_id=af_id)
    #             .values(
    #                 "af_id",
    #                 "af_gen_cod",
    #                 "des",
    #                 "af_gen_des_eng",
    #                 "ciclo_des",
    #                 "regdid__regdid_id",
    #                 "regdid__aa_reg_did",
    #                 "anno_corso",
    #                 "didatticacopertura__coper_peso",
    #                 "cds__cds_cod",
    #                 "cds__cds_id",
    #                 "cds__nome_cds_it",
    #                 "cds__nome_cds_eng",
    #                 "pds_cod",
    #                 "pds_des",
    #             )
    #         )
    #     return None if len(activity_father) == 0 else activity_father
    
    # def get_copertura(self, af_id):
    #     return DidatticaCopertura.objects.filter(af_id=af_id).values(
    #             "personale__id",
    #             "personale__id_ab",
    #             "personale__nome",
    #             "personale__cognome",
    #             "personale__middle_name",
    #             "personale__matricola",
    #             "fat_part_stu_cod",
    #             "fat_part_stu_des",
    #             "part_stu_cod",
    #             "part_stu_des",
    #         )
        
    # def get_filteredHours(self, af_id):
    #     filtered_hours = DidatticaCoperturaDettaglioOre.objects.filter(
    #         ~Q(coper_id__stato_coper_cod="R"), coper_id__af_id=af_id
    #     ).values(
    #         "tipo_att_did_cod",
    #         "ore",
    #         "coper_id__personale_id__id_ab",
    #         "coper_id__personale_id__matricola",
    #         "coper_id__personale_id__nome",
    #         "coper_id__personale_id__cognome",
    #         "coper_id__personale_id__middle_name",
    #         "coper_id__personale_id__flg_cessato",
    #         "coper_id",
    #     )
        
    #     aggregated_hours = {}

    #     for hour in filtered_hours:
    #         key = (hour["tipo_att_did_cod"], hour["coper_id__personale_id__matricola"])

    #         if key in aggregated_hours:
    #             aggregated_hours[key]["ore"] += hour["ore"]
    #         else:
    #             aggregated_hours[key] = hour.copy() 
                    
    #     return list(aggregated_hours.values())
    
    # def get_modalities(self, af_id):
    #     return DidatticaAttivitaFormativaModalita.objects.filter(
    #         af_id=af_id
    #     ).values("mod_did_af_id", "mod_did_cod", "mod_did_des")
    
    # def get_get_texts(self, af_id):
    #     return DidatticaTestiAf.objects.filter(af_id=af_id).values(
    #         "tipo_testo_af_cod", "testo_af_ita", "testo_af_eng"
    #     )
        
        
    def get_queryset(self):
        if self.action == "list":
            coperture_qs = DidatticaCopertura.objects.filter(
                af_id=OuterRef("af_id")
            ).values("af_gen_cod", "anno_corso", "ciclo_des")[:1]

            queryset = (
                DidatticaAttivitaFormativa.objects.select_related(
                    "cds__dip", "matricola_resp_did"
                )
                .only(
                    "af_id",
                    "af_gen_cod",
                    "af_gen_des_eng",
                    "cds_id",
                    "cds__cds_cod",
                    "des",
                    "lista_lin_did_af",
                    "af_radice_id",
                    "regdid_id",
                    "cds__dip__dip_des_it",
                    "cds__dip__dip_des_eng",
                    "cds__dip__dip_cod",
                    "anno_corso",
                    "aa_off_id",
                    "ciclo_des",
                    "sett_cod",
                    "sett_des",
                    "part_stu_cod",
                    "part_stu_des",
                    "fat_part_stu_cod",
                    "fat_part_stu_des",
                    "cds__nome_cds_it",
                    "cds__nome_cds_eng",
                    "matricola_resp_did__matricola",
                    "matricola_resp_did__cognome",
                    "matricola_resp_did__nome",
                    "matricola_resp_did__middle_name",
                    "pds_des",
                )
                .annotate(
                    full_name=Case(
                        When(
                            matricola_resp_did__cognome__isnull=True,
                            matricola_resp_did__nome__isnull=True,
                            matricola_resp_did__middle_name__isnull=True,
                            then=Value(""),
                        ),
                        default=Concat(
                            F("matricola_resp_did__cognome"),
                            Value(" "),
                            F("matricola_resp_did__nome"),
                            Case(
                                When(
                                    matricola_resp_did__middle_name__isnull=False,
                                    then=Concat(
                                        Value(" "),
                                        F("matricola_resp_did__middle_name"),
                                    ),
                                ),
                                default=Value(""),
                                output_field=models.CharField(),
                            ),
                            output_field=models.CharField(),
                        ),
                    ),
                    group_description=Concat(
                        F("des"),
                        Case(
                            When(
                                part_stu_des__isnull=False,
                                then=Concat(Value(" ("), F("part_stu_des"), Value(")")),
                            )
                        ),
                        output_field=models.CharField(),
                    ),
                    fatherName=F("des"),
                    af_gen_cod_final=Coalesce(
                        F("af_gen_cod"),
                        Subquery(coperture_qs.values("af_gen_cod")),
                        output_field=models.CharField(),
                    ),
                    anno_corso_final=Coalesce(
                        F("anno_corso"),
                        Subquery(coperture_qs.values("anno_corso")),
                        output_field=models.IntegerField(),
                    ),
                    ciclo_des_final=Coalesce(
                        F("ciclo_des"),
                        Subquery(coperture_qs.values("ciclo_des")),
                        output_field=models.CharField(),
                    ),
                )
                .filter(
                    Q(
                        af_id__in=Subquery(
                            DidatticaCopertura.objects.filter(
                                ~Q(stato_coper_cod="R") | Q(stato_coper_cod__isnull=True)
                            ).values("af_id")
                        )
                    )
                    | Q(
                        af_master_id__in=Subquery(
                            DidatticaCopertura.objects.filter(
                                ~Q(stato_coper_cod="R") | Q(stato_coper_cod__isnull=True)
                            ).values("af_id")
                        )
                    )
                )
                .order_by("des")
            )
            return queryset
        
        if self.action == "retrieve":  
            af_id = self.kwargs.get("af_id")
            queryset = (
                DidatticaAttivitaFormativa.objects.filter(af_id=af_id)
                .prefetch_related(
                    Prefetch(
                        "didatticaattivitaformativa_set",
                        queryset= DidatticaAttivitaFormativa.objects.filter(af_id=OuterRef("af_radice_id"))
                        .only(
                            "af_id",
                            "af_gen_cod",
                            "des",
                            "af_gen_des_eng",
                            "ciclo_des",
                            "regdid__regdid_id",
                            "regdid__aa_reg_did",
                            "anno_corso",
                            "didatticacopertura__coper_peso",
                            "cds__cds_cod",
                            "cds__cds_id",
                            "cds__nome_cds_it",
                            "cds__nome_cds_eng",
                            "pds_cod",
                            "pds_des",
                        ),
                        to_attr="activityRoot"
                    ),
                    Prefetch(
                        "didatticaattivitaformativa_set",
                        queryset= DidatticaAttivitaFormativa.objects.filter(
                            af_radice_id=OuterRef(af_id), af_pdr_id=OuterRef(af_id)
                        )
                        .exclude(af_id=af_id)
                        .only(
                            "af_id",
                            "af_gen_cod",
                            "des",
                            "af_gen_des_eng",
                            "fat_part_stu_cod",
                            "lista_lin_did_af",
                            "part_stu_cod",
                            "part_stu_des",
                            "fat_part_stu_des",
                            "ciclo_des",
                            "matricola_resp_did",
                        ),
                        to_attr="modules"
                    ),
                )
                .order_by('anno_corso', 'ciclo_des')
                .values(
                    "af_id",
                    "af_gen_cod",
                    "des",
                    "af_gen_des_eng",
                    "cds__cds_cod",
                    "cds__cds_id",
                    "lista_lin_did_af",
                    "pds_cod",
                    "pds_des",
                    "regdid__regdid_id",
                    "regdid__aa_reg_did",
                    "anno_corso",
                    "ciclo_des",
                    "peso",
                    "sett_cod",
                    "sett_des",
                    "freq_obblig_flg",
                    "cds__nome_cds_it",
                    "cds__nome_cds_eng",
                    "tipo_af_des",
                    "tipo_af_cod",
                    "tipo_af_intercla_cod",
                    "tipo_af_intercla_des",
                    "matricola_resp_did",
                    "mutuata_flg",
                    "af_master_id",
                    "af_radice_id",
                    "af_pdr_id",
                    "didatticacopertura__coper_peso",
                    "part_stu_cod",
                    "fat_part_stu_cod",
                    "part_stu_des",
                    "fat_part_stu_des",
                    
                    "mutuata_flg",
                    "af_master_id",
                    
                )
                .annotate(
                    full_name=Case(
                        When(
                            matricola_resp_did__cognome__isnull=True,
                            matricola_resp_did__nome__isnull=True,
                            matricola_resp_did__middle_name__isnull=True,
                            then=Value(""),
                        ),
                        default=Concat(
                            F("matricola_resp_did__cognome"),
                            Value(" "),
                            F("matricola_resp_did__nome"),
                            Case(
                                When(
                                    matricola_resp_did__middle_name__isnull=False,
                                    then=Concat(
                                        Value(" "),
                                        F("matricola_resp_did__middle_name"),
                                    ),
                                ),
                                default=Value(""),
                                output_field=models.CharField(),
                            ),
                            output_field=models.CharField(),
                        ),
                    ),
                    group_description=Concat(
                        F("des"),
                        Case(
                            When(
                                part_stu_des__isnull=False,
                                then=Concat(Value(" ("), F("part_stu_des"), Value(")")),
                            )
                        ),
                        output_field=models.CharField(),
                    ),
                )
                
                    
            )
            # list_submodules = self.get_submodules(af_id)
            
            # if queryset.first()["mutuata_flg"] == 1:
            #     id_master = queryset.first()["af_master_id"]
            #     mutuata_da = self.get_mutuata_da(id_master)
                
            # attivita_mututate_da_questa = self.get_mutuata_da_questa(af_id)
            
            # radice = queryset.first()
            # id_radice_padre = radice["af_pdr_id"]
            # id_radice = radice["af_radice_id"]
            
            # activity_root = self.get_activity_root(af_id, id_radice)

            # if id_radice_padre and id_radice_padre != id_radice:
            #     activity_father = self.get_activity_father(af_id, id_radice_padre)
                    
            # copertura = self.get_copertura(af_id)
            
            # filtered_hours = self.get_filteredHours(af_id)
            
            # append_email_addresses(filtered_hours, "coper_id__personale_id__id_ab")
            
            # texts = self.get_texts(af_id)
            # modalities = self.get_modalities(af_id)
            
            
            
            
    def get_serializer_class(self):
        if self.action == "retrieve":
            return StudyActivitiesDetailSerializer
        else:
            return StudyActivitiesListSerializer

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
class AcademicPathwaysViewSet(ReadOnlyModelViewSet):
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

class SortingContactsViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = SortingContactsSerializer
    
    last_year = datetime.date.today().year - 1
    current_year = datetime.date.today().year
    years = [last_year, current_year]
    
    queryset = DidatticaCopertura.objects.all()

    def retrieve(self, request, *args, **kwargs):
        return (self.queryset.filter(
                        Q(personale__flg_cessato=0, personale__fl_docente=1) | 
                        ~Q(stato_coper_cod="R"),
                        cds_cod=self.kwargs.get("cdscod"),
                        aa_off_id__in=self.years,
                    )
                    .values(
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
