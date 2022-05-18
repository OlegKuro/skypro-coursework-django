
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME

from social_core.utils import setting_name
from social_core.actions import do_auth
from social_django.utils import psa

NAMESPACE = getattr(settings, setting_name('URL_NAMESPACE'), None) or 'social'

@never_cache
@psa(f'{NAMESPACE}:complete')
def auth(request, backend):
    if request.GET.get(REDIRECT_FIELD_NAME) is None:
        request.GET._mutable = True
        request.GET[REDIRECT_FIELD_NAME] = 'http://okhayatov.ga'
        request.GET._mutable = False
    return do_auth(request.backend, redirect_name=REDIRECT_FIELD_NAME)