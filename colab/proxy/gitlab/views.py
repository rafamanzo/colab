
from ..utils.views import ColabProxyView
from django.conf import settings


class GitlabProxyView(ColabProxyView):
    app_label = 'gitlab'
    diazo_theme_template = 'proxy/gitlab.html'
