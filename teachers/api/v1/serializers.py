from addressbook.settings import PERSON_CONTACTS_TO_TAKE
from generics.serializers import CreateUpdateAbstract
from generics.utils import build_media_path, encrypt


def _get_teacher_obj_publication_date(teacher_dict):
    if not teacher_dict["dt_pubblicazione"]:
        return None
    if not teacher_dict["dt_inizio_validita"]:
        return teacher_dict["dt_pubblicazione"]
    if not teacher_dict["dt_pubblicazione"]:
        return teacher_dict["dt_inizio_validita"]
    if teacher_dict["dt_pubblicazione"] > teacher_dict["dt_inizio_validita"]:
        return teacher_dict["dt_pubblicazione"]
    return teacher_dict["dt_inizio_validita"]


class TeachersSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        full_name = (
            query["cognome"]
            + " "
            + query["nome"]
            + (" " + query["middle_name"] if query["middle_name"] is not None else "")
        )
        return {
            "TeacherID": encrypt(query["matricola"]),
            "TeacherName": full_name,
            "TeacherDepartmentID": query["dip_id"],
            "TeacherDepartmentCod": query["dip_cod"],
            "TeacherDepartmentName": query["dip_des_it"]
            if req_lang == "it" or not query["dip_des_eng"]
            else query["dip_des_eng"],
            "TeacherRole": query["cd_ruolo"],
            "TeacherRoleDescription": query["ds_ruolo_locale"],
            "TeacherSSDCod": query["cd_ssd"],
            "TeacherSSDDescription": query["ds_ssd"],
            "TeacherCVFull": query["cv_full_it"]
            if req_lang == "it" or not query["cv_full_eng"]
            else query["cv_full_eng"],
            "TeacherCVShort": query["cv_short_it"]
            if req_lang == "it" or not query["cv_short_eng"]
            else query["cv_short_eng"],
            "ProfileId": query["profilo"],
            "ProfileDescription": query["ds_profilo"],
            "ProfileShortDescription": query["ds_profilo_breve"],
            "Email": query["email"],
        }


class TeacherStudyActivitiesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "StudyActivityID": query["af_id"],
            "StudyActivityCod": query["af_gen_cod"],
            "StudyActivityName": query["af_gen_des"]
            if req_lang == "it" or query["af_gen_des_eng"] is None
            else query["af_gen_des_eng"],
            "StudyActivityCdSID": query["cds_id"],
            "StudyActivityCdSCod": query["cds_cod"],
            "StudyActivityRegDidId": query["regdid_id"],
            "StudyActivityCdSName": query["cds_des"]
            if req_lang == "it" or query["af__cds__nome_cds_eng"] is None
            else query["af__cds__nome_cds_eng"],
            "StudyActivityAA": query["aa_off_id"],
            "StudyActivityYear": query["anno_corso"],
            "StudyActivitySemester": query["ciclo_des"],
            "StudyActivityECTS": query["peso"],
            "StudyActivityLanguage": query["af__lista_lin_did_af"],
            "StudyActivitySSD": query["sett_des"],
            "StudyActivityCompulsory": query["af__freq_obblig_flg"],
            "StudyActivityPartitionCod": query["fat_part_stu_cod"],
            "StudyActivityPartitionDescription": query["fat_part_stu_des"],
            "SingleStudyActivityPartitionCod": query["part_stu_cod"],
            "SingleStudyActivityPartitionDescription": query["part_stu_des"],
            "StudyActivityPartitionType": query["tipo_fat_stu_cod"],
            "StudyActivityPartitionStart": query["part_ini"],
            "StudyActivityPartitionEnd": query["part_fine"],
        }


class TeacherInfoSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        functions = None
        if query["Functions"] is not None:
            functions = TeacherInfoSerializer.to_dict_functions(query["Functions"])

        return {
            "TeacherID": encrypt(query["matricola"]),
            "TeacherFirstName": query["nome"]
            + (" " + query["middle_name"] if query["middle_name"] is not None else ""),
            "TeacherLastName": query["cognome"],
            "TeacherDepartmentID": query["dip_id"],
            "TeacherDepartmentCod": query["dip_cod"],
            "TeacherDepartmentName": query["dip_des_it"]
            if req_lang == "it" or not query["dip_des_eng"]
            else query["dip_des_eng"],
            "TeacherRole": query["cd_ruolo"],
            "TeacherRoleDescription": query["ds_ruolo_locale"],
            "TeacherSSDCod": query["cd_ssd"],
            "TeacherSSDDescription": query["ds_ssd"],
            "TeacherOffice": query["ds_aff_org"],
            "ORCID": query["ORCID"],
            "PhotoPath": build_media_path(query["PHOTOPATH"]),
            "CVPathIta": build_media_path(query["PATHCVITA"]),
            "CVPathEn": build_media_path(query["PATHCVENG"]),
            "ShortBio": query["BREVEBIO"]
            if req_lang == "it" or not query["BREVEBIOENG"]
            else query["BREVEBIOENG"],
            "ReceptionHours": query["ORARIORICEVIMENTO"]
            if req_lang == "it" or not query["ORARIORICEVIMENTOEN"]
            else query["ORARIORICEVIMENTOEN"],
            "TeacherOfficeReference": query["Riferimento Ufficio"]
            if "Riferimento Ufficio" in PERSON_CONTACTS_TO_TAKE
            else [],
            "TeacherEmail": query["Posta Elettronica"]
            if "Posta Elettronica" in PERSON_CONTACTS_TO_TAKE
            else [],
            "TeacherPEC": query["POSTA ELETTRONICA CERTIFICATA"]
            if "POSTA ELETTRONICA CERTIFICATA" in PERSON_CONTACTS_TO_TAKE
            else [],
            "TeacherTelOffice": query["Telefono Ufficio"]
            if "Telefono Ufficio" in PERSON_CONTACTS_TO_TAKE
            else [],
            "TeacherTelCelOffice": query["Telefono Cellulare Ufficio"]
            if "Telefono Cellulare Ufficio" in PERSON_CONTACTS_TO_TAKE
            else [],
            "TeacherFax": query["Fax"] if "Fax" in PERSON_CONTACTS_TO_TAKE else [],
            "TeacherWebSite": query["URL Sito WEB"]
            if "URL Sito WEB" in PERSON_CONTACTS_TO_TAKE
            else [],
            "TeacherCV": query["URL Sito WEB Curriculum Vitae"]
            if "URL Sito WEB Curriculum Vitae" in PERSON_CONTACTS_TO_TAKE
            else [],
            "TeacherFunctions": functions,
            "TeacherCVFull": query["cv_full_it"]
            if req_lang == "it" or not query["cv_full_eng"]
            else query["cv_full_eng"],
            "TeacherCVShort": query["cv_short_it"]
            if req_lang == "it" or not query["cv_short_eng"]
            else query["cv_short_eng"],
            "ProfileId": query["profilo"],
            "ProfileDescription": query["ds_profilo"],
            "ProfileShortDescription": query["ds_profilo_breve"],
        }

    @staticmethod
    def to_dict_functions(query):  # pragma: no cover
        functions = []
        for q in query:
            functions.append(
                {
                    "TeacherRole": q["ds_funzione"],
                    "StructureCod": q["cd_csa__uo"],
                    "StructureName": q["cd_csa__denominazione"],
                }
            )
        return functions

    @staticmethod
    def to_dict_board(query, req_lang="en"):  # pragma: no cover
        board = []
        for q in query:
            board.append(
                {
                    "Title": q["titolo"]
                    if req_lang == "it" or not q["titolo_en"]
                    else q["titolo_en"],
                    "TextType": q["tipo_testo"]
                    if req_lang == "it" or not q["tipo_testo_en"]
                    else q["tipo_testo_en"],
                    "Text": q["testo"]
                    if req_lang == "it" or not q["testo_en"]
                    else q["testo_en"],
                    "TextUrl": q["url_testo"]
                    if req_lang == "it" or not q["url_testo_en"]
                    else q["url_testo_en"],
                    "Order": q["ordine"],
                    "Active": q["attivo"],
                    "PublicationDate": q["dt_pubblicazione"],
                    "ValidityStartDate": q["dt_inizio_validita"],
                    "ValidityEndDate": q["dt_fine_validita"],
                }
            )
        return board


class TeacherMaterialsSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "ID": query["id"],
            "Title": query["titolo"]
            if req_lang == "it" or not query["titolo_en"]
            else query["titolo_en"],
            "Text": query["testo"]
            if req_lang == "it" or not query["testo_en"]
            else query["testo_en"],
            "TextUrl": query["url_testo"]
            if req_lang == "it" or not query["url_testo_en"]
            else query["url_testo_en"],
            "Order": query["ordine"],
            "Active": query["attivo"],
            "PublicationDate": _get_teacher_obj_publication_date(query),
        }


class TeacherNewsSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "ID": query["id"],
            "Title": query["titolo"]
            if req_lang == "it" or not query["titolo_en"]
            else query["titolo_en"],
            "TextType": query["tipo_testo"]
            if req_lang == "it" or not query["tipo_testo_en"]
            else query["tipo_testo_en"],
            "Text": query["testo"]
            if req_lang == "it" or not query["testo_en"]
            else query["testo_en"],
            "TextUrl": query["url_testo"]
            if req_lang == "it" or not query["url_testo_en"]
            else query["url_testo_en"],
            "Order": query["ordine"],
            "Active": query["attivo"],
            "PublicationDate": _get_teacher_obj_publication_date(query),
        }


class PublicationSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        authors = None
        if query.get("Authors") is not None:
            authors = PublicationSerializer.to_dict_authors(query["Authors"])
        return {
            "PublicationId": query["item_id"],
            "PublicationTitle": query["title"],
            "PublicationAbstract": query["des_abstract"]
            if req_lang == "it" or query["des_abstracteng"] is None
            else query["des_abstracteng"],
            "PublicationCollection": query["collection_id__collection_name"],
            "PublicationCommunity": query[
                "collection_id__community_id__community_name"
            ],
            "Publication": query["pubblicazione"],
            "PublicationLabel": query["label_pubblicazione"],
            "PublicationContributors": query["contributors"],
            "PublicationYear": query["date_issued_year"],
            "PublicationAuthors": authors,
            "PublicationUrl": query["url_pubblicazione"],
        }

    @staticmethod
    def to_dict_authors(query):
        result = []
        for q in query:
            if q["ab__matricola"] is None:
                full_name = q["last_name"] + " " + q["first_name"]
            else:
                full_name = (
                    q["ab__cognome"]
                    + " "
                    + q["ab__nome"]
                    + (
                        " " + q["ab__middle_name"]
                        if q["ab__middle_name"] is not None
                        else ""
                    )
                )
            result.append(
                {
                    "AuthorId": encrypt(q["ab__matricola"]),
                    "AuthorName": full_name,
                    "AuthorEmail": q["email"],
                }
            )
        return result


class PublicationsSerializer(PublicationSerializer):
    @staticmethod
    def to_dict(query, req_lang="en"):
        response = PublicationSerializer.to_dict(query, req_lang)
        response.pop("PublicationAuthors")
        return response


class PublicationsCommunityTypesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "CommunityId": query["community_id"],
            "CommunityName": query["community_name"],
        }


class TeacherResearchLinesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        if query["Tipologia"] == "base":
            return {
                "RLineID": query["ricercadocentelineabase__ricerca_linea_base__id"],
                "RLineDescription": query[
                    "ricercadocentelineabase__ricerca_linea_base__descrizione"
                ],
                "RLineResults": query[
                    "ricercadocentelineabase__ricerca_linea_base__descr_pubblicaz_prog_brevetto"
                ],
                "RLineERC0Id": query[
                    "ricercadocentelineabase__ricerca_linea_base__ricerca_erc2__ricerca_erc1__ricerca_erc0_cod__erc0_cod"
                ],
                "RLineERC0Name": query[
                    "ricercadocentelineabase__ricerca_linea_base__ricerca_erc2__ricerca_erc1__ricerca_erc0_cod__description"
                ],
            }
        else:
            return {
                "RLineID": query[
                    "ricercadocentelineaapplicata__ricerca_linea_applicata__id"
                ],
                "RLineDescription": query[
                    "ricercadocentelineaapplicata__ricerca_linea_applicata__descrizione"
                ],
                "RLineResults": query[
                    "ricercadocentelineaapplicata__ricerca_linea_applicata__descr_pubblicaz_prog_brevetto"
                ],
                "RLineERC0Id": query[
                    "ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__erc0_cod"
                ],
                "RLineERC0Name": query[
                    "ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__description"
                ],
            }
