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

    # cors headers
    'corsheaders.middleware.CorsMiddleware',

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
        'RLineERC1Id': 'ERC1 ID',
        'RLineERC1Name': 'ERC1 Name',
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
        'DepartmentURL': 'URL',
        'StructureURL': 'URL',
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
        'InfrastructureDescription': 'Referent Infrastructure',
        'LaboratoryScopes': 'Laboratory Scopes',
        'ScopeID': 'Scope ID',
        'ScopeDescription': 'Scope Description',
        'PatentId': 'Patent Id',
        'PatentUniqueId': 'Patent Unique Id',
        'PatentTitle': 'Patent Title',
        'PatentImage': 'Patent Image',
        'PatentAbstract': 'Patent Abstract',
        'PatentUrlKnowledgeShare': 'Patent Knowledge Share',
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
        'TechAreaDescription': 'Tech Area',
        'SpinoffAgencyUrl': 'Spinoff Agency Url',
        'IsSpinoff': 'Is Spinoff',
        'IsStartup': 'Is Startup',
        'PersonFunctions': ' Funzioni Persona',
        'ProjectId': 'Project Id',
        'TerritorialScopeId': 'Territorial Scope Id',
        'TerritorialScopeDescription': 'Territorial Scope',
        'TypeProgramId': 'Type Program Id',
        'TypeProgramDescription': 'Program Description',
        'ProjectTitle': 'Project Title',
        'ProjectDescription': 'Description',
        'ProjectAbstract': 'Abstract',
        'ProjectImage': 'Project Image',
        'ProjectYear': 'Project Year',
        'ProjectDepartmentId': 'Project Department Id',
        'FunctionDescription': 'Function Description',
        'FunctionCod': 'Function Cod',
        'AreaCds': 'Cds Area',
        'CdsUrl': 'Url Cds',
        'Researchers': 'Researchers',
        'ResearcherId': 'ResearcherId',
        'ResearcherName': 'ResearcherName',
        'CF': 'Fiscal Code',
        'MasterTitle': 'Master Title',
        'HighFormationTypeId': 'High Formation Type Id',
        'HighFormationErogationMode': 'High Formation Erogation Mode',
        'HighFormationErogationModeDescription': 'High Formation Erogation Mode Description',
        'HighFormationHours': 'Hours',
        'HighFormationMonths': 'Months',
        'HighFormationCourseStructure': 'Course Structure',
        'HighFormationMinParticipants': 'Minimum Participants',
        'HighFormationMaxParticipants': 'Maximum Participants',
        'ListenersAccepted': 'Listeners Accepted',
        'MaxListeners': 'Maximum Listeners',
        'AdmissionRequirements': 'Admission Requirements',
        'TitleIssued': 'Title Issued',
        'DoubleTitle': 'Double Title',
        'SubscriptionFee': 'Subscription Fee',
        'ListenersFee': 'Listeners Fee',
        'WorkFunction': 'Work Function',
        'FormationObjectivesSummerSchool': 'Formation Objectives Summer School',
        'Skills': 'Skills',
        'JobOpportunities': 'Job Opportunities',
        'CourseObjectives': 'Course Objectives',
        'FinalTestMode': 'Final Test Mode',
        'NumModules': 'Nummber of Modules',
        'Internship': 'Internship',
        'InternshipHours': 'Internship Hours',
        'InternshipCFU': 'Internship CFU',
        'InternshipMonths': 'Internship Months',
        'TypeCompaniesInternship': 'Type Companies Internship',
        'ContentTimesCriteriaCFU': 'Content Times Criteria CFU',
        'ProjectWork': 'Project Work',
        'HighFormationMasterPartners': 'High Formation Master Partners',
        'PartnerDenomination': 'Partner Denomination',
        'PartnerURL': 'Partner URL',
        'PartnerType': 'Partner Type',
        'HighFormationMasterSelectionModes': 'High Formation Master Selection Modes',
        'SelectionType': 'Selection Type',
        'SelectionId': 'Selection Mode Id',
        'HighFormationMasterInternalCouncil': 'High Formation Master Internal Council',
        'PersonId': 'Person Id',
        'PersonName': 'Person Name',
        'HighFormationMasterExternalCouncil': 'High Formation Master External Council',
        'Institution': 'Institution',
        'PartnerId': 'Partner Id',
        'HighFormationMasterTeachingPlans': 'High Formation Master Teaching Plans',
        'TeachingPlanCFU': 'Teaching PlanC FU',
        'TeachingPlanFinalTest': 'Teaching Plan Final Test',
        'TeachingPlanSSD': 'Teaching Plan SSD',
        'TeachingPlanModule': 'Teaching Plan Module',
        'TeachingPlanHours': 'Teaching Plan Hours',
        'HighFormationMasterTeachingAssignments': 'High Formation Master Teaching Assignments',
        'TeachingAssignmentsModule': 'Teaching Assignments Module',
        'TeachingAssignmentsHours': 'Teaching Assignments Hours',
        'TeachingAssignmentsTeachers': 'Teaching Assignments Teachers',
        'TeachingAssignmentsQualification': 'Teaching Assignments Qualification',
        'TeachingAssignmentsInstitution': 'Teaching Assignments Institution',
        'TeachingAssignmentsType': 'Teaching Assignments Type',
        'IdAster1': 'Aster 1 Id',
        'IdAster2' : 'Aster 2 Id',
        'Aster1List': 'Aster1 List',
        'Aster2List': 'Aster2 List',
        'HighFormationMasterYear': ' High Formation Master Year',
        'OtherData': 'Other Data',
        'OfficesData': 'Offices Data',
        'DirectorId': 'Director Id',
        'DirectorName': 'Coordinator',
        'DeputyDirectorId': 'Deputy Director Id',
        'DeputyDirectorName': 'Deputy Coordinator',
        'SeatsNumber': 'Seats Number',
        'RegistrationMode': 'Registration Mode',
        'Order': 'Order',
        'OfficeName': 'Office Name',
        'OfficeDirector': 'Office Director',
        'OfficeDirectorName': 'Office Director Name',
        'Floor': 'Floor',
        'Timetables': 'Timetables',
        'OnlineCounter': 'Online Counter',
        'StudyActivityTeachingUnitTypeCod': 'Study Activity Teaching Unit Type Cod',
        'StudyActivityInterclassTeachingUnitTypeCod': 'Study Activity Interclass Teaching Unit Type Cod',
        'StudyActivityInterclassTeachingUnitType': 'Study Activity Interclass Teaching Unit Type',
        'ActivityType': 'Activity Type',
        'StudyActivityHours': 'Study Activity Hours',
        'StudyActivityAcademicYear': 'Study Activity Academic Year',
        'StudyActivityDevelopmentGoal': 'Study Activity Development Goal',
        'StudyActivityModalities': 'Study Activity Modalities',
        'ModalityActivityId': 'Modality Activity Id',
        'ModalityActivityCod': 'Modality Activity Cod',
        'ModalityActivityDescription': 'Modality Activity Description',
        'StudyActivityPartitionCod': 'Study Activity Partition Code',
        'StudyActivityPartitionDes': 'Study Activity Partition Description',
        'StudyActivityExtendedPartitionCod': 'Study Activity Extended Partition Code',
        'StudyActivityExtendedPartitionDes': 'Study Activity Extended Partition Description',
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
        'CdSFinalTest': 'Prova Finale',
        'CdSFinalTestMode': 'Modalità Prova Finale',
        'CdSSatisfactionSurvey': 'Soddisfazione e condizione occupazionale dei laureati (Almalaurea)',
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
        'IdAster1': 'Id Aster 1',
        'IdAster2' : 'Id Aster 2',
        'Name': 'Nome',
        'RGroupID': 'ID Gruppo di Ricerca',
        'RGroupName': 'Nome Gruppo di Ricerca',
        'RGroupDescription': 'Descrizione Gruppo di Ricerca',
        'RLineID': 'ID Linea di Ricerca',
        'RLineDescription': 'Descrizione Linea di Ricerca',
        'RLineResults': 'Risultati Linea di Ricerca',
        'RLineERC0Id': 'ID Linea di Ricerca ERC0',
        'RLineERC0Name': 'Nome Linea di Ricerca ERC0',
        'RLineERC1Id': 'ID Linea di Ricerca ERC1',
        'RLineERC1Name': 'Nome Linea di Ricerca ERC1',
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
        'DepartmentURL': 'URL',
        'StructureURL': 'URL',
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
        'InfrastructureDescription': 'Struttura di Riferimento',
        'LaboratoryScopes': 'Finalità Laboratorio',
        'ScopeID': 'ID Finalità',
        'ScopeDescription': 'Descrizione Finalità',
        'PatentId': 'Id Brevetto',
        'PatentUniqueId': 'Id Univoco Brevetto',
        'PatentTitle': 'Titolo Brevetto',
        'PatentImage': 'Immagine Brevetto',
        'PatentAbstract': 'Abstract Brevetto',
        'PatentUrlKnowledgeShare': 'Scheda Knowledge Share',
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
        'TechAreaDescription': 'Area Tecnologica',
        'SpinoffAgencyUrl': 'Url Azienda Spinoff',
        'IsSpinoff': 'Spinoff',
        'IsStartup': 'Startup',
        'PersonFunctions': ' Funzioni Persona',
        'ProjectId': 'Id Progetto',
        'TerritorialScopeId': 'Id Ambito Territoriale',
        'TerritorialScopeDescription': 'Ambito Territoriale',
        'TypeProgramId': 'Id Tipologia Programma',
        'TypeProgramDescription': 'Programma',
        'ProjectTitle': 'Titolo Progetto',
        'ProjectDescription': 'Descrizione',
        'ProjectAbstract': 'Abstract',
        'ProjectImage': 'Immagine Progetto',
        'ScientificDirectors': 'Responsabili Scientifici',
        'ProjectYear': 'Anno Avvio',
        'ProjectDepartmentId': 'Dipartimento Progetto',
        'FunctionDescription': 'Descrizione Funzione',
        'FunctionCod': 'Codice Funzione',
        'AreaCds': 'Area Cds',
        'CdsUrl': 'Url Cds',
        'Researchers': 'Ricercatori',
        'ResearcherId': 'Matricola Ricercatore',
        'ResearcherName': 'Nome Ricercatore',
        'CF': 'Codice Fiscale',
        'MasterTitle': 'Titolo Master',
        'HighFormationTypeId': 'Alta Formazione ID',
        'HighFormationErogationMode': 'Modalità di erogazione',
        'HighFormationHours': 'Ore',
        'HighFormationMonths': 'Mesi',
        'HighFormationCourseStructure': 'Sede Corso',
        'HighFormationMinParticipants': 'Numero Minimo Partecipanti',
        'HighFormationMaxParticipants': 'Numero Massimo Partecipanti',
        'ListenersAccepted': 'Uditori Ammessi',
        'MaxListeners': 'Numero Massimo Uditori',
        'AdmissionRequirements': 'Requisiti di Ammissione',
        'TitleIssued': 'Titolo Rilasciato',
        'DoubleTitle': 'Doppio Titolo',
        'SubscriptionFee': 'Quota di Iscrizione',
        'ListenersFee': 'Quota di Uditori',
        'WorkFunction': 'Funzione Lavoro',
        'FormationObjectivesSummerSchool': 'Obiettivi Formativi High School',
        'Skills': 'Competenze',
        'JobOpportunities': 'Sbocchi Occupazionali',
        'CourseObjectives': 'Obiettivi Formativi Corso',
        'FinalTestMode': 'Modalità Svolgimento Prova Finale',
        'NumModules': 'Numero Moduli',
        'Internship': 'Stage/Tirocinio',
        'InternshipHours': 'Ore Stage/Tirocinio',
        'InternshipCFU': 'CFU Stage/Tirocinio',
        'InternshipMonths': 'Mesi Stage/Tirocinio',
        'TypeCompaniesInternship': 'Tipologia Aziende Enti Tirocinio',
        'ContentTimesCriteriaCFU': 'Contenuti, Tempi e Criteri CFU',
        'ProjectWork': 'Progetto di Lavoro',
        'HighFormationMasterPartners': 'Partner del Master',
        'PartnerDenomination': 'Denominazione del Partner',
        'PartnerURL': 'Sito Web del Partner',
        'PartnerType': 'Tipologia del Partner',
        'HighFormationErogationModeDescription': 'Descrizione Modalità Erogazione',
        'HighFormationMasterSelectionModes': 'Modalità di Selezione Master',
        'SelectionType': 'Tipologia Selezione',
        'SelectionId': 'Id Modalita Selezione',
        'HighFormationMasterInternalCouncil': 'Consiglio Scientifico Interno',
        'HighFormationMasterYear': ' Anno Master Alta Formazione',
        'PersonId': 'Matricola Persona',
        'PersonName': 'Nome Persona',
        'HighFormationMasterExternalCouncil': 'Consiglio Scientifico Esterno',
        'Institution': 'Ente',
        'PartnerId': 'Id Partner',
        'HighFormationMasterTeachingPlans': 'Piani Didattici',
        'TeachingPlanCFU': 'CFU Piano Didattico',
        'TeachingPlanFinalTest': 'Prova Finale Piano Didattico',
        'TeachingPlanSSD': 'SSD Piano Didattico',
        'TeachingPlanModule': 'Modulo Piano Didattico',
        'TeachingPlanHours': 'Ore Piano Didattico',
        'HighFormationMasterTeachingAssignments': 'Alta Formazione Incarichi Didattici',
        'TeachingAssignmentsModule': 'Modulo Incarico Didattico',
        'TeachingAssignmentsHours': 'Ore Incarico Didattico',
        'TeachingAssignmentsTeachers': 'Docenti Incarico Didattico',
        'TeachingAssignmentsQualification': 'Qualifica Incarico Didattico',
        'TeachingAssignmentsInstitution': 'Ente Incarico Didattico',
        'TeachingAssignmentsType': 'Tipologia Incarico Didattico',
        'Aster1List': 'Lista Aster1',
        'Aster2List': 'Lista Aster2',
        'OtherData': 'Altri Dati',
        'OfficesData': 'Altri Dati Ufficio',
        'DirectorId': 'Matricola Coordinatore',
        'DirectorName': 'Coordinatore',
        'DeputyDirectorId': 'Matricola Vice-Coordinatore',
        'DeputyDirectorName': 'Vice-Coordinatore',
        'SeatsNumber': 'Numero Posti',
        'RegistrationMode': 'Modalità Iscrizione',
        'Order': 'Ordine',
        'OfficeName': 'Nome Ufficio',
        'OfficeDirector': 'Matricola Riferimento Ufficio',
        'OfficeDirectorName': 'Nome Riferimento Ufficio',
        'Floor': 'Piano',
        'Timetables': 'Orari',
        'OnlineCounter': 'Sportello Online',
        'StudyActivityTeachingUnitTypeCod': 'Codice Tipologia Insegnamento',
        'StudyActivityInterclassTeachingUnitTypeCod': 'Codice Tipologia Insegnamento Interclasse',
        'StudyActivityInterclassTeachingUnitType': 'Tipologia Insegnamento Interclasse',
        'ActivityType': 'Tipologia Attività Didattica',
        'StudyActivityHours': 'Ore Attività Didattica',
        'StudyActivityAcademicYear': 'Anno Accademico Attività Didattica',
        'StudyActivityDevelopmentGoal': 'Obiettivo Attività Didattica',
        'StudyActivityModalities': 'Modalità Attività Didattica',
        'ModalityActivityId': 'Id Modalità Attività Didattica',
        'ModalityActivityCod': 'Codice Modalità Attività Didattica',
        'ModalityActivityDescription': 'Descrizione Modalità Attività Didattica',
        'StudyActivityPartitionCod': 'Codice Partizionamento',
        'StudyActivityPartitionDes': 'Descrizione Partizionamento',
        'StudyActivityExtendedPartitionCod': 'Codice Esteso Partizionamento',
        'StudyActivityExtendedPartitionDes': 'Descrizione Estesa Partizionamento',
    }
}
