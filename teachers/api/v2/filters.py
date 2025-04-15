from django_filters import rest_framework as filters
from django.db.models import Q
from addressbook.models import Personale
from structures.models import DidatticaDipartimento
import datetime

class TeachersFilter(filters.FilterSet):
    search = filters.CharFilter(
        field_name="cognome",
        lookup_expr="istartswith",
        label="Search",
        help_text="Search for research groups.",
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
    dip = filters.CharFilter(
        field_name="dip_cod",
        lookup_expr="exact",
        label="Department",
        help_text="Search for department.",
    )
    
    def filter_cds(self, queryset, name, value):
        if not value and not self.data.get('regdid'):
            return queryset.filter(
                Q(fl_docente=1, flg_cessato=0)
                | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year) & ~Q(didatticacopertura__stato_coper_cod='R')
                | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1) & ~Q(didatticacopertura__stato_coper_cod='R')
            )
        return queryset.filter(didatticacopertura__cds_cod=value)
    
    def filter_regdid(self, queryset, name, value):
        if not value and not self.data.get('cds'):
                return queryset.filter(
                Q(fl_docente=1, flg_cessato=0)
                | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year) & ~Q(didatticacopertura__stato_coper_cod='R')
                | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1) & ~Q(didatticacopertura__stato_coper_cod='R')
            )
        return queryset.filter(didatticacopertura__cds_cod=value)
        

    def filter_role(self, queryset, name, value):
        roles = value.split(',')
        return queryset.filter(cd_ruolo__in=roles)

    def filter_department(self, queryset, name, value):
        if value:
            dip = value
        else:
            dip = queryset.values_list('cd_uo_aff_org', flat=True).distinct()
            dip = list(dip)
        
        department = (DidatticaDipartimento.objects.filter(dip_cod=dip)
                     .values("dip_id", "dip_cod", "dip_des_it", "dip_des_eng")
                     .first())
        if not department:
            return queryset.none()
        
        qs = queryset.filter(cd_uo_aff_org=department.dip_cod)
        for q in qs:
                q["dip_id"] = department.dip_id
                q["dip_cod"] = department.dip_cod
                q["dip_des_it"] = department.dip_des_it
                q["dip_des_eng"] = department.dip_des_eng
        return qs

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
        roles = value.split(',')
        return queryset.filter(cd_ruolo__in=roles)

    class Meta:
        model = Personale
        fields = []
