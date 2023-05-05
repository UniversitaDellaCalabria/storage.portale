def is_allowed(offices, phd):
    for office in offices:
        if office.office.name == phd:
            return True
    return False
