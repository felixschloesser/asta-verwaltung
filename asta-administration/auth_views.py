import time

from django.views.generic import View

from django.contrib import messages, auth

from django.http import HttpResponseRedirect

from mozilla_django_oidc.views import OIDCAuthenticationCallbackView

class OIDCAuthenticationCallbackWithMessagesView(OIDCAuthenticationCallbackView):

    def login_failure(self):
        messages.add_message(self.request, 50, 'Angemeldung fehlgeschlagen.', extra_tags="danger")

        return HttpResponseRedirect(self.failure_url)

    def login_success(self):
        messages.success(self.request, 'Anmeldung erfolgreich.')

        auth.login(self.request, self.user)

        # Figure out when this id_token will expire. This is ignored unless you're
        # using the RenewIDToken middleware.
        expiration_interval = self.get_settings('OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS', 60 * 15)
        self.request.session['oidc_id_token_expiration'] = time.time() + expiration_interval

        return HttpResponseRedirect(self.success_url)
