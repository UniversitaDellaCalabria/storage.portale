from rest_framework import serializers
from ricerca_app.models import SitoWebCdsOggettiPortale

class SitoWebCdsOggettiPortaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SitoWebCdsOggettiPortale
        fields = ('id', 'aa_regdid_id', 'titolo_it', 'titolo_en')