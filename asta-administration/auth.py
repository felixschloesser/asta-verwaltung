from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group

from mozilla_django_oidc.auth import OIDCAuthenticationBackend

import logging

class CustomOpenidBackend(OIDCAuthenticationBackend):
    def verify_claims(self, claims):
        verified = super().verify_claims(claims)
        logging.debug(claims.get('group'))
        logging.debug(claims)
        logging.debug(claims.get('read_user'))
        logging.debug("reading_claims")

        claimed_groups = claims.get('groups', [])

        # Groups as set in GitLab
        authorized_groups = [
            'asta/mitarbeitende',
            'asta/mitglieder/vorstand',
            'asta/mitglieder/referate/it',
        ]

        # Return True if any of the groups in the authorized groups list is found in the claimed groups
        authorized = any(group in claimed_groups for group in authorized_groups)

        return verified and authorized


    def get_username(self, claims):
        # Using the RZ-Kennung from the nickname field as username
        nickname = claims.get('nickname')
        return nickname


    def get_first_and_last_name(self, claims):
        # OpenID just returns a single name string,
        # but Django would like to have seperate first and last names.
        # Therefore we assume most names have two parts seperated by spaces
        # and if the name is longer just use the first and last part.

        name = claims.get('name')

        first_name = ""
        last_name = ""

        if name:
            name_list = name.split(' ') # split provided name at spaces
        else:
            logging.info("No name provided, leaving first and last name empty.")
            return first_name, last_name

        if len(name_list) < 2:
            logging.info("Provided name {} was too short, leaving first and last name empty.".format(name))

        elif len(name_list) == 2:
            first_name = name_list[0] # first provided name
            last_name = name_list[1]  # second provided name

        elif len(name_list) > 2:
            # This is not good, but I dont know what else to do for longer names
            first_name = name_list[0] # first provided name
            last_name = name_list[-1]  # last provided name
            logging.info("Provided name {} was too long, naïvly using the first and last name provided name.".format(name))


        return first_name, last_name


    def get_groups(self, claims):
        claimed_groups = claims.get('groups', [])

        groups = []

        # Group with permission to access the Key Management System
        # Groups who can access it as set in GitLab
        schlüsselsystem_groups = ['asta/mitarbeitende',
                                  'asta/mitglieder/referate/it']

        if any(group in claimed_groups for group in schlüsselsystem_groups):
            # Check if the group "Schlüsselverwaltung" exists in Django
            try:
                group = Group.objects.filter(name="Schlüsselverwaltung").get()
                groups.append(group.id)
                logging.info("Adding 'Schlüsselverwaltung' to the users groups")
            except ObjectDoesNotExist:
                logging.critical("Can't find the group 'Schlüsselverwaltung', create it in the admin first.")
        else:
            logging.debug("None of the claimed of groups is allowed to administer the Schlüsselverwaltung")

        return groups


    def is_superuser(self, claims):
        claimed_groups = claims.get('groups', [])

        # Groups as set in GitLab
        superuser_groups = ['asta/mitglieder/referate/it']

        is_superuser = any(group in claimed_groups for group in superuser_groups)

        return is_superuser


    def is_staff(self, claims):
        claimed_groups = claims.get('groups', [])

        # Groups as set in GitLab
        staff_groups = ['asta/mitarbeitende',
                        'asta/mitglieder/referate/it']

        is_staff = any(group in claimed_groups for group in staff_groups)

        return is_staff


    def create_user(self, claims):
        """Return object for a newly created user account."""
        username = self.get_username(claims)

        email = claims.get('email')

        first_name, last_name = self.get_first_and_last_name(claims)

        user = self.UserModel.objects.create_user(username,
                                                  email,
                                                  first_name=first_name,
                                                  last_name=last_name)
        logging.info("Created User: {}".format(username))
        logging.debug("User Params: {}, {}, {}, {}".format(username, email, first_name, last_name))

        user.is_staff = self.is_staff(claims)
        logging.debug("Is staff: {}".format(user.is_staff))

        user.is_superuser = self.is_superuser(claims)
        logging.debug("Is superuser: {}".format(user.is_superuser))

        groups = self.get_groups(claims)
        logging.debug("Groups: {}".format(groups))

        user.groups.set(groups)
        logging.info("User {} is in groups: {}".format(username, groups))

        return user


    def update_user(self, user, claims):
        """Update existing user with new claims, if necessary save, and return user"""
        user.is_staff = self.is_staff(claims)
        logging.debug("Is staff: {}".format(user.is_staff))

        user.is_superuser = self.is_superuser(claims)
        logging.debug("Is superuser: {}".format(user.is_superuser))

        groups = self.get_groups(claims)
        logging.debug("Groups: {}".format(groups))

        user.groups.set(groups)

        user.save()
        logging.info("User {} is now in groups: {}".format(user.username, groups))

        return user
