from mozilla_django_oidc.auth import OIDCAuthenticationBackend

import logging

class CustomOpenidBackend(OIDCAuthenticationBackend):
    def verify_claims(self, claims):
        verified = super().verify_claims(claims)
        logging.debug(claims.get('group'))
        logging.debug(claims)
        logging.debug(claims.get('read_user'))
        logging.debug("reading_claims")
        is_admin = 'AStA/Mitglieder/Vorstand' in claims.get('group', [])
        logging.debug(is_admin)
        return verified and True

    def create_user(self, claims):
        """Return object for a newly created user account."""
        email = claims.get('email')

        logging.info("Creating debug")
        logging.info(claims)

        username = self.get_username(claims)
        return self.UserModel.objects.create_user(username, email)
