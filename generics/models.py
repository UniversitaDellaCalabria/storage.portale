from django.db import models

from organizational_area.models import OrganizationalStructureOfficeEmployee


class PermissionsModAbstract(models.Model):
    @classmethod
    def get_offices_names(cls, **kwargs):
        """
        Returns a tuple containing the names of the relevant offices
        for this model
        """
        raise NotImplementedError()

    @classmethod
    def user_has_offices(cls, user, **kwargs):
        """
        Returns whether or not the user is part of any office related to the model,
        without performing any additional checks
        """
        return cls._get_all_user_offices(user, **kwargs).exists()

    @classmethod
    def can_user_create_object(cls, user, **kwargs):
        """
        Returns whether or not the user can create an object
        """
        return False

    @classmethod
    def _get_all_user_offices(cls, user, **kwargs):
        """
        Returns a queryset containing all the active offices a user is part of,
        among the ones related to the model, without performing any additional checks
        """
        return OrganizationalStructureOfficeEmployee.objects.filter(
            employee=user,
            office__is_active=True,
            office__name__in=cls.get_offices_names(),
            office__organizational_structure__is_active=True,
        )

    def _is_valid_office(self, office_name, all_user_offices, **kwargs):
        """
        Performs advanced checks on an office record: all_user_offices.get(office__name=office_name)

        example:
            check if the given office's unique_code matches the department code related to the object
        """
        return True

    def _check_access_permission(self, user_offices_names, **kwargs):
        """
        Given the offices names the user's already been checked to be part of,
        returns whether or not they have the permission to access the object

        default: the user is part of at least one office related to the model
        """
        return len(user_offices_names) > 0

    def _check_edit_permission(self, user_offices_names, **kwargs):
        """
        Given the offices names the user's already been checked to be part of,
        returns whether or not they have the permission to edit the object
        """
        return False

    def _check_lock_permission(self, user_offices_names, **kwargs):
        """
        Given the offices names the user's already been checked to be part of,
        returns whether or not they have the permission to acquire a lock on the object
        """
        return False

    def get_user_offices_names(self, user, **kwargs):
        """
        Returns a tuple containing the offices names a user is part of,
        among the ones returned by get_offices_names(),
        that matches all the conditions of _is_valid_office()
        """
        try:
            self._all_user_offices = self._all_user_offices
        except AttributeError:
            self._all_user_offices = {}

        # avoid querying the same offices for the same user multiple times on the same object
        if user not in self._all_user_offices:
            self._all_user_offices[user] = self._get_all_user_offices(user, **kwargs)
        return tuple(
            user_office.office.name
            for user_office in self._all_user_offices[user]
            if self._is_valid_office(
                user_office.office.name, self._all_user_offices[user], **kwargs
            )
        )

    def get_user_permissions_and_offices(self, user, **kwargs):
        """
        Returns a dict containing whether or not the user possesses
        the following permissions: access, edit, lock,
        together with offices: user's offices names
        """
        user_offices_names = self.get_user_offices_names(user, **kwargs)
        return {
            "permissions": {
                "access": user.is_superuser
                or self._check_access_permission(user_offices_names, **kwargs),
                "edit": user.is_superuser
                or self._check_edit_permission(user_offices_names, **kwargs),
                "lock": user.is_superuser
                or self._check_lock_permission(user_offices_names, **kwargs),
            },
            "offices": user_offices_names,
        }

    class Meta:
        abstract = True


class InsModAbstract(models.Model):
    dt_ins = models.DateTimeField(db_column="DT_INS", auto_now_add=True)
    dt_mod = models.DateTimeField(
        db_column="DT_MOD", auto_now=True, blank=True, null=True
    )

    class Meta:
        abstract = True


class VisibileModAbstract(models.Model):
    visibile = models.BooleanField(db_column="VISIBILE", default=False)

    class Meta:
        abstract = True
