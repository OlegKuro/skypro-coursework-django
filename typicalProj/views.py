
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import redirect

from social_core.utils import setting_name
from social_core.actions import do_auth
from social_django.utils import psa

NAMESPACE = getattr(settings, setting_name('URL_NAMESPACE'), None) or 'social'

@never_cache
@psa(f'{NAMESPACE}:complete')
def auth(request, backend):
    if request.GET.get(REDIRECT_FIELD_NAME) is None:
        return redirect('login-social-backend', **{
            f'{REDIRECT_FIELD_NAME}': 'http://okhayatov.ga',
        })
    return do_auth(request.backend, redirect_name=REDIRECT_FIELD_NAME)