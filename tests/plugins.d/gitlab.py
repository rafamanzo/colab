from django.utils.translation import ugettext_lazy as _
from colab.plugins.utils.menu import colab_url_factory

name = 'colab_gitlab'
verbose_name = 'Gitlab Proxy'

upstream = 'localhost'
#middlewares = []

urls = {
    'include': 'colab_gitlab.urls',
    'namespace': 'gitlab',
    'prefix': 'gitlab',
}

menu_title = _('Code')

url = colab_url_factory('gitlab')

menu_urls = (
    url(display=_('Profile'), viewname='gitlab', kwargs={'path': '/profile/anonymous'}, auth=False),
    url(display=_('Profile Two'), viewname='gitlab', kwargs={'path': '/profile/logged'}, auth=True),
)
