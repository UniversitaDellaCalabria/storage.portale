from addressbook.models import Personale


def _is_user_scientific_director(request, laboratory):
    if request.user.taxpayer_id is None:
        return False
    else:
        user_profile = Personale.objects.filter(
            cod_fis=request.user.taxpayer_id
        ).first()
        return (
            user_profile is not None
            and laboratory.matricola_responsabile_scientifico == user_profile
        )


def _get_user_roles(request, laboratory, my_offices, is_validator):
    roles = {"superuser": False, "operator": False, "validator": False}
    if request.user.is_superuser:
        roles["superuser"] = True
        return roles
    if my_offices.exists() or _is_user_scientific_director(request, laboratory):
        roles["operator"] = True
    if is_validator:
        roles["validator"] = True
    return roles
