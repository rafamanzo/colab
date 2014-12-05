
from django.conf import settings

from ..proxybase.views import ColabProxyView


class JenkinsProxyView(ColabProxyView):
    app_label = 'jenkins'
