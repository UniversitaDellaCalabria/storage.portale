from rest_framework import serializers
from cds.models import DidatticaCds


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        for field in fields:
            fields[field].read_only = True
        return fields

class CdsSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DidatticaCds
        fields = "__all__"

