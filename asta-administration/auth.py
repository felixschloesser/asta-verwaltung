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

        authorized_groups = [
            'asta/mitarbeitende',
            'asta/mitglieder/vorstand',
            'asta/mitglieder/it',
        ]

        # Return True if any of the groups in the authorized groups list is found in the claimed groups
        authorized = any(item in claimed_groups for item in authorized_groups)

        return verified and authorized


    def get_username(self, claims):
        nickname = claims.get('nickname')
        return nickname


    def create_user(self, claims):
        """Return object for a newly created user account."""
        email = claims.get('email')
        name = claims.get('name').split(' ')
        if len(name) >= 2:
            fist_name = name.pop(0)
            last_name = name.pop()
        else:
            fist_name = name.pop(0)
            last_name = ""


        logging.info("Creating debug")
        logging.info(claims)

        username = self.get_username(claims)
        return self.UserModel.objects.create_user(username,
                                                  email,
                                                  first_name=fist_name,
                                                  last_name=last_name,
                                                  is_staff=True)
