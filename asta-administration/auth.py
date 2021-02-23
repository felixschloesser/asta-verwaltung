from mozilla_django_oidc.auth import OIDCAuthenticationBackend

import logging

class MyOIDCAB(OIDCAuthenticationBackend):
    def verify_claims(self, claims):
        verified = super(MyOIDCAB, self).verify_claims(claims)
        is_admin = 'vorstand' in claims.get('group', [])
        return verified and is_admin

    def create_user(self, claims):
        """Return object for a newly created user account."""
        email = claims.get('email')
        
        logging.info("Creating debug")
        logging.info(claims)

        username = self.get_username(claims)
        return self.UserModel.objects.create_user(username, email)