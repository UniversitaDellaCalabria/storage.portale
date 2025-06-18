# VIEW SUMMARY AND DESCRIPTION
# Teachers
TEACHERS_LIST_SUMMARY = "List of all teachers"
TEACHERS_LIST_DESCRIPTION = (
    "Retrieves a list of current or active teachers involved in teaching activities, "
    "ordered by surname and name."
)

TEACHERS_RETRIEVE_SUMMARY = "Details of a specific teacher"
TEACHERS_RETRIEVE_DESCRIPTION = (
    "Retrieves detailed information about a specific teacher, including personal data, "
    "teaching roles, organizational affiliations, contact information, and CVs."
)
# Coverages
COVERAGES_LIST_SUMMARY = "List of teachers with teaching assignments"
COVERAGES_LIST_DESCRIPTION = (
    "Retrieves a list of teachers who have teaching coverage for at least one course. "
    "Includes department metadata and academic profile information, ordered by surname and name."
)
# Publications
PUBLICATIONS_LIST_SUMMARY = "List of publications"
PUBLICATIONS_LIST_DESCRIPTION = (
    "Retrieves a list of scientific publications, including metadata such as title, abstract, "
    "publication year, contributors, and collection details. Results are ordered by year and title."
)

PUBLICATIONS_RETRIEVE_SUMMARY = "Details of a specific publication"
PUBLICATIONS_RETRIEVE_DESCRIPTION = (
    "Retrieves detailed information about a specific publication, including associated authors, "
    "abstracts, publication type, and collection/community hierarchy."
)
TEACHERS_STUDY_ACTIVITY_RETRIEVE_SUMMARY = "Teacher study activity details"
TEACHERS_STUDY_ACTIVITY_RETRIEVE_DESCRIPTION = (
    "Retrieves the study activity associated with a specific teacher identified by their matricola. "
    "Returns the most recent available teaching activity with metadata such as course year, subject code, "
    "credits, and language details."
)
TEACHERS_MATERIALS_LIST_SUMMARY = "List of teaching materials"
TEACHERS_MATERIALS_LIST_DESCRIPTION = (
    "Retrieves a list of teaching materials associated with a specific teacher. "
    "Includes metadata such as title, publication date, visibility, and text content in multiple languages. "
    "If the user has the proper permissions, restricted materials may also be included."
)
TEACHERS_BASE_RESEARCH_LINES_LIST_SUMMARY = "List of base research lines"
TEACHERS_BASE_RESEARCH_LINES_LIST_DESCRIPTION = (
    "Retrieves the active base research lines for a given teacher. "
    "Includes details such as the research topic, visibility status, and ERC classification hierarchy. "
    "Administrative users and authorized staff can view inactive lines as well."
)
TEACHERS_APPLIED_RESEARCH_LINES_LIST_SUMMARY = "List of applied research lines"
TEACHERS_APPLIED_RESEARCH_LINES_LIST_DESCRIPTION = (
    "Retrieves the applied research lines associated with a specific teacher, identified by their matricola. "
    "Includes metadata such as title, project description, and ERC classification. "
    "Results are filtered to show only active and visible lines unless the user has administrative privileges."
)
TEACHERS_NEWS_LIST_SUMMARY = "List of teacher-specific news"
TEACHERS_NEWS_LIST_DESCRIPTION = (
    "Retrieves news and announcements associated with a specific teacher. "
    "Results include multilingual titles and content, publication dates, and validity periods. "
    "If the requesting user has management rights over the teacher, inactive and future content may also be included."
)
# Publications Community Types
PUBLICATIONS_COMMUNITY_TYPES_LIST_SUMMARY = "List of community types"
PUBLICATIONS_COMMUNITY_TYPES_LIST_DESCRIPTION = (
    "Retrieves all publication community types used to classify research outputs. "
    "Each item includes the community ID and its corresponding name."
)