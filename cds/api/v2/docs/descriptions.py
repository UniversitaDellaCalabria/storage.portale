# VIEW SUMMARY AND DESCRIPTION

# DegreeType
DEGREETYPE_LIST_SUMMARY = "List of all degree types"
DEGREETYPE_LIST_DESCRIPTION = (
    "Retrieve a list of all available degree types with their codes and descriptions."
)

# AcademicYear
ACADEMICYEAR_LIST_SUMMARY = "List of all academic years"
ACADEMICYEAR_LIST_DESCRIPTION = (
    "Retrieve a list of all available academic years in descending order."
)

# StudyActivity
## List
STUDYACTIVITY_LIST_SUMMARY = "List of all study activities"
STUDYACTIVITY_LIST_DESCRIPTION = (
    "Retrieve a paginated list of all study activities with brief information. "
    "They can be filtered by academic year, course year, course code, department, "
    "SSD, teaching, teacher, and course year."
)
## Retrieve
STUDYACTIVITY_RETRIEVE_SUMMARY = "Retrieve a specific study activity"
STUDYACTIVITY_RETRIEVE_DESCRIPTION = (
    "Retrieve detailed information for a single study activity. "
    "The study activity is identified by its ID."
)

# CdsArea
CDSAREA_LIST_SUMMARY = "List of all the CDS areas"
CDSAREA_LIST_DESCRIPTION = (
    "Retrieve a list of all distinct Course of Study areas in Italian or in English."
)

# CdsExpired
CDSEXPIRED_LIST_SUMMARY = "List of expired courses"
CDSEXPIRED_LIST_DESCRIPTION = (
    "Retrieve a list of expired courses that are no longer active. "
    "This excludes courses that have been morphed into new ones."
)

# CdsMorph
## List
CDSMORPH_LIST_SUMMARY = "List all CDS morphing histories"
CDSMORPH_LIST_DESCRIPTION = (
    "Retrieve a list of all Course of Study morphing histories. "
    "This shows how the ids of the curses have evolved over time, tracking their "
    "previous versions."
)
## Retrieve
CDSMORPH_RETRIEVE_SUMMARY = "Retrieve a specific CDS morphing history"
CDSMORPH_RETRIEVE_DESCRIPTION = (
    "Retrieve detailed information for a single Course of Study morphing history. "
    "The morphing history is identified by its ID."
)

# AcademicPaths
## List
ACADEMICPATHS_LIST_SUMMARY = "List all Academic pathways for a specific didactic regulation"
ACADEMICPATHS_LIST_DESCRIPTION = (
    "API endpoints for managing academic pathways. Provides functionality to list all "
    "academic pathways and retrieve detailed information about specific pathways, "
    "including their associated study activities."
)
## Retrieve
ACADEMICPATHS_RETRIEVE_SUMMARY = "Retrieve a specific academic pathway"
ACADEMICPATHS_RETRIEVE_DESCRIPTION = (
    "Retrieve detailed information for a single academic pathway. "
    "The academic pathway is identified by its ID."
)
