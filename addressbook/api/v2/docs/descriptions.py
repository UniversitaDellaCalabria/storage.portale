# VIEW SUMMARY AND DESCRIPTION

# Personnel CF ViewSet
PERSONNEL_CF_LIST_SUMMARY = "List of active personnel with fiscal codes"
PERSONNEL_CF_LIST_DESCRIPTION = (
    "Retrieves a paginated list of active personnel (non-terminated employees with active contracts) "
    "including their fiscal codes, matricola, names, roles, and organizational unit information. "
    "Results are ordered by surname and can be filtered using various criteria. "
    "Only returns essential personnel data for identification and organizational purposes."
)

# Addressbook ViewSet
ADDRESSBOOK_LIST_SUMMARY = "List of addressbook entries"
ADDRESSBOOK_LIST_DESCRIPTION = (
    "Retrieves a paginated list of personnel in the addressbook, including both active employees "
    "and teachers with current or recent teaching assignments. Results are ordered by surname and name. "
    "Can be filtered using various criteria to narrow down the results."
)

ADDRESSBOOK_DETAIL_SUMMARY = "Get detailed addressbook entry"
ADDRESSBOOK_DETAIL_DESCRIPTION = (
    "Retrieves detailed information for a specific person in the addressbook by their matricola. "
    "Includes comprehensive contact information, roles, organizational functions, CV data, "
    "and teaching status. Supports both active personnel and teachers with recent assignments."
)

# Addressbook Full ViewSet
ADDRESSBOOK_FULL_LIST_SUMMARY = "List of full addressbook entries (authenticated)"
ADDRESSBOOK_FULL_LIST_DESCRIPTION = (
    "Retrieves a paginated list of personnel in the addressbook with full access to all data. "
    "Requires authentication. Includes both active employees and teachers with current or recent "
    "teaching assignments. Results are ordered by surname and name and can be filtered."
)

ADDRESSBOOK_FULL_DETAIL_SUMMARY = "Get full detailed addressbook entry (authenticated)"
ADDRESSBOOK_FULL_DETAIL_DESCRIPTION = (
    "Retrieves comprehensive detailed information for a specific person by matricola or fiscal code. "
    "Requires authentication. Includes all available contact information, roles with start dates, "
    "organizational functions, CV data, and teaching status. Supports lookup by both matricola and fiscal code."
)

# Addressbook Structures ViewSet
ADDRESSBOOK_STRUCTURES_LIST_SUMMARY = "List of organizational structures"
ADDRESSBOOK_STRUCTURES_LIST_DESCRIPTION = (
    "Retrieves a paginated list of active organizational structures (departments, faculties, centers, etc.) "
    "that are currently valid. Includes structure code, name, and type information. "
    "Results can be filtered by structure type or other criteria and are useful for understanding "
    "the organizational hierarchy of the institution."
)

# Roles ViewSet
ROLES_LIST_SUMMARY = "List of available personnel roles"
ROLES_LIST_DESCRIPTION = (
    "Retrieves a paginated list of all distinct personnel roles present in the system. "
    "Includes role codes and their descriptions, ordered alphabetically by role description. "
    "Useful for understanding the different types of positions and roles within the organization, "
    "such as academic positions, administrative roles, and technical staff classifications."
)