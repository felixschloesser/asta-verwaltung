from mozilla_django_oidc.auth import OIDCAuthenticationBackend

import logging

class CustomOpenidBackend(OIDCAuthenticationBackend):
    def verify_claims(self, claims):
        verified = super().verify_claims(claims)
        logging.debug(claims.get('group', []))
        print(claims.get('group', []))
        is_admin = 'AStA/Mitglieder/Vorstand' in claims.get('group', [])
        return verified and is_admin

    def create_user(self, claims):
        """Return object for a newly created user account."""
        email = claims.get('email')

        logging.info("Creating debug")
        logging.info(claims)

        username = self.get_username(claims)
        return self.UserModel.objects.create_user(username, email)
