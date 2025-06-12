from django_filters import rest_framework as filters
from django.db.models import Q
from addressbook.models import Personale

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
        if not value:
            return queryset

        role_param = self.data.get("role")
        role_list = role_param.split(",") if role_param else []

        filtro_struttura = Q(pers_attivo_tutti_ruoli__cd_uo_aff_org=value) | Q(
            pers_attivo_tutti_ruoli__sede=value
        )

        if role_list:
            filtro_ruolo = Q(pers_attivo_tutti_ruoli__cd_ruolo__in=role_list) | Q(
                profilo__in=role_list
            )
            queryset = queryset.filter(filtro_struttura & filtro_ruolo)
        else:
            queryset = queryset.filter(filtro_struttura)

        return queryset.distinct()

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
        if not value:
            return queryset

        role_param = self.data.get("role")
        role_list = role_param.split(",") if role_param else []

        structure_ids = self.getStructureChilds(value)

        filtro_struttura = Q(
            pers_attivo_tutti_ruoli__cd_uo_aff_org__in=structure_ids
        ) | Q(pers_attivo_tutti_ruoli__sede__in=structure_ids)

        if role_list:
            filtro_ruolo = Q(pers_attivo_tutti_ruoli__cd_ruolo__in=role_list) | Q(
                profilo__in=role_list
            )
            queryset = queryset.filter(filtro_struttura & filtro_ruolo)
        else:
            queryset = queryset.filter(filtro_struttura)

        return queryset.distinct()

    def filter_by_structuretypes(self, queryset, name, value):
        if not value:
            return queryset

        structuretypes = value.split(",")

        role_param = self.data.get("role")
        role_list = role_param.split(",") if role_param else []

        filtro_tipo_struttura = Q(
            pers_attivo_tutti_ruoli__cd_tipo_nodo__in=structuretypes
        )

        if role_list:
            filtro_ruolo = Q(pers_attivo_tutti_ruoli__cd_ruolo__in=role_list) | Q(
                profilo__in=role_list
            )
            queryset = queryset.filter(filtro_tipo_struttura & filtro_ruolo)
        else:
            queryset = queryset.filter(filtro_tipo_struttura)

        return queryset.distinct()

    def filter_by_phone(self, queryset, name, value):
        return queryset.filter(
            personalecontatti__cd_tipo_cont__descr_contatto__in=[
                "Telefono Cellulare",
                "Telefono Cellulare Ufficio",
            ],
            personalecontatti__contatto=value,
        ).distinct()

    def filter_by_role(self, queryset, name, value):
        role = value.split(",") if value else []
        roles = []
        for k in role:
            roles.append(k)

        return queryset.filter(
            Q(pers_attivo_tutti_ruoli__cd_ruolo__in=value) | Q(profilo__in=value)
        ).distinct()

    class Meta:
        model = Personale
        fields = []
