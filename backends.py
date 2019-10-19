"""CAS authentication backend"""
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from vanila_djangocore_cas.signals import cas_user_authenticated

from vanila_djangocore_cas.utils import  validateService, createSessionTicket, createVanila_cas_model

__all__ = ['CASBackend']


class CASBackend(ModelBackend):
    """CAS authentication backend"""

    def authenticate(self, request, ticket, service):
        """Verifies CAS ticket and gets or creates User object"""

        id, username, group = validateService(ticket,service)
        print (username)

        if not username:
            return None

        username = self.clean_username(username)

        UserModel = get_user_model()

        # Note that this could be accomplished in one try-except clause, but
        # instead we use get_or_create when creating unknown users since it has
        # built-in safeguards for multiple threads.
        if True:
            user_kwargs = {
                UserModel.USERNAME_FIELD: username
            }

            user, created = UserModel._default_manager.get_or_create(**user_kwargs)
            if created:
                user = self.configure_user(user)
                createSessionTicket(request, ticket)
                createVanila_cas_model(request, user, id, group)
        else:
            created = False
            try:
                if settings.CAS_LOCAL_NAME_FIELD:
                    user_kwargs = {
                        settings.CAS_LOCAL_NAME_FIELD: username

                    }
                    user = UserModel._default_manager.get(**user_kwargs)
                else:
                    user = UserModel._default_manager.get_by_natural_key(username)
            except UserModel.DoesNotExist:
                pass

        if not self.user_can_authenticate(user):
            return None

        return user

    # ModelBackend has a `user_can_authenticate` method starting from Django
    # 1.10, that only allows active user to log in. For consistency,
    # django-cas-ng will have the same behavior as Django's ModelBackend.
    if not hasattr(ModelBackend, 'user_can_authenticate'):
        def user_can_authenticate(self, user):
            return True

    def get_user_id(self, attributes):
        """
        For use when CAS_CREATE_USER_WITH_ID is True. Will raise ImproperlyConfigured
        exceptions when a user_id cannot be accessed. This is important because we
        shouldn't create Users with automatically assigned ids if we are trying to
        keep User primary key's in sync.
        """
        if not attributes:
            raise ImproperlyConfigured("CAS_CREATE_USER_WITH_ID is True, but "
                                       "no attributes were provided")

        user_id = attributes.get('id')

        if not user_id:
            raise ImproperlyConfigured("CAS_CREATE_USER_WITH_ID is True, but "
                                       "`'id'` is not part of attributes.")

        return user_id

    def clean_username(self, username):
        """
        Performs any cleaning on the "username" prior to using it to get or
        create the user object.  Returns the cleaned username.
        By default, changes the username case according to
        `settings.CAS_FORCE_CHANGE_USERNAME_CASE`.
        """

        return username

    def configure_user(self, user):
        """
        Configures a user after creation and returns the updated user.
        By default, returns the user unmodified.

        """

        return user

    def bad_attributes_reject(self, request, username, attributes):
        return False