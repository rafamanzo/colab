
from django.conf import settings
from django.conf.urls import patterns, url

from .views import (UserProfileDetailView, UserProfileUpdateView, LoginView,
                    ManageUserSubscriptionsView, ChangeXMPPPasswordView)

from colab.accounts import views
from django.contrib.auth import views as auth_views


BROWSERID_ENABLED = getattr(settings, 'BROWSERID_ENABLED', False)


if not BROWSERID_ENABLED:
    urlpatterns = patterns('',
        url(r'^login/?$', 'django.contrib.auth.views.login', name='login'),

        url(r'^logout/?$',  'django.contrib.auth.views.logout',
            {'next_page':'home'}, name='logout'),

        url(r'^password-reset-done/?$', 'colab.accounts.views.password_reset_done_custom',
            name="password_reset_done"),
        url(r'^password-reset-complete/$', 'colab.accounts.views.password_reset_complete_custom',
            name="password_reset_complete"),

        url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
            auth_views.password_reset_confirm,
            {'template_name':'registration/password_reset_confirm_custom.html'},
            name="password_reset_confirm"),

        url(r'^password-reset/?$', auth_views.password_reset,
            {'template_name':'registration/password_reset_form_custom.html'},
            name="password_reset"),

        url(r'^change-password/?$',auth_views.password_change,
            {'template_name':'registration/password_change_form_custom.html'},
            name='password_change'),

        url(r'^change-password-done/?$',
            'colab.accounts.views.password_changed', name='password_change_done'),
    )
else:
    urlpatterns = patterns('',
        url(r'^login/?$', LoginView.as_view(), name='login'),
    )

urlpatterns += patterns('',
    url(r'^register/?$', 'colab.accounts.views.signup', name='signup'),

#FIXME Configure for XMPP
#    url(r'^change-password/$',
#        ChangeXMPPPasswordView.as_view(), name='change_password'),

    url(r'^(?P<username>[\w@+.-]+)/?$',
        UserProfileDetailView.as_view(), name='user_profile'),

    url(r'^(?P<username>[\w@+.-]+)/edit/?$',
        UserProfileUpdateView.as_view(), name='user_profile_update'),

    url(r'^(?P<username>[\w@+.-]+)/subscriptions/?$',
        ManageUserSubscriptionsView.as_view(), name='user_list_subscriptions'),
)
