
from django.utils.translation import ugettext_lazy as _

from ..utils.apps import ColabProxiedAppConfig


class ProxyJenkinsAppConfig(ColabProxiedAppConfig):
    name = 'colab.plugins.jenkins'
    verbose_name = 'Jenkins Proxy'

    menu = {
        'title': _('Code'),
        'links': (
            (_('Continuos Integration'), ''),
        ),
    }
