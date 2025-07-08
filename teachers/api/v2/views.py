import datetime
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from .docs import descriptions
from api_docs import responses

from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import mixins, viewsets
from addressbook.utils import append_email_addresses, get_personale_matricola
from organizational_area.models import OrganizationalStructureOfficeEmployee
from research_lines.settings import OFFICE_RESEARCH_LINES
from .filters import (
    TeachersFilter,
    CoveragesFilter,
    TeachersStudyActivitiesFilter,
    TeachersMaterialsFilter,
    TeachersNewsFilter,
    PublicationFilter
)
from .serializers import (
    TeachersSerializer,
    TeacherSerializer,
    PublicationsSerializer,
    PublicationSerializer,
    TeachersStudyActivitiesSerializer,
    TeachersMaterialsSerializer,
    PublicationsCommunityTypesSerializer,
    TeachersBaseResearchLinesSerializer,
    TeachersAppliedResearchLinesSerializer,
    TeachersNewsSerializer
)

from django.db.models import Q, OuterRef, F,Prefetch
from structures.models import DidatticaDipartimento, UnitaOrganizzativaFunzioni
from addressbook.models import Personale, PersonaleContatti
from teachers.models import (
    DocenteMaterialeDidattico,
    DocentePtaBacheca,
    PubblicazioneAutori,
    PubblicazioneCommunity,
    PubblicazioneDatiBase,
)
from cds.models import DidatticaCopertura
import teachers.utils


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.TEACHERS_LIST_SUMMARY,
        description=descriptions.TEACHERS_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(TeachersSerializer(many=True)),
    ),
    retrieve=extend_schema(
        summary=descriptions.TEACHERS_RETRIEVE_SUMMARY,
        description=descriptions.TEACHERS_RETRIEVE_DESCRIPTION,
        responses=responses.COMMON_RETRIEVE_RESPONSES(TeacherSerializer),
    ),
)
class TeachersViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeachersFilter
    lookup_field = "matricola"

    def get_serializer_class(self):
        return TeacherSerializer if self.action == "retrieve" else TeachersSerializer

    def get_queryset(self):
        if self.action == "list":
            return (
                Personale.objects.filter(
                    Q(fl_docente=1)
                    | (
                        Q(didatticacopertura__af__isnull=False)
                        & ~Q(didatticacopertura__stato_coper_cod="R")
                    )
                )
                .only(
                    "id_ab",
                    "cod_fis",
                    "matricola",
                    "nome",
                    "middle_name",
                    "cognome",
                    "cd_ruolo",
                    "ds_ruolo_locale",
                    "cd_ssd",
                    "cd_uo_aff_org",
                    "ds_ssd",
                    "cv_full_it",
                    "cv_short_it",
                    "cv_full_eng",
                    "cv_short_eng",
                    "profilo",
                    "ds_profilo",
                    "ds_profilo_breve",
                )
                .order_by("cognome", "nome", "middle_name")
                .distinct()
            )

        if self.action == "retrieve":
            teacher = get_personale_matricola(self.kwargs.get("matricola"))

            return (
                Personale.objects.filter(
                    Q(fl_docente=1, flg_cessato=0)
                    | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year)
                    & ~Q(didatticacopertura__stato_coper_cod="R")
                    | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1)
                    & ~Q(didatticacopertura__stato_coper_cod="R"),
                    matricola=teacher,
                )
                .select_related("docente_pta_altri_dati")
                .prefetch_related(
                    Prefetch(
                        "unitaorganizzativafunzioni_set",
                        queryset=(
                            UnitaOrganizzativaFunzioni.objects.filter(
                                termine__gt=datetime.datetime.now(),
                                decorrenza__lt=datetime.datetime.now(),
                            ).select_related("cd_csa")
                        ),
                        to_attr="functions",
                    ),
                    Prefetch(
                        "personalecontatti",
                        queryset=PersonaleContatti.objects.select_related(
                            "cd_tipo_cont"
                        ),
                        to_attr="contatti",
                    ),
                )
                .only(
                    "id_ab",
                    "matricola",
                    "nome",
                    "middle_name",
                    "cognome",
                    "cd_ruolo",
                    "ds_ruolo_locale",
                    "cd_ssd",
                    "ds_ssd",
                    "cd_uo_aff_org",
                    "ds_aff_org",
                    "telrif",
                    "email",
                    "cv_full_it",
                    "cv_short_it",
                    "cv_full_eng",
                    "cv_short_eng",
                    "profilo",
                    "ds_profilo",
                    "ds_profilo_breve",
                )
                .distinct()
            )

    def get_object(self):
        return self.get_queryset().first()

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.COVERAGES_LIST_SUMMARY,
        description=descriptions.COVERAGES_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(TeachersSerializer(many=True)),
    ),
)
class CoveragesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = TeachersSerializer
    filterset_class = CoveragesFilter

    def get_queryset(self):
        dip_des_it_subquery = DidatticaDipartimento.objects.filter(
            dip_cod=OuterRef("cd_uo_aff_org")
        ).values("dip_des_it")[:1]

        dip_des_eng_subquery = DidatticaDipartimento.objects.filter(
            dip_cod=OuterRef("cd_uo_aff_org")
        ).values("dip_des_eng")[:1]

        dip_id_subquery = DidatticaDipartimento.objects.filter(
            dip_cod=OuterRef("cd_uo_aff_org")
        ).values("dip_id")[:1]

        dip_cod_subquery = DidatticaDipartimento.objects.filter(
            dip_cod=OuterRef("cd_uo_aff_org")
        ).values("dip_cod")[:1]

        query = (
            Personale.objects.filter(didatticacopertura__af__isnull=False)
            .exclude(didatticacopertura__stato_coper_cod="R")
            .annotate(
                dip_id=dip_id_subquery,
                dip_cod=dip_cod_subquery,
                dip_des_it=dip_des_it_subquery,
                dip_des_eng=dip_des_eng_subquery,
            )
            .values(
                "id_ab",
                "matricola",
                "nome",
                "middle_name",
                "cognome",
                "cd_ruolo",
                "ds_ruolo_locale",
                "cd_ssd",
                "cd_uo_aff_org",
                "ds_ssd",
                "cv_full_it",
                "cv_short_it",
                "cv_full_eng",
                "cv_short_eng",
                "profilo",
                "ds_profilo",
                "ds_profilo_breve",
            )
            .order_by("cognome", "nome", "middle_name")
            .distinct()
        )

        append_email_addresses(query, "id_ab")

        return query

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.PUBLICATIONS_LIST_SUMMARY,
        description=descriptions.PUBLICATIONS_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(PublicationsSerializer(many=True)),
    ),
    retrieve=extend_schema(
        summary=descriptions.PUBLICATIONS_RETRIEVE_SUMMARY,
        description=descriptions.PUBLICATIONS_RETRIEVE_DESCRIPTION,
        responses=responses.COMMON_RETRIEVE_RESPONSES(PublicationSerializer),
    ),
)
class PublicationsViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = PublicationsSerializer
    filterset_class = PublicationFilter

    def get_serializer_class(self):
        return (
            PublicationsSerializer if self.action == "list" else PublicationSerializer
        )

    def get_queryset(self):
        if self.action == "list":
            return (
                PubblicazioneDatiBase.objects.select_related("collection")
                .only(
                    "item_id",
                    "title",
                    "des_abstract",
                    "des_abstracteng",
                    "collection_id__collection_name",
                    "collection_id__community_id__community_name",
                    "pubblicazione",
                    "label_pubblicazione",
                    "contributors",
                    "date_issued_year",
                    "url_pubblicazione",
                )
                .order_by(
                    "-date_issued_year",
                    "collection_id__community_id__community_name",
                    "title",
                )
                .distinct()
            )
        if self.action == "retrieve":
            return (
                PubblicazioneDatiBase.objects.select_related("collection")
                .prefetch_related(
                    Prefetch(
                        "pubblicazioneautori",
                        queryset=PubblicazioneAutori.objects.only(
                            "ab__id_ab",
                            "ab__nome",
                            "ab__cognome",
                            "ab__middle_name",
                            "ab__matricola",
                            "first_name",
                            "last_name",
                        ),
                        to_attr="autori",
                    )
                )
                .only(
                    "item_id",
                    "title",
                    "des_abstract",
                    "des_abstracteng",
                    "collection_id__collection_name",
                    "collection_id__community_id__community_name",
                    "pubblicazione",
                    "label_pubblicazione",
                    "contributors",
                    "date_issued_year",
                    "url_pubblicazione",
                )
                .order_by(
                    "-date_issued_year",
                    "collection_id__community_id__community_name",
                    "title",
                )
                .distinct()
            )

