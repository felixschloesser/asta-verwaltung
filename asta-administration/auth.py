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

        if not name:
            fist_name = None
            last_name = None
            logging.info("No name provided, leaving first and last name empty.")
        else:
            name_list = name.split(' ') # split provided name at spaces

        if len(name_list) < 2:
            fist_name = None
            last_name = None
            logging.info("Provided name {} was too short, leaving first and last name empty.".format(name))

        elif len(name_list) == 2:
            fist_name = name_list.pop(0) # first provided name
            last_name = name_list.pop(1)  # second provided name

        elif len(name_list) > 2:
            # This is not good, but I dont know what else to do for longer names
            fist_name = name_list.pop(0) # first provided name
            last_name = name_list.pop()  # last provided name

        return first_name, last_name


    def create_user(self, claims):
        """Return object for a newly created user account."""
        username = self.get_username(claims)

        email = claims.get('email')

        first_name, last_name = self.get_first_and_last_name(claims)

        logging.info("Creating user: {}, {}, {}, {}".format(username, email, fist_name, last_name))

        return self.UserModel.objects.create_user(username,
                                                  email,
                                                  first_name=fist_name,
                                                  last_name=last_name,
                                                  is_staff=True)
