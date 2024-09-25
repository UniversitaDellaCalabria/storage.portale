from generics.serializers import CreateUpdateAbstract
from generics.utils import encrypt

class AllResearchGroupsSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        teachers = None
        if query['Teachers'] is not None:
            teachers = AllResearchGroupsSerializer.to_dict_teachers(
                query['Teachers'])
        return {
            'RGroupID': query['id'],
            'RGroupName': query['nome'],
            'RGroupDescription': query['descrizione'],
            'IdErc1': query['ricerca_erc1_id__cod_erc1'],
            'RLineDescription': query['ricerca_erc1_id__descrizione'],
            'Teachers': teachers,
        }

    @staticmethod
    def to_dict_teachers(query):
        result = []
        for q in query:
            full_name = q['personale_id__cognome'] + " " + q['personale_id__nome'] + \
                (" " + q['personale_id__middle_name']
                 if q['personale_id__middle_name'] is not None else "")
            result.append({
                'TeacherID': encrypt(q['personale_id__matricola']),
                'TeacherName': full_name,
                'DepartmentName': q['personale_id__ds_sede'],
                'DepartmentCod': q['personale_id__sede']
            })
        return result

