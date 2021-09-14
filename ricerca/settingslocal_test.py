"""
Django settings for ricerca project.
Generated by 'django-admin startproject' using Django 3.0.8.
For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""


import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = '82^w&ie47r^!c8f6yeui@#6e*myi*o4sf3^u*o7+#3qk!tn^=s'
ALLOWED_HOSTS = ['*']
ADMIN_PATH = 'test_admin'
INSTALLED_APPS = [
    'accounts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'accounts.apps.AccountsConfig',
    'rest_framework',
    'ricerca_app',
    # 'silk',
    # 'ricerca_app.apps.RicercaAppConfig',
]
AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    # 'silk.middleware.SilkyMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # SameSite Cookie workaround
    #  'djangosaml2.middleware.SamlSessionMiddleware'
]

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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
        'CourseClassId': 'Course Class ID',
        'CourseClassName': 'Course Class Name',
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
        'ScientificDirector': 'Sceintific Director',
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
        'R&SLineID': 'Research Line ID',
        'R&SLineDescription': 'Description',
        'R&SLineResults': 'Results',
        'R&SLineERC0Id': 'ERC0 ID',
        'R&SLineERC0Name': 'ERC0 Name',
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
        'StructureId': 'Structure Id',
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
        'PublicationUrl': 'Publication Url',
        'TeacherCVFull':'Teacher CV Full',
        'TeacherCVShort':'Teacher CV Short',

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
        'CourseClassId': 'ID Classe Corso',
        'CourseClassName': 'Classe Corso',
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
        'R&SLineID': 'ID Linea di Ricerca',
        'R&SLineDescription': 'Descrizione Linea di Ricerca',
        'R&SLineResults': 'Risultati Linea di Ricerca',
        'R&SLineERC0Id': 'ID Linea di Ricerca ERC0',
        'R&SLineERC0Name': 'Nome Linea di Ricerca ERC0',
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
        'StructureId': 'ID',
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
        'PublicationUrl': 'Url Pubblicazione',
        'TeacherCVFull':'CV completo',
        'TeacherCVShort':'CV breve',
    }
}
