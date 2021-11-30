"""
Django settings for ricerca project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from .settingslocal import *

MIDDLEWARE = [
    # 'silk.middleware.SilkyMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    # SameSite Cookie workaround
    #  'djangosaml2.middleware.SamlSessionMiddleware'
]

CORS_ORIGIN_ALLOW_ALL = True

# GETTEXT LOCALIZATION
MIDDLEWARE.append('django.middleware.locale.LocaleMiddleware')
LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)
#

ROOT_URLCONF = 'ricerca.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ricerca.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# from django 3.2
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# MAPPING LABEL

LABEL_MAPPING = {
    'en': {
        'RegDidId': 'Teaching Regulation ID',
        'RegDidState': 'Teaching Regulation State',
        'CdSId': 'Course of Study ID',
        'CdSCod': 'Course of Study Code',
        'AcademicYear': 'Academic Year',
        'CdSName': 'Course of Study Name',
        'DepartmentId': 'Department ID',
        'DepartmentName': 'Department',
        'DepartmentNameShort': 'Department Name Short',
        'CourseType': 'Course Type',
        'CourseTypeDescription': 'Course Type',
        'CourseClassCod': 'Course Class Cod',
        'CourseClassName': 'Course Class Name',
        'CourseInterClassCod': 'Course InterClass Cod',
        'CourseInterClassDes': 'Course InterClass Name',
        'CdSLanguage': 'Language',
        'CdSDuration': 'Duration',
        'CdSECTS': 'ECTS',
        'CdSAttendance': 'Attendance',
        'CdSIntro': 'Intro',
        'CdSDoc': 'Document',
        'CdSVideo': 'Video',
        'CdSGoals': 'Goals',
        'CdSAccess': 'Access',
        'CdSAdmission': 'Admission',
        'CdSProfiles': 'Profiles',
        'CdSFinalTest': 'Final Test',
        'CdSFinalTestMode': 'Final Test Mode',
        'CdSSatisfactionSurvey': 'Satisfaction Survey',
        'JointDegree': 'Joint Degree',
        'LaboratoryId': 'Laboratory Id',
        'LaboratoryName': 'Laboratory Name',
        'Area': 'Area',
        'Dimension': 'Dimension',
        'ScientificDirector': 'Scientific Director',
        'ScientificDirectors': 'Scientific Directors',
        'ScientificDirectorId': 'Id Scientific Director',
        'StudyPlanId': 'Study Plan ID',
        'StudyPlanName': 'Study Plan Name',
        'StudyPlanCod': 'Study Plan Code',
        'StudyActivities': 'Study Activities',
        'StudyActivityRegDidId': 'Teaching Regulation ID',
        'StudyActivityID': 'Study Activity ID',
        'StudyActivityCod': 'Study Activity Cod',
        'StudyActivityName': 'Study Activity',
        'StudyActivityCdSID': 'Course of Study ID',
        'StudyActivityCdSCod': 'Course of study Code',
        'StudyActivityYear': 'Year',
        'StudyActivitySemester': 'Semester',
        'StudyActivityECTS': 'ECTS',
        'StudyActivitySSD': 'SSD',
        'StudyActivityCompulsory': 'Compulsory',
        'StudyActivityCdSName': 'Course of Study',
        'StudyActivityTeachingUnitType': 'Teaching Unit Type',
        'StudyActivityTeacherID': 'Teacher ID',
        'StudyActivityTeacherName': 'Teacher',
        'StudyActivityContent': 'Content',
        'StudyActivityProgram': 'Program',
        'StudyActivityLearningOutcomes': 'Learning Outcomes',
        'StudyActivityMethodology': 'Methodology',
        'StudyActivityEvaluation': 'Evaluation',
        'StudyActivityTextbooks': 'Textbooks',
        'StudyActivityWorkload': 'Workload',
        'StudyActivityElearningLink': 'E-Learning Link',
        'StudyActivityElearningInfo': 'E-Learning Info',
        'StudyActivityPrerequisites': 'Prerequisites',
        'StudyActivitiesModules': 'Modules',
        'StudyActivityAA': 'Academic Year',
        'StudyActivityLanguage': 'Language',
        'StudyActivityRoot': 'Study Activity Root',
        'StudyActivityBorrowedFrom': 'Borrowed from',
        'StudyActivitiesBorrowedFromThis': 'Borrowed from this',
        'StudyActivityPartitionCod': 'Study Activity Partition Cod',
        'StudyActivityPartitionDescription': 'Study Activity Partition Description',
        'SingleStudyActivityPartitionCod': 'Single Study Activity Partition Cod',
        'SingleStudyActivityPartitionDescription': 'Single Study Activity Partition Description',
        'StudyActivityPartitionType': 'Study Activity Partition Type',
        'StudyActivityPartitionStart': 'Study Activity Start of Partition',
        'StudyActivityPartitionEnd': 'Study Activity End of Partition',
        'Teacher': 'Teacher Web Page',
        'TeacherID': 'Teacher ID',
        'TeacherName': 'Name',
        'TeacherRole': 'Role',
        'TeacherRoleDescription': 'Role',
        'TeacherSSD': 'SSD',
        'TeacherDepartmentID': 'Department ID',
        'TeacherDepartmentCod': 'Department Cod',
        'TeacherDepartmentName': 'Department',
        'TeacherSSDCod': 'SSD',
        'TeacherSSDDescription': 'SSD',
        'TeacherCode': 'Teacher Code',
        'TeacherFirstName': 'First Name',
        'TeacherLastName': 'Last Name',
        'TeacherOffice': 'Office',
        'TeacherOfficeReference': 'Office Reference',
        'TeacherEmail': 'Email',
        'TeacherPEC': 'PEC',
        'TeacherPrivateEmail': 'Private Email',
        'TeacherTelOffice': 'Office Phone',
        'TeacherTelCelOffice': 'Office Mobile Phone',
        'TeacherTelCel': 'Mobile Phone',
        'TeacherTelDomicile': 'Domicile Phone',
        'TeacherTelResidence': 'Residence Phone',
        'TeacherFax': 'Fax',
        'TeacherSkype': 'Skype',
        'TeacherWebSite': 'URL Web Site',
        'TeacherCV': 'Curriculum Vitae',
        'TeacherFunctions': 'Administrative roles',
        'Office': 'Office',
        'OfficeReference': 'Office Reference',
        'Email': 'Email',
        'PEC': 'PEC',
        'PrivateEmail': 'Private Email',
        'TelOffice': 'Office Phone',
        'TelCelOffice': 'Office Mobile Phone',
        'TelCel': 'Mobile Phone',
        'TelDomicile': 'Domicile Phone',
        'TelResidence': 'Residence Phone',
        'Fax': 'Fax',
        'Skype': 'Skype',
        'WebSite': 'URL Web Site',
        'CV': 'Curriculum Vitae',
        'Contacts': 'Contacts',
        'ContactType' : 'Contact Type',
        'Contact' : 'Contact',
        'Function': 'Function',
        'Structure': 'Structure',
        'Role': 'Role',
        'RoleDescription': 'Role',
        'ID': 'ID',
        'IdErc1': 'Id Erc1',
        'IdErc0': 'IdErc0',
        'Name': 'Name',
        'RGroupID': 'Group ID',
        'RGroupName': 'Group Name',
        'RGroupDescription': 'Group Description',
        'RLineID': 'Research Line ID',
        'RLineDescription': 'Description',
        'RLineResults': 'Results',
        'RLineERC0Id': 'ERC0 ID',
        'RLineERC0Name': 'ERC0 Name',
        'DepartmentID': 'Department ID',
        'DepartmentCod': 'Department Code',
        'DoctorateCdsCOD': 'Course of Study Code',
        'DoctorateCdsName': 'Course of Study Name',
        'DoctorateRegID': 'Doctorate Regulation ID',
        'DoctorateRegCOD': 'Doctorate Regulation Code',
        'DoctorateCdSDuration': 'Duration',
        'DoctorateCdSECTS': 'ECTS',
        'DoctorateCdSAttendance': 'Attendance',
        'CourseName': 'Course Name',
        'CycleNumber': 'Cycle Number',
        'StudyPlanCOD': 'Study Plan Code',
        'StudyPlanDes': 'Study Plan Description',
        'FUNZIONI': 'Tasks',
        'COMPETENZE': 'Skills',
        'SBOCCHI': 'Job Opportunities',
        'StructureCod': 'Structure Cod',
        'StructureTypeName': 'Type',
        'StructureName': 'Name',
        'StructureTypeCOD': 'Type',
        'StructureFatherId': 'Reference Structure',
        'StructureFatherName': 'Reference Structure',
        'StructureEmail': 'Email',
        'StructurePec': 'Pec',
        'StructureTfr': 'Phone',
        'StructurePersonnelFunctions': 'Administrative Staff',
        'LaboratoryId': 'ID',
        'Interdepartmental': 'Interdepartmental',
        'InfrastructureName': 'Infrastructure Name',
        'ExtraDepartments': 'Other Departments',
        'CompletionReferentName': 'Completion Referent Name',
        'CompletionReferentId': 'Completion Referent ID',
        'ScientificDirectorId': 'Scientific Director',
        'ScientificDirectorName': 'Scientific Director',
        'LaboratoryName': 'Name',
        'LaboratoryAcronym': 'Acronym',
        'LaboratoryLogo': 'Logo',
        'LaboratoryURL': 'Web Page',
        'LaboratoryEquipment': 'Equipment',
        'DepartmentReferentId': 'Department Referent ID',
        'DepartmentReferentCod': 'Department Referent Cod',
        'DepartmentReferentName': 'Department',
        'LaboratoryScope': 'Scope',
        'LaboratoryServicesScope': 'Services Scope',
        'LaboratoryResearchScope': 'Research Scope',
        'LaboratoryTeachingScope': 'Teaching Scope',
        'LaboratoryActivities': 'Activities',
        'LaboratoryErc1': 'Erc 1',
        'LaboratoryResearchPersonnel': 'Research Scope',
        'LaboratoryTechPersonnel': 'Tech Personnel',
        'LaboratoryOfferedServices': 'Services',
        'LaboratoryLocation': 'Location',
        'LocationBuilding': 'Building',
        'LocationFloor': 'Floor',
        'LocationNotes': 'Notes',
        'ServiceName': 'Name',
        'ServiceDescription': 'Description',
        'TechPersonnelID': 'ID',
        'TechPersonnelName': 'Name',
        'TechPersonnelRole': 'Role',
        'ResearchPersonnelID': 'ID',
        'ResearchPersonnelName': 'Name',
        'LaboratoryErc1Cod': 'Erc1 Code',
        'LaboratoryErc1Description': 'Erc1 Description',
        'LaboratoryErc0Cod': 'Erc0 Code',
        'LaboratoryErc0Description': 'Erc0 Description',
        'LaboratoryActivityType': 'Activity Type',
        'Description': 'Description',
        'PublicationId': 'ID',
        'PublicationTitle': 'Title',
        'PublicationAbstract': 'Abstract',
        'PublicationCollection': 'Collection',
        'PublicationCommunity': 'Type',
        'Publication': 'Publication',
        'PublicationLabel': 'Publication Type',
        'PublicationContributors': 'All Authors',
        'PublicationAuthors': 'Unical Authors',
        'PublicationYear': 'Publication Year',
        'AuthorId': 'ID',
        'AuthorName': 'Name',
        'CommunityId': 'Id',
        'CommunityName': 'Name',
        'PublicationReferenceAuthor': 'Reference Author',
        'Erc1List':'Erc1 List',
        'Erc2List': 'Erc2 List',
        'PublicationUrl': 'Publication Url',
        'TeacherCVFull':'Teacher CV Full',
        'TeacherCVShort':'Teacher CV Short',
        'Teachers': 'Teachers',
        'RLineErc2ID': 'Erc2 Cod',
        'RLineErc2Name': 'Erc2 Name',
        'RYear': 'Research Year',
        'RLineAster2ID': 'Research Aster 2 ID',
        'RLineAster2Name': 'Research Aster 2 Name',
        'Hours': 'Hours',
        'Cover': 'Cover',
        'CodErc2': 'Erc2 Cod',
        'RLineAster2Id': 'Aster2 Cod',
        'RLineAster2Name': 'Aster2 Name',
        'StructureMission': 'Structure Mission',
        'InfrastructureId' : 'Infrastructure Id',
        'InfrastructureDescription': 'Infrastructure Description',
        'LaboratoryScopes': 'Laboratory Scopes',
        'ScopeID': 'Scope ID',
        'ScopeDescription': 'Scope Description',
        'PatentId': 'Patent Id',
        'PatentUniqueId': 'Patent Unique Id',
        'PatentTitle': 'Patent Title',
        'PatentImage': 'Patent Image',
        'PatentAbstract': 'Patent Abstract',
        'PatentUrlKnowledgeShare': 'Patent Url Knowledge Share',
        'PatentTechAreaId': 'Patent Tech-Area Id',
        'PatentAreaDescription': 'Area Description',
        'PatentInventors': 'Patent Inventors',
        'SpinoffId': 'Spinoff Id',
        'SpinoffPIva': 'Spinoff P.Iva',
        'SpinoffAgencyName': 'Spinoff Agency Name',
        'SpinoffImage': 'Spinoff Image',
        'SpinoffDescription': 'Spinoff Description',
        'SpinoffUnicalReferent': 'Unical Referent Spinoff',
        'SpinoffUnicalReferentId': 'Unical Referent Id',
        'TechAreaId': 'Spinoff Tech Area Id',
        'TechAreaDescription': 'Spinoff Area Description',
        'SpinoffAgencyUrl': 'Spinoff Agency Url',
        'IsSpinoff': 'Is Spinoff',
        'IsStartup': 'Is Startup',
        'PersonFunctions': ' Funzioni Persona',
        'ProjectId': 'Project Id',
        'TerritorialScopeId': 'Territorial Scope Id',
        'TerritorialScopeDescription': ' Territorial Scope Description',
        'TypeProgramId': 'Type Program Id',
        'TypeProgramDescription': 'Type Program Description',
        'ProjectTitle': 'Project Title',
        'ProjectDescription': 'Project Description',
        'ProjectAbstract': 'Project Abstract',
        'ProjectImage': 'Project Image',
        'ProjectYear': 'Project Year',
        'ProjectDepartmentId': 'Project Department Id',
        'FunctionDescription': 'Function Description',
        'FunctionCod': 'Function Cod',
    },
    'it': {
        'RegDidId': 'ID Regolamento Didattico',
        'RegDidState': 'Stato del Regolamento Didattico',
        'CdSId': 'ID Corso di Studi',
        'CdSCod': 'Codice Corso di Studi',
        'AcademicYear': 'Anno Accademico',
        'CdSName': 'Nome Corso di Studi',
        'DepartmentId': 'ID Dipartimento',
        'DepartmentCod': 'Codice Dipartimento',
        'DepartmentName': 'Nome Dipartimento',
        'DepartmentNameShort': 'Nome Dipartimento Breve',
        'CourseType': 'Tipologia Corso',
        'CourseTypeDescription': 'Tipologia Corso',
        'CourseClassCod': 'Codice Classe Corso',
        'CourseClassName': 'Classe Corso',
        'CourseInterClassCod': 'Codice Interclasse Corso',
        'CourseInterClassDes': 'Interclasse Corso',
        'CdSLanguage': 'Lingua',
        'CdSDuration': 'Durata',
        'CdSECTS': 'ECTS',
        'CdSAttendance': 'Frequenza Obbligatoria',
        'CdSIntro': 'Descrizione',
        'CdSDoc': 'Documento',
        'CdSVideo': 'Video',
        'CdSGoals': 'Obiettivi',
        'CdSAccess': 'Accesso',
        'CdSAdmission': 'Ammissione',
        'CdSProfiles': 'Profili',
        'CdSFinalTest': 'Test Finale',
        'CdSFinalTestMode': 'Modalità Test Finale',
        'CdSSatisfactionSurvey': 'Soddisfazione e condizione occupazionale (fonte Almalaurea)',
        'JointDegree' : 'Titolo Congiunto',
        'LaboratoryId': 'Id Laboratorio',
        'LaboratoryName': 'Nome Laboratorio',
        'LaboratoryURL': 'Pagina Web',
        'LaboratoryEquipment': 'Strumentazione',
        'Interdepartmental': 'Interdipartimentale',
        'InfrastructureName': 'Infrastruttura di Riferimento',
        'ExtraDepartments': 'Altri dipartimenti',
        'Area': 'Ambito',
        'Dimension': 'Dimensione',
        'ScientificDirector': 'Responsabile Scientifico',
        'ScientificDirectorId': 'Id Responsabile Scientifico',
        'StudyPlanId': 'ID Piano di Studi',
        'StudyPlanName': 'Piano di Studi',
        'StudyPlanCod': 'Codice Piano di Studi',
        'StudyActivities': 'Attività Formative',
        'StudyActivityID': 'ID Attività Formativa',
        'StudyActivityCod': 'Codice Attività Formativa',
        'StudyActivityRegDidId': 'ID Regolamento Didattico',
        'StudyActivityName': 'Nome Attività Formativa',
        'StudyActivityCdSID': 'Id Corso di Studi',
        'StudyActivityCdSCod': 'Codice Corso di Studi',
        'StudyActivityYear': 'Anno Corso',
        'StudyActivitySemester': 'Semestre',
        'StudyActivityECTS': 'ECTS',
        'StudyActivitySSD': 'SSD',
        'StudyActivityCompulsory': 'Frequenza Obbligatoria',
        'StudyActivityCdSName': 'Corso di Studi',
        'StudyActivityTeachingUnitType': 'Tipologia Insegnamento',
        'StudyActivityTeacherID': 'Matricola Docente',
        'StudyActivityTeacherName': 'Docente',
        'StudyActivityContent': 'Contenuti',
        'StudyActivityProgram': 'Programma',
        'StudyActivityLearningOutcomes': 'Obiettivi Formativi',
        'StudyActivityMethodology': 'Metodologie Didattiche',
        'StudyActivityEvaluation': 'Metodi di Valutazione',
        'StudyActivityTextbooks': 'Testi di Riferimento',
        'StudyActivityWorkload': 'Carico di Lavoro',
        'StudyActivityElearningLink': 'Link Aula Virtuale',
        'StudyActivityElearningInfo': 'Info per l\'Accesso all\'Aula Virtuale',
        'StudyActivityPrerequisites': 'Prerequisiti',
        'StudyActivitiesModules': 'Moduli',
        'StudyActivityAA': 'Anno Accademico',
        'StudyActivityLanguage': 'Lingua',
        'StudyActivityRoot': 'Attività Formativa Principale',
        'StudyActivityBorrowedFrom': 'Mutuata da',
        'StudyActivitiesBorrowedFromThis': 'Mutuate da questa',
        'StudyActivityPartitionCod': 'Codice Partizione',
        'StudyActivityPartitionDescription': 'Descrizione Partizione',
        'SingleStudyActivityPartitionCod': 'Codice Singola Partizione ',
        'SingleStudyActivityPartitionDescription': 'Descrizione Singola Partizione',
        'StudyActivityPartitionType': 'Tipologia Partizione',
        'StudyActivityPartitionStart': 'Inizio della Partizione',
        'StudyActivityPartitionEnd': 'Fine della Partizione',
        'Teacher': 'Pagina Docente',
        'TeacherID': 'ID Docente',
        'TeacherName': 'Nome',
        'TeacherRole': 'Ruolo',
        'TeacherRoleDescription': 'Ruolo',
        'TeacherSSD': 'SSD',
        'TeacherDepartmentID': 'ID Dipartimento',
        'TeacherDepartmentCod': 'Codice Dipartimento',
        'TeacherDepartmentName': 'Dipartimento',
        'TeacherSSDCod': 'SSD',
        'TeacherSSDDescription': 'SSD',
        'TeacherCode': 'Codice Fiscale',
        'TeacherFirstName': 'Nome',
        'TeacherLastName': 'Cognome',
        'TeacherOffice': 'Ufficio',
        'TeacherOfficeReference': 'Riferimento Ufficio',
        'TeacherEmail': 'Posta Elettronica',
        'TeacherPEC': 'Posta Elettronica Certificata',
        'TeacherPrivateEmail': 'Posta Elettronica Privata',
        'TeacherTelOffice': 'Telefono Ufficio',
        'TeacherTelCelOffice': 'Telefono Cellulare Ufficio',
        'TeacherTelCel': 'Telefono Cellulare',
        'TeacherTelDomicile': 'Telefono Domicilio',
        'TeacherTelResidence': 'Telefono Residenza',
        'TeacherFax': 'Fax',
        'TeacherSkype': 'Skype',
        'TeacherWebSite': 'URL Sito WEB',
        'TeacherCV': 'Curriculum Vitae',
        'TeacherFunctions': 'Ruoli Amministrativi',
        'Office': 'Ufficio',
        'OfficeReference': 'Riferimento Ufficio',
        'Email': 'Posta Elettronica',
        'PEC': 'Posta Elettronica Certificata',
        'PrivateEmail': 'Posta Elettronica Privata',
        'TelOffice': 'Telefono Ufficio',
        'TelCelOffice': 'Telefono Cellulare Ufficio',
        'TelCel': 'Telefono Cellulare',
        'TelDomicile': 'Telefono Domicilio',
        'TelResidence': 'Telefono Residenza',
        'Fax': 'Fax',
        'Skype': 'Skype',
        'WebSite': 'URL Sito WEB',
        'CV': 'Curriculum Vitae',
        'Contacts': 'Contatti',
        'ContactType': 'Tipo Contatto',
        'Contact': 'Contatto',
        'Function': 'Funzione',
        'Structure': 'Struttura',
        'Role': 'Ruolo',
        'RoleDescription': 'Ruolo',
        'ID': 'ID',
        'IdErc1': 'Id Erc1',
        'IdErc0': 'IdErc0',
        'Name': 'Nome',
        'RGroupID': 'ID Gruppo di Ricerca',
        'RGroupName': 'Nome Gruppo di Ricerca',
        'RGroupDescription': 'Descrizione Gruppo di Ricerca',
        'RLineID': 'ID Linea di Ricerca',
        'RLineDescription': 'Descrizione Linea di Ricerca',
        'RLineResults': 'Risultati Linea di Ricerca',
        'RLineERC0Id': 'ID Linea di Ricerca ERC0',
        'RLineERC0Name': 'Nome Linea di Ricerca ERC0',
        'DepartmentID': 'ID Dipartimento',
        'DoctorateCdsCOD': 'Codice Corso di Studi',
        'DoctorateCdsName': 'Nome Corso di Studi',
        'DoctorateRegID': 'ID Regolamento Dottorato',
        'DoctorateRegCOD': 'Codice Regolamento Dottorato',
        'DoctorateCdSDuration': 'Durata',
        'DoctorateCdSECTS': 'ECTS',
        'DoctorateCdSAttendance': 'Frequenza Obbligatoria',
        'CourseName': 'Nome Corso',
        'CycleNumber': 'Numero Ciclo',
        'StudyPlanCOD': 'Codice Piano di Studi',
        'StudyPlanDes': 'Descrizione Piano di Studi',
        'FUNZIONI': 'Funzioni',
        'COMPETENZE': 'Competenze',
        'SBOCCHI': 'Sbocchi',
        'StructureCod': 'Codice Struttura',
        'StructureTypeName': 'Tipologia',
        'StructureName': 'Nome',
        'StructureTypeCOD': 'Tipologia',
        'StructureFatherId': 'Struttura Riferimento',
        'StructureFatherName': 'Struttura Riferimento',
        'StructureEmail': 'Email',
        'StructurePec': 'Pec',
        'StructureTfr': 'Telefono',
        'StructurePersonnelFunctions': 'Personale Amministrativo',
        'LaboratoryId': 'ID',
        'CompletionReferentName': 'Referente Compilazione',
        'CompletionReferentId': 'Referente Compilazione',
        'ScientificDirectorId': 'Responsabile Scientifico',
        'ScientificDirectorName': 'Responsabile Scientifico',
        'LaboratoryName': 'Nome',
        'LaboratoryAcronym': 'Acronimo',
        'LaboratoryLogo': 'Logo',
        'DepartmentReferentId': 'Dipartimento di Riferimento',
        'DepartmentReferentCod': 'Codice Dipartimento di Riferimento',
        'DepartmentReferentName': 'Dipartimento di Riferimento',
        'LaboratoryScope': 'Ambito',
        'LaboratoryServicesScope': 'Finalità  dei servizi',
        'LaboratoryResearchScope': 'Finalità Ricerca',
        'LaboratoryTeachingScope': 'Finalità Didattica',
        'LaboratoryActivities': 'Attività',
        'LaboratoryErc1': 'Erc 1',
        'LaboratoryResearchPersonnel': 'Finalità di ricerca',
        'LaboratoryTechPersonnel': 'Personale Tecnico',
        'LaboratoryOfferedServices': 'Servizi Offerti',
        'LaboratoryLocation': 'Ubicazione',
        'LocationBuilding': 'Edificio',
        'LocationFloor': 'Piano',
        'LocationNotes': 'Note',
        'ServiceName': 'Nome',
        'ServiceDescription': 'Descrizione',
        'TechPersonnelID': 'ID',
        'TechPersonnelName': 'Nome',
        'TechPersonnelRole': 'Ruolo',
        'ResearchPersonnelID': 'ID',
        'ResearchPersonnelName': 'Nome',
        'LaboratoryErc1Cod': 'Codice Erc1',
        'LaboratoryErc1Description': 'Descrizione Erc1',
        'LaboratoryErc0Cod': 'Codice Erc0',
        'LaboratoryErc0Description': 'Descrizione Erc0',
        'LaboratoryActivityType': 'Tipologia Attività',
        'Description': 'Descrizione',
        'PublicationId': 'ID',
        'PublicationTitle': 'Titolo',
        'PublicationAbstract': 'Abstract',
        'PublicationCollection': 'Collection',
        'PublicationCommunity': 'Tipologia',
        'Publication': 'Pubblicazione',
        'PublicationLabel': 'Tipologia Pubblicazione',
        'PublicationContributors': 'Tutti gli autori',
        'PublicationAuthors': 'Autori Unical',
        'PublicationYear': 'Anno di Pubblicazione',
        'AuthorId': 'ID',
        'AuthorName': 'Nome',
        'CommunityId': 'Id',
        'CommunityName': 'Nome',
        'PublicationReferenceAuthor': 'Autore Principale',
        'Erc1List': 'Lista Erc1 Associati',
        'Erc2List': 'Lista Erc2 Associati',
        'PublicationUrl': 'Url Pubblicazione',
        'TeacherCVFull':'CV completo',
        'TeacherCVShort':'CV breve',
        'Teachers': 'Docenti',
        'RLineErc2ID': 'Codice Erc2',
        'RLineErc2Name': 'Nome Erc2',
        'RYear': 'Anno di ricerca',
        'RLineAster2ID': 'ID Aster2',
        'RLineAster2Name': 'Nome Aster2',
        'Hours': 'Ore',
        'Cover': 'Peso',
        'CodErc2': 'Codice Erc2',
        'RLineAster2Id': 'Codice Aster2',
        'RLineAster2Name': 'Nome Aster2',
        'StructureMission': 'Obiettivo Struttura',
        'InfrastructureId' : 'Id Infrastruttura',
        'InfrastructureDescription': 'Descrizione Infrastruttura',
        'LaboratoryScopes': 'Finalità Laboratorio',
        'ScopeID': 'ID Finalità',
        'ScopeDescription': 'Descrizione Finalità',
        'PatentId': 'Id Brevetto',
        'PatentUniqueId': 'Id Univoco Brevetto',
        'PatentTitle': 'Titolo Brevetto',
        'PatentImage': 'Immagine Brevetto',
        'PatentAbstract': 'Abstract Brevetto',
        'PatentUrlKnowledgeShare': 'Url Knowledge Share Brevetto',
        'PatentTechAreaId': 'Area Tecnologica Brevetto',
        'PatentAreaDescription': 'Area Tecnologica',
        'PatentInventors': 'Inventori Brevetto',
        'SpinoffId': 'Id Spinoff',
        'SpinoffPIva': 'P. Iva Spinoff',
        'SpinoffAgencyName': 'Nome Azienda Spinoff',
        'SpinoffImage': 'Immagine Spinoff',
        'SpinoffDescription': 'Descrizione Spinoff',
        'SpinoffUnicalReferent': 'Referente Unical Spinoff',
        'SpinoffUnicalReferentId': 'Matricola Referente Unical',
        'TechAreaId': 'Id Area Tecnologica Spinoff',
        'TechAreaDescription': 'Area Tecnologica Spinoff',
        'SpinoffAgencyUrl': 'Url Azienda Spinoff',
        'IsSpinoff': 'Spinoff',
        'IsStartup': 'Startup',
        'PersonFunctions': ' Funzioni Persona',
        'ProjectId': 'Id Progetto',
        'TerritorialScopeId': 'Id Ambito Territoriale',
        'TerritorialScopeDescription': ' Decrizione Ambito Territoriale',
        'TypeProgramId': 'Id Tipologia Programma',
        'TypeProgramDescription': 'Descrizione Tipologia Programma',
        'ProjectTitle': 'Titolo Progetto',
        'ProjectDescription': 'Descrizione Progetto',
        'ProjectAbstract': 'Abstract Progetto',
        'ProjectImage': 'Immagine Progetto',
        'ScientificDirectors': 'Responsabili Scientifici',
        'ProjectYear': 'Anno Avvio Progetto',
        'ProjectDepartmentId': 'Dipartimento Progetto',
        'FunctionDescription': 'Descrizione Funzione',
        'FunctionCod': 'Codice Funzione',

    }
}
