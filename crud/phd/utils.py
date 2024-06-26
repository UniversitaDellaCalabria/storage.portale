def is_allowed(user, offices, phd):
    if not user: return False
    if user.is_superuser: return True
    if not offices: return False
    if not phd: return False
    for office in offices:
        if office.office.name == phd:
            return True
    return False
