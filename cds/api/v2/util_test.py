from addressbook.models import Personale
from django.test import TestCase
from cds.models import (
    DidatticaCds,
    DidatticaRegolamento,
    DidatticaAttivitaFormativa,
    DidatticaCopertura,
    DidatticaCdsTipoCorso,
    DidatticaCdsLingua,
    DidatticaCdsAltriDatiUfficio,
    DidatticaCdsAltriDati,
    DidatticaTestiRegolamento,
    DidatticaPdsRegolamento,
    DidatticaTestiAf,
    DidatticaCoperturaDettaglioOre,
    DidatticaAttivitaFormativaModalita,
    DidatticaCdsCollegamento
)
from structures.models import DidatticaDipartimento


class ApiCdsUnitTestMethods(TestCase):
    @classmethod
    def create_personale(cls, **kwargs):
        data = {
            "id": 1,
            "nome": "Franco",
            "cognome": "Garofalo",
            "cd_ruolo": "PO",
            "id_ab": 1,
            "matricola": "111111",
        }
        data.update(kwargs)
        return Personale.objects.create(**data)

    @classmethod
    def create_didattica_cds_tipo_corso(cls, user, **kwargs):
        data = {
            "tipo_corso_cod": "L",
            "tipo_corso_des": "Laurea",
            "user_mod": user,
        }
        data.update(kwargs)
        return DidatticaCdsTipoCorso.objects.create(**data)

    @classmethod
    def create_didatticaAttivitaFormativa(cls, **kwargs):
        data = {
            "af_id": 1,
            "af_gen_cod": "AF001",
            "des": "Analisi Matematica",
            "af_gen_des_eng": "Mathematical Analysis",
            "cds_id": 1,
            "aa_off_id": 2023,
            "ciclo_des": "Primo semestre",
            "tipo_ciclo_cod": "S1",
            "des_tipo_ciclo": "S1",
            "sett_cod": "MAT/05",
            "sett_des": "Analisi Matematica",
            "pds_des": "Piano di studi A",
            "part_stu_des": "Part Stu Des",
        }
        data.update(kwargs)
        return DidatticaAttivitaFormativa.objects.create(**data)

    @classmethod
    def create_didatticaDipartimento(cls, **kwargs):
        data = {
            "dip_id": 1,
            "dip_cod": "DIP01",
            "dip_des_it": "Dipartimento di Informatica",
            "dip_des_eng": "Department of Computer Science",
        }
        data.update(kwargs)
        return DidatticaDipartimento.objects.create(**data)

    @classmethod
    def create_didatticaCopertura(cls, **kwargs):
        data = {
            "af_id": 1,
            "matricola_resp_did": "111111",
            "stato_coper_cod": "A",
            "personale_id": 1,
        }
        data.update(kwargs)
        return DidatticaCopertura.objects.create(**data)

    @classmethod
    def create_didatticaCds(cls, **kwargs):
        data = {
            "cds_id": 1,
            "nome_cds_it": "informatica",
            "nome_cds_eng": "computer science",
            "tipo_corso_cod": "1",
            "cla_miur_cod": "1",
            "cla_miur_des": "laurea in informatica",
            "durata_anni": 3,
            "valore_min": 180,
            "cdsord_id": 1,
        }
        data.update(kwargs)
        return DidatticaCds.objects.create(**data)

    @classmethod
    def create_didatticaRegolamento(cls, **kwargs):
        data = {
            "regdid_id": 1,
            "aa_reg_did": 2020,
            "frequenza_obbligatoria": 0,
            "titolo_congiunto_cod": "N",
        }
        data.update(kwargs)
        return DidatticaRegolamento.objects.create(**data)

    @classmethod
    def create_didatticaCdsLingua(cls, **kwargs):
        data = {
            "lin_did_ord_id": 1,
            "lingua_des_it": "ITALIANO",
            "lingua_des_eng": "ITALIAN",
        }
        data.update(kwargs)
        return DidatticaCdsLingua.objects.create(**data)

    @classmethod
    def create_didatticaCdsAltriDatiUfficio(cls, **kwargs):
        data = {
            "cds_id": 1,
            "edificio": 2,
            "ordine": 1,
        }
        data.update(kwargs)
        return DidatticaCdsAltriDatiUfficio.objects.create(**data)

    @classmethod
    def create_didatticaCdsAltriDati(cls, **kwargs):
        data = {"nome_origine_coordinatore": "Test coordinatore"}
        data.update(kwargs)
        return DidatticaCdsAltriDati.objects.create(**data)

    @classmethod
    def create_didatticaTestiRegolamento(cls, **kwargs):
        data = {
            "txt_id": 1,
            "tipo_testo_regdid_cod": "testo regolamento",
        }
        data.update(kwargs)
        return DidatticaTestiRegolamento.objects.create(**data)

    @classmethod
    def create_didatticaPdsRegolamento(cls, **kwargs):
        data = {
            "pds_regdid_id": 1,
            "pds_cod": "cod/1",
            "pds_des_it": "des_it",
            "pds_des_eng": "des_eng",
        }
        data.update(kwargs)
        return DidatticaPdsRegolamento.objects.create(**data)

    @classmethod
    def create_didatticaTestiAf(cls, **kwargs):
        data = {
            "tipo_testo_af_cod": "CONTENUTI",
            "testo_af_ita": "Variabili",
            "testo_af_eng": "Variables",
        }
        data.update(kwargs)
        return DidatticaTestiAf.objects.create(**data)

    @classmethod
    def create_didatticaAttivitaFormativaModalita(cls, **kwargs):
        data = {
            "mod_did_af_id": 1,
            "af_id": 1,
            "mod_did_cod": "c",
            "mod_did_des": "convenzionale",
        }
        data.update(kwargs)
        return DidatticaAttivitaFormativaModalita.objects.create(**data)

    @classmethod
    def create_didatticaCoperturaDettaglioOre(cls, **kwargs):
        data = {
            "tipo_att_did_cod": 444,
            "coper_id": 1,
            "ore": 3,
        }
        data.update(kwargs)
        return DidatticaCoperturaDettaglioOre.objects.create(**data)
    

    @classmethod
    def create_didatticaCdsCollegamento(cls, **kwargs):
        data = {
            "cds": 3,
            "cds_prec": 2
        }
        data.update(kwargs)
        return DidatticaCdsCollegamento.objects.create(**data)
