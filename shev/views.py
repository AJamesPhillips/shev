from django.views.generic import RedirectView


class RedirectRoot(RedirectView):
    def get_redirect_url(self):
        return '/admin/'
