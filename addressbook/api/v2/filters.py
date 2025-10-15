from django_filters import rest_framework as filters
from django.db.models import Q
from addressbook.models import Personale, PersonaleAttivoTuttiRuoli
from addressbook.settings import (
    PERSON_CONTACTS_EXCLUDE_STRINGS,
    PERSON_CONTACTS_TO_TAKE,
)
import datetime

from structures.models import UnitaOrganizzativa


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


class AddressbookStructuresFilter(filters.FilterSet):
    father = filters.CharFilter(
        method="filter_father",
        label="Father",
        help_text="Search for father",
    )

    search = filters.CharFilter(
        method="filter_search",
        label="Search",
        help_text="Search for search",
    )

    type = filters.CharFilter(
        method="filter_type",
        label="Type",
        help_text="Search for type",
    )

    def filter_father(self, queryset, name, value):
        if value:
            return queryset.filter(uo_padre=value)
        return queryset.filter(uo_padre__isnull=True)

    def filter_search(self, queryset, name, value):
        query_search = Q()
        if value:
            for k in value.split(" "):
                q_denominazione = Q(denominazione__icontains=k)
                query_search &= q_denominazione
            return queryset.filter(query_search)

    def filter_type(self, queryset, name, value):
        query_type = Q()
        if value:
            for k in value.split(","):
                q_type = Q(cd_tipo_nodo=k)
                query_type |= q_type
            return queryset.filter(query_type)

    class Meta:
        model = UnitaOrganizzativa
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
        help_text="Filter by Taxpayer ID.",
    )

    phone = filters.CharFilter(
        method="filter_by_phone", label="Phone", help_text="Filter by phone number."
    )

    role = filters.CharFilter(
        method="filter_by_role", label="Role", help_text="Filter by roles."
    )

    structuretypes = filters.CharFilter(
        method="filter_by_structuretypes",
        label="Structure Types",
        help_text="Filter by structure types.",
    )

    structureid = filters.CharFilter(
        method="filter_by_structureid",
        label="Structure ID",
        help_text="Filter by exact structure or site.",
    )

    structuretree = filters.CharFilter(
        method="filter_by_structuretree",
        label="Structure Tree",
        help_text="Filter by structure tree (including children).",
    )

    def filter_by_structureid(self, queryset, name, value):
        role_param = self.data.get("role")
        results =[]
        for item in queryset:
            ruoli = self.ruoli(item.cod_fis, "")
            for r in ruoli:
                if r.cd_uo_aff_org == value or r.sede == value:
                    if not role_param or r.cd_ruolo in role_param or r.cd_profilo in role_param:
                        results.append(item.id_ab)
        return queryset.filter(id_ab__in=results)

    def getStructureChilds(self, structureid=None):
        child = UnitaOrganizzativa.objects.filter(
            uo_padre=structureid, dt_fine_val__gte=datetime.datetime.today()
        ).values_list("uo", flat=True)
        result = [structureid]
        for c in child:
            structures_tree = self.getStructureChilds(c)
            result.extend(structures_tree)
        result.extend(child)
        return result

    def filter_by_structuretree(self, queryset, name, value):
        query_structuretree = self.getStructureChilds(value)
        role_param = self.data.get("role", [])
        
        if not role_param or not query_structuretree:
            return queryset

        filtered_queryset = queryset.filter(
            Q(ruoli__cd_uo_aff_org__in=query_structuretree) | 
            Q(ruoli__sede__in=query_structuretree)
        ).filter(
            Q(ruoli__cd_ruolo__in=role_param) | 
            Q(profilo__in=role_param)
        )
        return filtered_queryset

    
    def filter_by_structuretypes(self, queryset, name, value):
        s = []
        for k in value.split(","):
            s.append(k)
        role_param = self.data.get("role")

        result =  []
        for item in queryset:
            final_structures = []
            ruoli = self.ruoli(item.cod_fis, "")
            for r in ruoli:
                if not role_param or r.cd_ruolo in role_param or r.cd_profilo in role_param:
                    final_structures.append(r.cd_uo_aff_org.cd_tipo_nodo)
            if set(s).intersection(set(final_structures)):
                    result.append(item.id_ab)
            
        return queryset.filter(id_ab__in=result)
    
    def get_contacts(self, obj, contactDescr):
        if contactDescr in PERSON_CONTACTS_TO_TAKE:
            for contact in obj.contatti:
                tipo = contact.cd_tipo_cont
                if tipo.descr_contatto not in PERSON_CONTACTS_EXCLUDE_STRINGS:
                    return contact.contatto
        return []

    def filter_by_phone(self, queryset, name, value):
        if not value:
            return queryset

        results = []
        for item in queryset:
            numbers = self.get_contacts(item, "Telefono Cellulare Ufficio")
            if not numbers:
                numbers = self.get_contacts(item, "Telefono Ufficio")
            if value in numbers:
                results.append(item.id_ab)
        return queryset.filter(id_ab__in=results)

    def ruoli(self, cod_fis, ruolo):
        if(ruolo):
            return PersonaleAttivoTuttiRuoli.objects.filter(
                cd_uo_aff_org__isnull=False, cod_fis=cod_fis, cd_ruolo=ruolo
            ).select_related("cd_uo_aff_org")
        else:
             return PersonaleAttivoTuttiRuoli.objects.filter(
            cd_uo_aff_org__isnull=False, cod_fis=cod_fis,
        ).select_related("cd_uo_aff_org")

    def filter_by_role(self, queryset, name, value):
        roles = value.split(",") if value else []
        if not roles:
            return queryset

        results = []
        for obj in queryset:
            for ruolo in self.ruoli(obj.cod_fis, value):
                if ruolo.cd_ruolo in roles:
                    results.append(obj.id_ab)

        return queryset.filter(id_ab__in=results)

    class Meta:
        model = Personale
        fields = []
