from rest_framework import serializers

from .models import *


class PersonaleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Personale
        # Todo add @properties to Model to hanlde childs elements
        fields = ['nome', 'cognome', ]  # 'matricola', 'cod_fis']
        #  fields = '__all__'


class RicercaAster1Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RicercaAster1
        fields = ['descrizione', ]


class RicercaAster2Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RicercaAster2
        fields = ['descrizione', ]


class RicercaErc1Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RicercaErc1
        fields = ['cod_erc1', 'descrizione', ]


class RicercaErc2Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RicercaErc2
        fields = ['cod_erc2', 'descrizione', 'ricerca_erc1']


class RicercaDocenteGruppoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RicercaDocenteGruppo
        fields = ['personale', 'ricerca_gruppo', 'dt_inizio', 'dt_fine']


class RicercaDocenteLineaApplicataSerializer(
        serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RicercaDocenteLineaApplicata
        fields = [
            'personale',
            'ricerca_linea_applicata',
            'dt_inizio',
            'dt_fine']


class RicercaDocenteLineaBaseSerializer(
        serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RicercaDocenteLineaBase
        fields = ['personale', 'ricerca_linea_base', 'dt_inizio', 'dt_fine']


class RicercaGruppoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RicercaGruppo
        fields = ['nome', 'descrizione']


class RicercaLineaApplicataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RicercaLineaApplicata
        fields = ['descrizione', 'ricerca_aster2',
                  'descr_pubblicaz_prog_brevetto', 'anno']


class RicercaLineaBaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RicercaLineaBase
        fields = ['descrizione', 'ricerca_erc2',
                  'descr_pubblicaz_prog_brevetto', 'anno']


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

class CreateUpdateAbstract(serializers.Serializer):
    def create(self, validated_data):
        try:
            super().create(validated_data)
        except BaseException:
            pass

    def update(self, instance, validated_data):
        try:
            super().update(instance, validated_data)
        except BaseException:
            pass


class CdSListSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        return {
            'RegDidId': query['didatticaregolamento__regdid_id'],
            'CdSId': query['cds_id'],
            'AcademicYear': query['didatticaregolamento__aa_reg_did'],
            'CdSName': query['nome_cds_it'] if req_lang == 'it' or query['nome_cds_eng'] is None else query['nome_cds_eng'],
            'DepartmentId': query['dip__dip_cod'],
            'DepartmentName': query['dip__dip_des_it'] if req_lang == 'it' or query['dip__dip_des_eng'] is None else query['dip__dip_des_eng'],
            'CourseType': query['tipo_corso_cod'],
            'CourseClassId': query['cla_miur_cod'],
            'CourseClassName': query['cla_miur_des'],
            'CdSLanguage': query['didatticacdslingua__lingua_des_it'] if req_lang == 'it' or query['didatticacdslingua__lingua_des_eng'] is None else query['didatticacdslingua__lingua_des_eng'],
            'CdSDuration': query['durata_anni'],
            'CdSECTS': query['valore_min'],
            'CdSAttendance': query['didatticaregolamento__frequenza_obbligatoria']
        }


class CdsInfoSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        return {
            'RegDidId': query['didatticaregolamento__regdid_id'],
            'CdSId': query['cds_id'],
            'AcademicYear': query['didatticaregolamento__aa_reg_did'],
            'CdSName': query['nome_cds_it'] if req_lang == 'it' or query['nome_cds_eng'] is None else query['nome_cds_eng'],
            'DepartmentId': query['dip__dip_cod'],
            'DepartmentName': query['dip__dip_des_it'] if req_lang == 'it' or query['dip__dip_des_eng'] is None else query['dip__dip_des_eng'],
            'CourseType': query['tipo_corso_cod'],
            'CourseClassId': query['cla_miur_cod'],
            'CourseClassName': query['cla_miur_des'],
            'CdSLanguage': query['didatticacdslingua__lingua_des_it'] if req_lang == 'it' or query['didatticacdslingua__lingua_des_eng'] is None else query['didatticacdslingua__lingua_des_eng'],
            'CdSDuration': query['durata_anni'],
            'CdSECTS': query['valore_min'],
            'CdSAttendance': query['didatticaregolamento__frequenza_obbligatoria'],
            'CdSIntro': query['DESC_COR_BRE'],
            'CdSGoals': query['OBB_SPEC'],
            'CdSAccess': query['REQ_ACC'],
            'CdSAdmission': query['REQ_ACC_2'],
            'CdSProfiles': query['PROFILO'],
            'CdSFinalTest': query['PROVA_FINALE'],
            'CdSFinalTestMode': query['PROVA_FINALE_2'],
            'CdSSatisfactionSurvey': query['codicione'],
        }


class CdSStudyPlansSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        return {
            'RegDidId': query['regdid__regdid_id'],
            'StudyPlanId': query['pds_regdid__pds_regdid_id'],
            'StudyPlanName': query['pds_regdid__pds_des_it'] if req_lang == 'it' or query['pds_regdid__pds_des_eng'] is None else query[
                'pds_regdid__pds_des_eng'],
            'StudyActivityID': query['af_id'],
            'StudyActivityName': query['des'] if req_lang == 'it' or query['af_gen_des_eng'] is None else query['af_gen_des_eng'],
            'StudyActivityCdSID': query['cds__cds_id'],
            'StudyActivityYear': query['anno_corso'],
            'StudyActivitySemester': query['ciclo_des'],
            'StudyActivityECTS': query['peso'],
            'StudyActivitySSD': query['sett_des'],
            'StudyActivityCompulsory': query['freq_obblig_flg'],
            'StudyActivityCdSName': query['cds__nome_cds_it'] if req_lang == 'it' or query['cds__nome_cds_eng'] is None else query['cds__nome_cds_eng'],
        }


class StudyPlansActivitiesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        return {
            'StudyActivityID': query['af_id'],
            'StudyActivityName': query['des'] if req_lang == 'it' or query['af_gen_des_eng'] is None else query['af_gen_des_eng'],
            'StudyActivityCdSID': query['cds__cds_id'],
            'StudyActivityYear': query['anno_corso'],
            'StudyActivitySemester': query['ciclo_des'],
            'StudyActivityECTS': query['peso'],
            'StudyActivitySSD': query['sett_des'],
            'StudyActivityCompulsory': query['freq_obblig_flg'],
            'StudyActivityCdSName': query['cds__nome_cds_it'] if req_lang == 'it' or query['cds__nome_cds_eng'] is None else query['cds__nome_cds_eng'],
        }

# class StudyActivityInfoSerializer(CreateUpdateAbstract):
#     def to_representation(self, instance):
#         query = instance
#         data = super().to_representation(instance)
#         data.update(self.to_dict(query,
#                                  str(self.context['language']).lower()))
#         return data
#
#     @staticmethod
#     def to_dict(query,
#                 req_lang='en'):
#         return {
#             'StudyActivityID': query['af_id'],
#             'StudyActivityName': query['des'] if req_lang == 'it' or query['af_gen_des_eng'] is None else query['af_gen_des_eng'],
#             'StudyActivityCdSID': query['cds__cds_id'],
#             'StudyActivityYear': query['anno_corso'],
#             'StudyActivitySemester': query['ciclo_des'],
#             'StudyActivityECTS': query['peso'],
#             'StudyActivitySSD': query['sett_des'],
#             'StudyActivityCompulsory': query['freq_obblig_flg'],
#             'StudyActivityCdSName': query['cds__nome_cds_it'] if req_lang == 'it' or query['cds__nome_cds_eng'] is None else query['cds__nome_cds_eng'],
#             'StudyActivitiesModules': query['MODULES'],
#         }
