from django_filters import rest_framework as filters
from django.db.models import Q
from addressbook.models import Personale
from structures.models import DidatticaDipartimento
from cds.models import DidatticaCopertura
from teachers.models import DocenteMaterialeDidattico, DocentePtaBacheca, PubblicazioneDatiBase
import datetime
from addressbook.utils import get_personale_matricola


class PublicationFilter(filters.FilterSet):
    search = filters.CharFilter(
        method="filter_search",
        label="Search",
        help_text="Search for title.",
    )
    year = filters.NumberFilter(
        field_name="date_issued_year",
        lookup_expr="exact",
        label="Year",
        help_text="Search for year.",
    )
    pub_type = filters.CharFilter(
        field_name="collection_id.community_id.community_id",
        lookup_expr="exact",
        label="Publication Type",
        help_text="Search for publication type.",
    ) 
    teacherid = filters.CharFilter(
        method="filter_teacherid",
        label="Teacher ID",
        help_text="Search for teacher id.",
    )
    structure = filters.CharFilter(
        field_name="pubblicazioneautori.ab.cd_uo_aff_org",
        lookup_expr="exact",
        label="Structure",
        help_text="Search for structure.",
    )
    
    def filter_teacherid(self, queryset, name, value):
        if value:
            valuedecr = get_personale_matricola(value)
            personale = Personale.objects.filter(matricola=valuedecr).values('cod_fis').first()
            if personale:
                return queryset.filter(Q(pubblicazioneautori__codice_fiscale=personale['cod_fis']))
    
    def filter_search(self, queryset, name, value):
        for k in value.split(" "): 
            query_search = Q(title__icontains=k) | Q(contributors__icontains=k)
        return queryset.filter(query_search)


    class Meta:
        model = PubblicazioneDatiBase
        fields = []

class TeachersNewsFilter(filters.FilterSet):
    search = filters.CharFilter(
        method="filters_search",
        label="Search",
        help_text="Search for title.",
    )
    
    def filter_search(self, queryset, name, value):
        for k in value.split(" "): 
            query_search = Q(titolo__icontains=k) | Q(titolo_en__icontains=k)
        
        return queryset.filter(query_search)


    class Meta:
        model = DocentePtaBacheca
        fields = []

class TeachersMaterialsFilter(filters.FilterSet):
    search = filters.CharFilter(
        method="filters_search",
        label="Search",
        help_text="Search for title.",
    )
    
    def filter_search(self, queryset, name, value):
        for k in value.split(" "): 
            query_search = Q(titolo__icontains=k) | Q(titolo_en__icontains=k)
        
        return queryset.filter(query_search)


    class Meta:
        model = DocenteMaterialeDidattico
        fields = []


class TeachersStudyActivitiesFilter(filters.FilterSet):
    year = filters.NumberFilter(
        field_name="aa_off_id",
        lookup_expr="exact",
        label="Year",
        help_text="Search for year.",
    )
    
    yearFrom = filters.NumberFilter(
        field_name="aa_off_id",
        lookup_expr="gte",
        label="Year From",
        help_text="Search from a specific year.",
    )

    yearTo = filters.NumberFilter(
        field_name="aa_off_id",
        lookup_expr="lte",
        label="Year To",
        help_text="Search to a specific year.",
    )


    class Meta:
        model = DidatticaCopertura
        fields = []


