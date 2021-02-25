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
            'asta/mitglieder/it',
        ]

        # Return True if any of the groups in the authorized groups list is found in the claimed groups
        authorized = any(item in claimed_groups for item in authorized_groups)

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

        first_name = None
        last_name = None

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

        return first_name, last_name

    def is_staff(self, claims):
        claimed_groups = claims.get('groups', [])

        # Groups as set in GitLab
        staff_groups = [
            'asta/mitarbeitende',
            'asta/mitglieder/it',
        ]

        return any(item in claimed_groups for item in staff_groups)
  

    def create_user(self, claims):
        """Return object for a newly created user account."""
        username = self.get_username(claims)

        email = claims.get('email')

        first_name, last_name = self.get_first_and_last_name(claims)

        is_staff = self.is_staff(claims)

        logging.info("Creating user: {}, {}, {}, {}".format(username, email, first_name, last_name, is_staff))

        return self.UserModel.objects.create_user(username,
                                                  email,
                                                  first_name=first_name,
                                                  last_name=last_name,
                                                  is_staff=True)
