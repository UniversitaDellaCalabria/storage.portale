from django_filters import rest_framework as filters
from django.db.models import Q
from addressbook.models import Personale


class PersonnelCfFilter(filters.FilterSet):
    roles = filters.CharFilter(
        method="filter_roles",
        label="Roles",
        help_text="Search for roles",
    )

    def filter_roles(self, queryset, name, value):
        return queryset.filter(cd_ruolo__in=value.split(","))

    class Meta:
        model = Personale
        fields = []
        
        
class AddressbookFilter(filters.FilterSet):
    search = filters.CharFilter(
        field_name="cognome",
        lookup_expr="istartswith",
        label="Search",
        help_text="Filter by surname.",
    )
    taxpayer_id = filters.CharFilter(
        field_name="cod_fis",
        lookup_expr="exact",
        label="Taxpayer ID",
        help_text="Filter by Taxpayer ID."
    )
    
    phone = filters.CharFilter(
        method="filter_by_phone", 
        label="Phone",
        help_text="Filter by phone number."
    )
    
    role = filters.CharFilter(
        method="filter_by_role", 
        label="Role",
        help_text="Filter by roles."
    )

    def filter_by_phone(self, queryset, name, value):
        return queryset.filter(
            personalecontatti__cd_tipo_cont__descr_contatto__in=[
                "Telefono Cellulare",
                "Telefono Cellulare Ufficio"
            ],
            personalecontatti__contatto=value
        ).distinct()
    
    def filter_by_role(self, queryset, name, value):
        role = value.split(",") if value else []
        roles = []
        for k in role:
            roles.append(k)
                
        return queryset.filter(
            Q(pers_attivo_tutti_ruoli__cd_ruolo__in=value)
            | Q(profilo__in=value)
        ).distinct()

    class Meta:
        model = Personale
        fields = []