class TeachersFilter(filters.FilterSet):
    search = filters.CharFilter(
        field_name="cognome",
        lookup_expr="istartswith",
        label="Search",
        help_text="Search for research groups.",
    )
    dip  = filters.CharFilter(
        method="filter_dip",
        label="Department",
        help_text="Search for department.",
    )
    regdid = filters.CharFilter(
        method="filter_regdid",
        label="RegDid",
        help_text="Search for RegDid.",
    )
    cds = filters.CharFilter(
        method="filter_cds",
        lookup_expr="exact",
        label="Cds",
        help_text="Search for Cds.",
    )
    year = filters.CharFilter(
        field_name="didatticacopertura__aa_off_id",
        lookup_expr="exact",
        label="Year",
        help_text="Search for year.",
    )
    role = filters.CharFilter(
        method="filter_role",
        label="Role",
        help_text="Search for role.",
    )

    def filter_dip(self, queryset, name, value):
        if value:
            department = (
                DidatticaDipartimento.objects.filter(dip_cod=value)
                .values("dip_id", "dip_cod", "dip_des_it", "dip_des_eng")
                .first()
            )
            if not department:
                return None
            query = queryset.filter(cd_uo_aff_org=department["dip_cod"])
            query = list(query)
            for q in query:
                q["dip_id"] = department["dip_id"]
                q["dip_cod"] = department["dip_cod"]
                q["dip_des_it"] = department["dip_des_it"]
                q["dip_des_eng"] = department["dip_des_eng"]

        else:
            dip_cods = query.values_list("cd_uo_aff_org", flat=True).distinct()
            dip_cods = list(dip_cods)

            departments = DidatticaDipartimento.objects.filter(
                dip_cod__in=dip_cods
            ).values("dip_id", "dip_cod", "dip_des_it", "dip_des_eng")

            for q in query:
                found = False
                for dep in departments:
                    if dep["dip_cod"] == q["cd_uo_aff_org"]:
                        q["dip_id"] = dep["dip_id"]
                        q["dip_cod"] = dep["dip_cod"]
                        q["dip_des_it"] = dep["dip_des_it"]
                        q["dip_des_eng"] = dep["dip_des_eng"]
                        found = True
                        break

                if not found:
                    q["dip_id"] = None
                    q["dip_cod"] = None
                    q["dip_des_it"] = None
                    q["dip_des_eng"] = None

        
    
    def filter_cds(self, queryset, name, value):
        if not value and not self.data.get("regdid"):
            return queryset.filter(
                Q(fl_docente=1, flg_cessato=0)
                | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year)
                & ~Q(didatticacopertura__stato_coper_cod="R")
                | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1)
                & ~Q(didatticacopertura__stato_coper_cod="R")
            )
        return queryset.filter(didatticacopertura__cds_cod=value)

    def filter_regdid(self, queryset, name, value):
        if not value and not self.data.get("cds"):
            return queryset.filter(
                Q(fl_docente=1, flg_cessato=0)
                | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year)
                & ~Q(didatticacopertura__stato_coper_cod="R")
                | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1)
                & ~Q(didatticacopertura__stato_coper_cod="R")
            )
        return queryset.filter(didatticacopertura__regdid_id=value)

    def filter_role(self, queryset, name, value):
        roles = value.split(",")
        return queryset.filter(cd_ruolo__in=roles)

    class Meta:
        model = Personale
        fields = []


class CoveragesFilter(filters.FilterSet):
    search = filters.CharFilter(
        field_name="cognome",
        lookup_expr="icontains",
        label="Search",
        help_text="Search for research groups.",
    )
    regdid = filters.CharFilter(
        field_name="didatticacopertura__af__regdid__regdid_id",
        lookup_expr="exact",
        label="RegDid",
        help_text="Search for RegDid.",
    )
    cds = filters.CharFilter(
        field_name="didatticacopertura__cds_cod",
        lookup_expr="exact",
        label="Cds",
        help_text="Search for Cds.",
    )
    year = filters.CharFilter(
        field_name="didatticacopertura__aa_off_id",
        lookup_expr="exact",
        label="Year",
        help_text="Search for year.",
    )
    role = filters.CharFilter(
        method="filter_role",
        label="Role",
        help_text="Search for role.",
    )
    dip = filters.CharFilter(
        field_name="dip_cod",
        lookup_expr="exact",
        label="Department",
        help_text="Search for department.",
    )

    def filter_search(self, queryset, name, value):
        query_search = Q()
        for k in value.split(" "):
            q_cognome = Q(cognome__icontains=k)
            query_search &= q_cognome

        return queryset.filter(query_search)

    def filter_role(self, queryset, name, value):
        roles = value.split(",")
        return queryset.filter(cd_ruolo__in=roles)

    class Meta:
        model = Personale
        fields = []
