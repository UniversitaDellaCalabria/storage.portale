from generics.serializers import CreateUpdateAbstract
from generics.utils import build_media_path


class CdsBrochureLightSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(self.to_dict(instance, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        languages = [lang.iso6392_cod for lang in query.cds.languages]
        return {
            "Id": query.id,
            # 'CDSId': query['cds__cds_id'],
            "CdSCod": query.cds.cds_cod,
            "CdSAcademicYear": query.aa,
            "CdSName": query.cds.nome_cds_it
            if req_lang == "it" or query.cds.nome_cds_eng is None
            else query.cds.nome_cds_eng,
            "AreaCds": query.cds.area_cds
            if req_lang == "it" or query.cds.area_cds_en is None
            else query.cds.area_cds_en,
            "CourseType": query.cds.tipo_corso_cod,
            "CdSLanguage": languages,
            "CdsClassCod": query.cds.cla_miur_cod,
            "CdsInterClassCod": query.cds.intercla_miur_cod,
        }


class CdsBrochureSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(self.to_dict(instance, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        ex_students = []
        if query.get("ExStudents"):
            ex_students = CdsBrochureSerializer.to_dict_ex_students(
                query["ExStudents"], req_lang
            )

        cds_link = []
        if query.get("CdsLink"):
            cds_link = CdsBrochureSerializer.to_dict_links(query["CdsLink"], req_lang)

        cds_sliders = []
        if query.get("CdsSliders"):
            cds_sliders = CdsBrochureSerializer.to_dict_sliders(
                query["CdsSliders"], req_lang
            )

        course_interclass = None
        if query["cds__intercla_miur_cod"] and query["cds__intercla_miur_des"]:
            course_interclass = (
                f"{query['cds__intercla_miur_cod']} {query['cds__intercla_miur_des']}"
            )

        course_class = None
        if query["cds__cla_miur_cod"] and query["cds__cla_miur_des"]:
            course_class = f"{query['cds__cla_miur_cod']} {query['cds__cla_miur_des']}"

        return {
            "Id": query["id"],
            # 'CDSId': query['cds_id'],
            "CDSCOD": query["cds__cds_cod"],
            "CDSAcademicYear": query["aa"],
            "CDSName": query["cds__nome_cds_it"]
            if req_lang == "it" or query["cds__nome_cds_eng"] is None
            else query["cds__nome_cds_eng"],
            "CDSCourseClassName": course_class,
            "CDSCourseInterClassDes": course_interclass,
            "CDSLanguage": query[
                "lingue"
            ],  # query['lingua_it'] if req_lang=='it' or query['lingua_en'] is None else query['lingua_en'],
            "CDSDuration": query["cds__durata_anni"],
            "CDSSeatsNumber": query["num_posti"],
            "CDSVideo": query["link_video_cds_it"]
            if req_lang == "it" or query["link_video_cds_en"] is None
            else query["link_video_cds_en"],
            "CDSIntro": query["descrizione_corso_it"]
            if req_lang == "it" or query["descrizione_corso_en"] is None
            else query["descrizione_corso_en"],
            "CDSAdmission": query["accesso_corso_it"]
            if req_lang == "it" or query["accesso_corso_en"] is None
            else query["accesso_corso_en"],
            "CDSGoals": query["obiettivi_corso_it"]
            if req_lang == "it" or query["obiettivi_corso_en"] is None
            else query["obiettivi_corso_en"],
            "CDSJobOpportunities": query["sbocchi_professionali_it"]
            if req_lang == "it" or query["sbocchi_professionali_en"] is None
            else query["sbocchi_professionali_en"],
            "CDSTaxes": query["tasse_contributi_esoneri_it"]
            if req_lang == "it" or query["tasse_contributi_esoneri_en"] is None
            else query["tasse_contributi_esoneri_en"],
            "CDSScholarships": query["borse_studio_it"]
            if req_lang == "it" or query["borse_studio_en"] is None
            else query["borse_studio_en"],
            "CDSConcessions": query["agevolazioni_it"]
            if req_lang == "it" or query["agevolazioni_en"] is None
            else query["agevolazioni_en"],
            "CDSShortDescription": query["corso_in_pillole_it"]
            if req_lang == "it" or query["corso_in_pillole_en"] is None
            else query["corso_in_pillole_en"],
            "CDSStudyPlan": query["cosa_si_studia_it"]
            if req_lang == "it" or query["cosa_si_studia_en"] is None
            else query["cosa_si_studia_en"],
            "CDSEnrollmentMode": query["come_iscriversi_it"]
            if req_lang == "it" or query["come_iscriversi_en"] is None
            else query["come_iscriversi_en"],
            "CDSExStudents": ex_students,
            "CDSLinks": cds_link,
            "CDSSliders": cds_sliders,
        }

    @staticmethod
    def to_dict_ex_students(query, req_lang="en"):
        ex_students = []
        for q in query:
            ex_students.append(
                {
                    "StudentId": q["id"],
                    "StudentName": q["nome"],
                    "StudentOrder": q["ordine"],
                    "StudentProfile": q["profilo_it"]
                    if req_lang == "it" or q["profilo_en"] is None
                    else q["profilo_en"],
                    "StudentLink": q["link_it"]
                    if req_lang == "it" or q["link_en"] is None
                    else q["link_en"],
                    "StudentPhoto": build_media_path(q["foto"]) if q["foto"] else None,
                }
            )
        return ex_students

    @staticmethod
    def to_dict_links(query, req_lang="en"):
        links = []
        for q in query:
            links.append(
                {
                    "LinkId": q["id"],
                    "LinkOrder": q["ordine"],
                    "LinkDescription": q["descrizione_link_it"]
                    if req_lang == "it" or q["descrizione_link_en"] is None
                    else q["descrizione_link_en"],
                    "Link": q["link_it"]
                    if req_lang == "it" or q["link_en"] is None
                    else q["link_en"],
                }
            )
        return links

    @staticmethod
    def to_dict_sliders(query, req_lang="en"):
        sliders = []
        for q in query:
            sliders.append(
                {
                    "SliderId": q["id"],
                    "SliderOrder": q["ordine"],
                    "SliderDescription": q["slider_it"]
                    if req_lang == "it" or q["slider_en"] is None
                    else q["slider_en"],
                }
            )
        return sliders

    # @staticmethod
    # def to_dict_offices_data(query):
    #     data = []
    #     for q in query:
    #         data.append({
    #             'Order': q['ordine'],
    #             'OfficeName': q['nome_ufficio'],
    #             'OfficeDirector': encrypt(q['matricola_riferimento']),
    #             'OfficeDirectorName': q['nome_origine_riferimento'],
    #             'TelOffice': q['telefono'],
    #             'Email': q['email'],
    #             'Floor': q['piano'],
    #             'Timetables': q['orari'],
    #             'OnlineCounter': q['sportello_online']
    #         })
    #     return data
