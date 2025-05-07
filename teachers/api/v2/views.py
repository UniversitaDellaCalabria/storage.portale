import datetime
from django_filters.rest_framework import DjangoFilterBackend
# from drf_spectacular.utils import (
#     extend_schema,
#     extend_schema_view,
# )
# from .docs import descriptions
# from api_docs import responses

from rest_framework.pagination import PageNumberPagination
from addressbook.settings import (
    PERSON_CONTACTS_EXCLUDE_STRINGS,
    PERSON_CONTACTS_TO_TAKE,
)
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import mixins, viewsets
from addressbook.utils import append_email_addresses, get_personale_matricola
from organizational_area.models import OrganizationalStructureOfficeEmployee
from research_lines.settings import OFFICE_RESEARCH_LINES
from .filters import (
    TeachersFilter,
    CoveragesFilter,
    # PublicationFilter
)
from .serializers import (
    TeachersSerializer,
    PublicationsSerializer,
    PublicationSerializer,
    TeachersStudyActivitiesSerializer,
    TeachersMaterialsSerializer,
    PublicationsCommunityTypesSerializer,
)

from django.db.models import Case, Q, OuterRef, When, F, Value, IntegerField, Prefetch
from structures.models import DidatticaDipartimento, UnitaOrganizzativaFunzioni
from django.db.models.functions import Lower
from addressbook.models import Personale
from teachers.models import (
    DocenteMaterialeDidattico,
    DocentePtaAltriDati,
    DocentePtaBacheca,
    PubblicazioneAutori,
    PubblicazioneCommunity,
    PubblicazioneDatiBase,
)
from cds.models import DidatticaCopertura
import teachers.utils


class TeachersViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = TeachersSerializer
    filterset_class = TeachersFilter

    def get_queryset(self):
        if self.action == "list":
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
                Personale.objects.filter(
                    Q(fl_docente=1)
                    | (
                        Q(didatticacopertura__af__isnull=False)
                        & ~Q(didatticacopertura__stato_coper_cod="R")
                    )
                )
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
                    "dip_id",
                    "dip_cod",
                    "dip_des_it",
                    "dip_des_eng",
                    "email",
                )
                .order_by("cognome", "nome", "middle_name")
                .distinct()
            )

            append_email_addresses(query, "id_ab")
            return query

        if self.action == "retrieve":
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

            teacher = get_personale_matricola(self.kwargs.get("id"))
            query = (
                Personale.objects.filter(
                    Q(fl_docente=1, flg_cessato=0)
                    | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year)
                    & ~Q(didatticacopertura__stato_coper_cod="R")
                    | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1)
                    & ~Q(didatticacopertura__stato_coper_cod="R"),
                    matricola=teacher,
                )
                .prefetch_related(
                    Prefetch(
                        "unitaorganizzativafunzioni_set",
                        queryset=UnitaOrganizzativaFunzioni.objects.filter(
                            termine__gt=datetime.datetime.now(),
                            decorrenza__lt=datetime.datetime.now(),
                        ).only("ds_funzione", "cd_csa__uo", "cd_csa__denominazione"),
                        to_attr="unitaorganizzativafunzioni",
                    ),
                    Prefetch(
                        "docenteptaaltridati_set",
                        queryset=DocentePtaAltriDati.objects.only(
                            "path_foto",
                            "path_cv_ita",
                            "path_cv_en",
                            "breve_bio",
                            "breve_bio_en",
                            "orario_ricevimento",
                            "orario_ricevimento_en",
                            "orcid",
                        ),
                        to_attr="docenteptaaltridati",
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
                    "dip_id",
                    "dip_cod",
                    "dip_des_it",
                    "dip_des_eng",
                )
                .distinct()
            )
            q_contacts = (
                query.filter(
                    personalecontatti__cd_tipo_cont__descr_contatto__in=PERSON_CONTACTS_TO_TAKE,
                )
                .exclude(
                    personalecontatti__contatto__isnull=True,
                )
                .exclude(
                    *[
                        Q(personalecontatti__contatto__icontains=word)
                        for word in PERSON_CONTACTS_EXCLUDE_STRINGS
                    ]
                )
                .annotate(contatto_lower=Lower("personalecontatti__contatto"))
                .order_by("contatto_lower")
                .distinct("contatto_lower")
                .values(
                    "personalecontatti__cd_tipo_cont__descr_contatto",
                    "personalecontatti__contatto",
                )
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


class PublicationsViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = PublicationsSerializer
    # filterset_class = PublicationFilter

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
                        "pubblicazioneautori_set",
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
                        # append_email_addresses(autori, "ab__id_ab")
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
                .annotate(
                    date_issued_year=Case(
                        When(date_issued_year=9999, then=Value("in stampa")),
                        default=F("date_issued_year"),
                        output_field=IntegerField(),
                    )
                )
                .distinct()
            )


class TeachersStudyActivitiesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = TeachersStudyActivitiesSerializer
    # filterset_class = TeachersStudyActivitiesFilter

    def get_queryset(self):
        teacher = get_personale_matricola(self.kwargs.get("id"))

        queryset = (
            DidatticaCopertura.objects.filter(
                personale__matricola__exact=teacher, af__isnull=False
            )
            .select_related("personale", "af")
            .order_by("aa_off_id", "anno_corso", "af_gen_des", "af_gen_des_eng")
            .values(
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


class TeachersMaterialsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = TeachersMaterialsSerializer
    # filterset_class = TeachersMaterialsFilter

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
            .values(
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


class TeachersResearchLinesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    # serializer_class = TeachersResearchLinesSerializer
    # filterset_class = TeachersResearchLinesFilter

    def get_queryset(self):
        teacher = get_personale_matricola(self.kwargs.get("id"))

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

        query_is_active_app = (
            Q(ricercadocentelineaapplicata__ricerca_linea_applicata__visibile=True)
            if only_active
            else Q()
        )
        query_is_active_base = (
            Q(ricercadocentelineabase__ricerca_linea_base__visibile=True)
            if only_active
            else Q()
        )

        linea_applicata = (
            Personale.objects.filter(
                query_is_active_app,
                matricola__exact=self.kwargs.get("id"),
                fl_docente=1,
                ricercadocentelineaapplicata__dt_fine__isnull=True,
                ricercadocentelineaapplicata__ricerca_linea_applicata__id__isnull=False,
            )
            .order_by("ricercadocentelineaapplicata__ricerca_linea_applicata__id")
            .values(
                "ricercadocentelineaapplicata__ricerca_linea_applicata__id",
                "ricercadocentelineaapplicata__ricerca_linea_applicata__descrizione",
                "ricercadocentelineaapplicata__ricerca_linea_applicata__descr_pubblicaz_prog_brevetto",
                "ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__erc0_cod",
                "ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__description",
            )
            .distinct()
            .annotate(
                tipologia=Value(
                    "applicativa",
                    output_field=IntegerField(),
                )
            )
        )

        linea_base = (
            Personale.objects.filter(
                query_is_active_base,
                matricola__exact=self.kwargs.get("id"),
                fl_docente=1,
                ricercadocentelineabase__dt_fine__isnull=True,
                ricercadocentelineabase__ricerca_linea_base__id__isnull=False,
            )
            .order_by("ricercadocentelineabase__ricerca_linea_base__id")
            .values(
                "ricercadocentelineabase__ricerca_linea_base__id",
                "ricercadocentelineabase__ricerca_linea_base__descrizione",
                "ricercadocentelineabase__ricerca_linea_base__descr_pubblicaz_prog_brevetto",
                "ricercadocentelineabase__ricerca_linea_base__ricerca_erc2__ricerca_erc1__ricerca_erc0_cod__erc0_cod",
                "ricercadocentelineabase__ricerca_linea_base__ricerca_erc2__ricerca_erc1__ricerca_erc0_cod__description",
            )
            .distinct()
            .annotate(
                tipologia=Value(
                    "base",
                    output_field=IntegerField(),
                )
            )
        )


class TeachersNewsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]

    # serializer_class = TeachersNewsSerializer
    # filterset_class = TeachersMaterialsFilter
    def get_queryset(self):
        query_is_active = Q(attivo=True)

        return DocentePtaBacheca.objects.filter(query_is_active).only(
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


class PublicationsCommunityTypesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = PublicationsCommunityTypesSerializer
    # filterset_class = PublicationFilter
    queryset = (
        PubblicazioneCommunity.objects.all()
        .only("community_id", "community_name")
        .order_by("community_id")
        .distinct()
    )
