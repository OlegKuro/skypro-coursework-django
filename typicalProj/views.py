from django.http import HttpResponse
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
    redirect: HttpResponse = do_auth(request.backend, redirect_name=REDIRECT_FIELD_NAME)
    for header in ['Location', 'location']:
        if 'api:8000' in redirect.headers[header]:
            redirect.headers[header] = redirect.headers[header].replace('api:8000', 'okhayatov.ga')

    return redirect