@extend_schema_view(
    retrieve=extend_schema(
        summary=descriptions.TEACHERS_STUDY_ACTIVITY_RETRIEVE_SUMMARY,
        description=descriptions.TEACHERS_STUDY_ACTIVITY_RETRIEVE_DESCRIPTION,
        responses=responses.COMMON_RETRIEVE_RESPONSES(TeachersStudyActivitiesSerializer),
    ),
)
class TeachersStudyActivitiesViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = TeachersStudyActivitiesSerializer
    filterset_class = TeachersStudyActivitiesFilter
    lookup_field = "matricola"

    def get_queryset(self):
        teacher = get_personale_matricola(self.kwargs.get("matricola"))

        queryset = (
            DidatticaCopertura.objects.filter(
                personale__matricola__exact=teacher, af__isnull=False
            )
            .select_related("personale", "af")
            .order_by("aa_off_id", "anno_corso", "af_gen_des", "af_gen_des_eng")
            .only(
                "personale__matricola",
                "af_id",
                "af_gen_cod",
                "af_gen_des",
                "af_gen_des_eng",
                "regdid_id",
                "anno_corso",
                "ciclo_des",
                "peso",
                "sett_des",
                "af__freq_obblig_flg",
                "cds_des",
                "af__cds__nome_cds_eng",
                "af__lista_lin_did_af",
                "aa_off_id",
                "cds_id",
                "cds_cod",
                "fat_part_stu_des",
                "fat_part_stu_cod",
                "part_stu_des",
                "part_stu_cod",
                "tipo_fat_stu_cod",
                "part_ini",
                "part_fine",
                "coper_peso",
                "ore",
            )
            .order_by("-aa_off_id")
        )

        single_id = []
        to_exclude = []

        for cop in queryset:
            if cop.af_id not in single_id:
                single_id.append(cop.af_id)
            else:
                to_exclude.append(cop.coper_id)
        return queryset.exclude(coper_id__in=to_exclude)

    def get_object(self):
        return self.get_queryset().first()

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.TEACHERS_MATERIALS_LIST_SUMMARY,
        description=descriptions.TEACHERS_MATERIALS_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(TeachersMaterialsSerializer(many=True)),
    ),
)
class TeachersMaterialsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = TeachersMaterialsSerializer
    filterset_class = TeachersMaterialsFilter

    def get_queryset(self):
        teacher = get_personale_matricola(self.kwargs.get("id"))
        user = self.request.user

        query_is_active = Q(attivo=True)
        query_is_started = Q(dt_inizio_validita__isnull=True) | Q(
            dt_inizio_validita__lte=datetime.datetime.now()
        )
        query_is_end = Q(dt_fine_validita__isnull=True) | Q(
            dt_fine_validita__gt=datetime.datetime.now()
        )

        if teachers.utils.can_manage_teacher(user, teacher):
            query_is_active = Q()
            query_is_started = Q()
            query_is_end = Q()

        return (
            DocenteMaterialeDidattico.objects.filter(
                query_is_active,
                query_is_started,
                query_is_end,
                matricola__exact=teacher,
            )
            .only(
                "id",
                "titolo",
                "titolo_en",
                "testo",
                "testo_en",
                "url_testo",
                "url_testo_en",
                "ordine",
                "attivo",
                "dt_pubblicazione",
                "dt_inizio_validita",
                "dt_fine_validita",
            )
            .annotate(
                docenteRiferimentoId=F("matricola"),
            )
        )

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.TEACHERS_BASE_RESEARCH_LINES_LIST_SUMMARY,
        description=descriptions.TEACHERS_BASE_RESEARCH_LINES_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(TeachersBaseResearchLinesSerializer(many=True)),
    ),
)
class TeachersBaseResearchLinesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = TeachersBaseResearchLinesSerializer

    def get_queryset(self):
        only_active = True
        request = self.request
        if request.user.is_superuser:
            only_active = False  # pragma: no cover
        if request.user.is_authenticated:  # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__name=OFFICE_RESEARCH_LINES,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            if my_offices.exists():
                only_active = False

        teacher_id = get_personale_matricola(self.kwargs.get("id"))

        query_is_active_base = (
            Q(ricercadocentelineabase__ricerca_linea_base__visibile=True)
            if only_active
            else Q()
        )

        return (
            Personale.objects.filter(
                query_is_active_base,
                matricola__exact=teacher_id,
                fl_docente=1,
                ricercadocentelineabase__dt_fine__isnull=True,
            )
            .order_by("ricercadocentelineabase__ricerca_linea_base__id")
            .values(
                "ricercadocentelineabase__ricerca_linea_base__id",
                "ricercadocentelineabase__ricerca_linea_base__descrizione",
                "ricercadocentelineabase__ricerca_linea_base__descr_pubblicaz_prog_brevetto",
                "ricercadocentelineabase__ricerca_linea_base__ricerca_erc2__ricerca_erc1__ricerca_erc0_cod__erc0_cod",
                "ricercadocentelineabase__ricerca_linea_base__ricerca_erc2__ricerca_erc1__ricerca_erc0_cod__description",
            )
            .exclude(ricercadocentelineabase__ricerca_linea_base__id__isnull=True)
            .distinct()
        )
        
    def get_object(self):
        return self.get_queryset().first()

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.TEACHERS_APPLIED_RESEARCH_LINES_LIST_SUMMARY,
        description=descriptions.TEACHERS_APPLIED_RESEARCH_LINES_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(TeachersAppliedResearchLinesSerializer(many=True)),
    ),
)
class TeachersAppliedResearchLinesViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = TeachersAppliedResearchLinesSerializer

    def get_queryset(self):
        only_active = True
        request = self.request
        if request.user.is_superuser:
            only_active = False  # pragma: no cover
        if request.user.is_authenticated:  # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__name=OFFICE_RESEARCH_LINES,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            if my_offices.exists():
                only_active = False

        teacher_id = get_personale_matricola(self.kwargs.get("matricola"))

        query_is_active_app = (
            Q(ricercadocentelineaapplicata__ricerca_linea_applicata__visibile=True)
            if only_active
            else Q()
        )

        return (
            Personale.objects.filter(
                query_is_active_app,
                matricola__exact=teacher_id,
                fl_docente=1,
                ricercadocentelineaapplicata__dt_fine__isnull=True,
            )
            .order_by("ricercadocentelineaapplicata__ricerca_linea_applicata__id")
            .exclude(
                ricercadocentelineaapplicata__ricerca_linea_applicata__id__isnull=True
            )
            .values(
                "ricercadocentelineaapplicata__ricerca_linea_applicata__id",
                "ricercadocentelineaapplicata__ricerca_linea_applicata__descrizione",
                "ricercadocentelineaapplicata__ricerca_linea_applicata__descr_pubblicaz_prog_brevetto",
                "ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__erc0_cod",
                "ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__description",
            )
            .distinct()
        )

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.TEACHERS_NEWS_LIST_SUMMARY,
        description=descriptions.TEACHERS_NEWS_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(TeachersNewsSerializer(many=True)),
    ),
)
class TeachersNewsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = TeachersNewsSerializer
    filterset_class = TeachersNewsFilter

    def get_queryset(self):
        teacher = get_personale_matricola(self.kwargs.get("id"))
        user = self.request.user

        query_is_active = Q(attivo=True)
        query_is_started = Q(dt_inizio_validita__isnull=True) | Q(
            dt_inizio_validita__lte=datetime.datetime.now()
        )
        query_is_end = Q(dt_fine_validita__isnull=True) | Q(
            dt_fine_validita__gt=datetime.datetime.now()
        )

        if teachers.utils.can_manage_teacher(user, teacher):
            query_is_active = Q()
            query_is_started = Q()
            query_is_end = Q()

        return DocentePtaBacheca.objects.filter(
            query_is_active,
            query_is_started,
            query_is_end,
            matricola__exact=teacher,
        ).only(
            "id",
            "tipo_testo",
            "tipo_testo_en",
            "titolo",
            "titolo_en",
            "testo",
            "testo_en",
            "url_testo",
            "url_testo_en",
            "ordine",
            "attivo",
            "dt_pubblicazione",
            "dt_inizio_validita",
            "dt_fine_validita",
        )

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.PUBLICATIONS_COMMUNITY_TYPES_LIST_SUMMARY,
        description=descriptions.PUBLICATIONS_COMMUNITY_TYPES_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(PublicationsCommunityTypesSerializer(many=True)),
    ),
)
class PublicationsCommunityTypesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = PublicationsCommunityTypesSerializer

    queryset = (
        PubblicazioneCommunity.objects.all()
        .only("community_id", "community_name")
        .order_by("community_id")
        .distinct()
    )
