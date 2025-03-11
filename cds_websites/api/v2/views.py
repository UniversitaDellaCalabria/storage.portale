from django.db.models import (
    Prefetch,
    Value,
    Case,
    When,
    Q,
    CharField, 
    F,
)
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from .docs import descriptions
from api_docs import responses

from organizational_area.models import OrganizationalStructureOfficeEmployee
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets
from cds_websites.settings import OFFICE_CDS_WEBSITES

from .serializers import (
    TopicListSerialzer,
    ArticlesTopicSerializer,
    StudyPlansSerializer
)
from cds_websites.models import (
    SitoWebCdsTopic,
    SitoWebCdsTopicArticoliRegAltriDati,
    SitoWebCdsSubArticoliRegolamento,
    SitoWebCdsTopicArticoliReg
    
)
from cds.models import (
    DidatticaAttivitaFormativa,
    DidatticaPianoRegolamento,
    DidatticaPianoSceltaAf,
    DidatticaPianoSceltaFilAnd,
    DidatticaPianoSceltaSchePiano,
    DidatticaPianoSche,
)


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.TOPIC_LIST_SUMMARY,
        description=descriptions.TOPIC_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(TopicListSerialzer(many=True)),
    ),
)
class TopicListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = TopicListSerialzer
    queryset = SitoWebCdsTopic.objects.only("id", "descr_topic_it", "descr_topic_en", "visibile").distinct()
    

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.ARTICLESTOPIC_LIST_SUMMARY,
        description=descriptions.ARTICLESTOPIC_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(ArticlesTopicSerializer(many=True)),
    ),
)    
class ArticlesTopicListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = ArticlesTopicSerializer    
    
    def get_queryset(self):
        cds_cod = self.kwargs.get("cds_cod")
        topic_id = self.kwargs.get("topic_id")
        
        topic_id_list = topic_id.split(",")
        
        only_active = True
        if self.request.user.is_superuser:
            only_active = False  # pragma: no cover
        elif self.request.user.is_authenticated:  # pragma: no cover
            offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=self.request.user,
                office__is_active=True,
                office__name=OFFICE_CDS_WEBSITES,
                office__organizational_structure__is_active=True,
            )

            if offices.exists():
                only_active = False
                
        query_visibile = Q(visibile=True) if only_active else Q()
        query_topic_id = Q(sito_web_cds_topic__id__in=topic_id_list)
        query_cds_cod = Q(
            didattica_cds_articoli_regolamento__didattica_cds_articoli_regolamento_testata__cds__cds_cod=str(
                cds_cod
            )
        ) | Q(sito_web_cds_oggetti_portale__cds__cds_cod=str(cds_cod))
        
        
        articoli_reg_altri_dati_qs = (
            SitoWebCdsTopicArticoliRegAltriDati.objects.filter(query_visibile)
            .select_related("sito_web_cds_tipo_dato")
            .defer("dt_mod", "user_mod", "sito_web_cds_tipo_dato__descr_lunga")
            .annotate(
                type_id=F("sito_web_cds_tipo_dato__id"),
                type=F("sito_web_cds_tipo_dato__descr_breve"),
            )
        )

        sub_articoli_qs = SitoWebCdsSubArticoliRegolamento.objects.filter(
            query_visibile
        ).defer("dt_mod", "user_mod")

        return (
            SitoWebCdsTopicArticoliReg.objects.prefetch_related(
                Prefetch(
                    "sitowebcdstopicarticoliregaltridati_set",
                    queryset=articoli_reg_altri_dati_qs,
                ),
                Prefetch(
                    "sitowebcdssubarticoliregolamento_set", queryset=sub_articoli_qs
                ),
            )
            .select_related(
                "sito_web_cds_oggetti_portale__cds",
                "didattica_cds_articoli_regolamento__didattica_cds_articoli_regolamento_testata__cds",
                "sito_web_cds_topic",
            )
            .filter(query_topic_id, query_cds_cod, query_visibile)
            .only(
                "id",
                "titolo_it",
                "titolo_en",
                "testo_it",
                "testo_en",
                "visibile",
                "ordine",
                "sito_web_cds_topic__id",
                "sito_web_cds_topic__descr_topic_it",
                "sito_web_cds_topic__descr_topic_en",
                "sito_web_cds_oggetti_portale__id",
                "sito_web_cds_oggetti_portale__id_classe_oggetto_portale",
                "sito_web_cds_oggetti_portale__id_oggetto_portale",
                "sito_web_cds_oggetti_portale__aa_regdid_id",
                "sito_web_cds_oggetti_portale__testo_it",
                "sito_web_cds_oggetti_portale__testo_en",
                "sito_web_cds_oggetti_portale__cds__cds_cod",
                "didattica_cds_articoli_regolamento__id",
                "didattica_cds_articoli_regolamento__didattica_cds_articoli_regolamento_testata__cds__cds_cod",
            )
            .annotate(
                tipo=Case(
                    When(
                        didattica_cds_articoli_regolamento__isnull=False,
                        then=Value("Article"),
                    ),
                    default=Value("Object"),
                    output_field=CharField(),
                )
            )
            .order_by("sito_web_cds_topic__id", "ordine")
        )
    

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.STUDYPLANS_LIST_SUMMARY,
        description=descriptions.STUDYPLANS_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(StudyPlansSerializer(many=True)),
    ),
)     
class StudyPlansViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = StudyPlansSerializer
    
    def get_queryset(self):
        cds_cod = self.kwargs.get("cds_cod")
        year = self.kwargs.get("year")
        
        if cds_cod and year:  # or regdid:
            query_cds = Q(regdid_id__cds_id__cds_cod__exact=cds_cod) if cds_cod else Q()
            query_year = Q(regdid_id__aa_reg_did__exact=year) if year else Q()
           
            query = (
                DidatticaPianoRegolamento.objects.filter(
                    query_cds,
                    query_year,
                    stato_cod="A",
                )
                .select_related("regdid__cds")
                .values(
                    "regpiani_id",
                    "regdid_id",
                    "attinenza_cod",
                    "cod",
                    "aa_coorte_id",
                    "aa_regpiani_id",
                    "des",
                    "def_flg",
                    "stato_cod",
                    "stato_des",
                    "regpiani_pdr_id",
                    "regpiani_pdr_cod",
                    "regpiani_pdr_des",
                    "regpiani_pdr_aa_coorte_id",
                    "regpiani_pdr_aa_regpiani_id",
                    "flg_exp_seg_stu",
                    "regdid__cds__durata_anni",
                )
                .distinct()
                .order_by("regpiani_id")
            )

            for q in query:
                schede = DidatticaPianoSche.objects.filter(
                    regpiani_id__exact=q["regpiani_id"]
                ).values(
                    "sche_piano_id",
                    "sche_piano_des",
                    "sche_piano_cod",
                    "pds_cod",
                    "pds_des",
                    "comune_flg",
                    "apt_id",
                    "cla_m_id",
                    "cla_miur_cod",
                    "cla_miur_des",
                    "pds_cod",
                )

                for s in schede:
                    obbl = DidatticaPianoSceltaSchePiano.objects.filter(
                        sche_piano_id__exact=s["sche_piano_id"], tipo_sce_cod__exact="O"
                    ).values(
                        "sce_id",
                        "sce_des",
                        "anno_corso",
                        "apt_slot_ord_num",
                        "tipo_regsce_cod",
                        "tipo_sce_cod",
                        "tipo_sce_des",
                        "tipo_regsce_des",
                        "tipo_um_regsce_cod",
                        "min_unt",
                        "max_unt",
                        "opz_flg",
                        "vin_id",
                        "vin_sce_des",
                        "sce_id__opz_flg",
                        "sce_id__anno_corso_ant",
                        "sche_statutario_flg",
                    )
                    s["isStatutario"] = None
                    s["AfRequired"] = obbl

                    for af in obbl:
                        if s["isStatutario"] is None:
                            s["isStatutario"] = af["sche_statutario_flg"]

                        af_obblig = DidatticaPianoSceltaAf.objects.filter(
                            sce_id__exact=af["sce_id"]
                        ).values(
                            "amb_id_af",
                            "anno_corso_af",
                            "ciclo_des",
                            "af_gen_des",
                            "af_id",
                            "af_gen_cod",
                            "tipo_af_des_af",
                            "ambito_des_af",
                            "sett_cod",
                            "peso",
                            "sce_id__sce_des",
                            "sce_id",
                        )

                        af["Required"] = af_obblig

                        for activity in af["Required"]:
                            list_submodules = (
                                DidatticaAttivitaFormativa.objects.filter(
                                    part_stu_cod__isnull=True,
                                    af_pdr_id=activity["af_id"],
                                )
                                .exclude(af_id=activity["af_id"])
                                .values(
                                    "af_id",
                                    "af_gen_cod",
                                    "des",
                                    "peso",
                                    "sett_cod",
                                    "af_gen_des_eng",
                                    "fat_part_stu_cod",
                                    "lista_lin_did_af",
                                    "part_stu_cod",
                                    "part_stu_des",
                                    "fat_part_stu_des",
                                    "ciclo_des",
                                )
                            )

                            activity["MODULES"] = list_submodules

                        fil_and = DidatticaPianoSceltaFilAnd.objects.filter(
                            sce_id__exact=af["sce_id"]
                        ).values(
                            "sce_fil_and_id",
                            "sce_id",
                            "sce_fil_or_id",
                            "sce_fil_or_des",
                            "tipo_filtro_cod",
                            "tipo_filtro_des",
                            "tipo_corso_sce_fil_and_cod",
                            "cds_sce_fil_and_id",
                            "cds_sce_fil_and_cod",
                            "cds_sce_fil_and_nome",
                            "not_flg",
                        )

                        af["FilAnd"] = fil_and

                    scelte = DidatticaPianoSceltaSchePiano.objects.filter(
                        ~Q(tipo_sce_cod__exact="O"),
                        sche_piano_id__exact=s["sche_piano_id"],
                    ).values(
                        "sce_id",
                        "sce_des",
                        "anno_corso",
                        "apt_slot_ord_num",
                        "tipo_regsce_cod",
                        "tipo_sce_cod",
                        "tipo_sce_des",
                        "tipo_regsce_des",
                        "tipo_um_regsce_cod",
                        "min_unt",
                        "max_unt",
                        "opz_flg",
                        "vin_id",
                        "vin_sce_des",
                        "sce_id__opz_flg",
                        "sce_id__anno_corso_ant",
                    )

                    verifica = (
                        Q(amb_id__isnull=False)
                        | Q(amb_id_af_regsce__isnull=False)
                        | Q(tipo_sce_cod="V")
                    )

                    s["AfChoices"] = scelte

                    for scelta in scelte:
                        if s["isStatutario"] is None:
                            s["isStatutario"] = af["sche_statutario_flg"]

                        fil_and = DidatticaPianoSceltaFilAnd.objects.filter(
                            sce_id__exact=scelta["sce_id"]
                        ).values(
                            "sce_fil_and_id",
                            "sce_id",
                            "sce_fil_or_id",
                            "sce_fil_or_des",
                            "tipo_filtro_cod",
                            "tipo_filtro_des",
                            "cds_sce_fil_and_id",
                            "cds_sce_fil_and_cod",
                            "cds_sce_fil_and_nome",
                            "tipo_corso_sce_fil_and_cod",
                            "not_flg",
                        )

                        scelta["FilAnd"] = fil_and

                        af_scelta = DidatticaPianoSceltaAf.objects.filter(
                            sce_id__exact=scelta["sce_id"]
                        ).values(
                            "amb_id_af",
                            "anno_corso_af",
                            "ciclo_des",
                            "af_gen_des",
                            "af_gen_cod",
                            "af_id",
                            "tipo_af_des_af",
                            "ambito_des_af",
                            "sett_cod",
                            "peso",
                            "sce_id__sce_des",
                            "sce_id",
                        )

                        scelta["Choices"] = af_scelta

                        for activity in scelta["Choices"]:
                            list_submodules = (
                                DidatticaAttivitaFormativa.objects.filter(
                                    part_stu_cod__isnull=True,
                                    af_pdr_id=activity["af_id"],
                                )
                                .exclude(af_id=activity["af_id"])
                                .values(
                                    "af_id",
                                    "af_gen_cod",
                                    "des",
                                    "af_gen_des_eng",
                                    "peso",
                                    "fat_part_stu_cod",
                                    "lista_lin_did_af",
                                    "part_stu_cod",
                                    "part_stu_des",
                                    "fat_part_stu_des",
                                    "ciclo_des",
                                )
                            )

                            activity["MODULES"] = list_submodules

                        if af_scelta is None:  # pragma: no cover
                            af_scelta = DidatticaPianoSceltaAf.objects.filter(
                                verifica, sce_id__exact=scelta["sce_id"]
                            ).values(
                                "amb_id_af",
                                "anno_corso_af",
                                "ciclo_des",
                                "af_gen_des",
                                "af_id",
                                "tipo_af_des_af",
                                "ambito_des_af",
                                "sett_cod",
                                "peso",
                                "sce_id__sce_des",
                                "sce_id",
                            )

                            scelta["Choices"] = af_scelta

                            for activity in scelta["Choices"]:
                                list_submodules = (
                                    DidatticaAttivitaFormativa.objects.filter(
                                        part_stu_cod__isnull=True,
                                        af_pdr_id=activity["af_id"],
                                    )
                                    .exclude(af_id=activity["af_id"])
                                    .values(
                                        "af_id",
                                        "af_gen_cod",
                                        "des",
                                        "peso",
                                        "af_gen_des_eng",
                                        "fat_part_stu_cod",
                                        "lista_lin_did_af",
                                        "part_stu_cod",
                                        "part_stu_des",
                                        "fat_part_stu_des",
                                        "ciclo_des",
                                    )
                                )

                                activity["MODULES"] = list_submodules
                schede = sorted(
                    list(schede),
                    key=lambda k: (
                        k["cla_m_id"] if k["cla_m_id"] else 0,
                        -k["isStatutario"],
                        k["apt_id"] if k["apt_id"] else 0,
                    ),
                )
                q["PlanTabs"] = schede
        return query


        
        
    
    