User Documentation
==================

Getting Started
---------------

Dependencies
++++++++++++
.. TODO

Install
+++++++
.. TODO

Plugins
-------
.. TODO

Trac
++++


Since Trac already installed:

- Easily, you can install it as follows:

.. code-block:: sh

  $ pip install trac

To enable Trac plugin must first configure the trac database in /etc/colab/settings.yml:

1. vim /etc/colab/settings.yaml

.. code-block:: yaml

  DATABASES:
    default:
      ENGINE: django.db.backends.postgresql_psycopg2
      HOST: localhost
      NAME: colab
      USER: colab
      PASSWORD: colab
    trac:
    ENGINE: django.db.backends.postgresql_psycopg2
    HOST: localhost
    NAME: trac
    USER: colab
    PASSWORD: colab

- Yet this file uncomment in PROXIED_APPS the Trac:

.. code-block:: yaml

  PROXIED_APPS:
    # gitlab:
    # upstream: 'http://localhost:8090/gitlab/'
    # private_token: ''
    trac:
      upstream: 'http://localhost:5000/trac/'

- Create the database in postgresql with user

.. code-block:: sh

  $ sudo -u postgres psql
  $ create database trac owner colab;

- Now, generate the migrations:

.. code-block:: sh

  # Since you are in the folder colab
  $ workon colab
  $ colab-admin makemigrations
  $ colab-admin migrate trac

- Finally, just import the Trac data (may take a few minutes):

.. code-block:: sh

  # Since you are in the folder colab
  $ colab-admin import_proxy_data

Settings
--------

Blog Planet
+++++++++++
.. TODO

Paste
+++++
.. TODO

XMPP
++++
.. TODO

SVN
+++
.. TODO

Social Networks
++++
.. attribute:: SOCIAL_NETWORK_ENABLED

   :default: False

   When this variable is True, the social networks fields, like Facebook and 
   Twitter, are added in user profile. By default, this fields are disabled.

Auth
++++
.. attribute:: BROWSERID_ENABLED

   :default: False

   When this variable is True, Colab use BrowserID authentication. By default,
   django authentication system is used.

.. attribute:: BROWSERID_AUDIENCES

   :default: No default

   List of audiences that your site accepts. An audience is the protocol,
   domain name, and (optionally) port that users access your site from. This
   list is used to determine the audience a user is part of (how they are
   accessing your site), which is used during verification to ensure that the
   assertion given to you by the user was intended for your site.

   Without this, other sites that the user has authenticated with via Persona
   could use their assertions to impersonate the user on your site.

   Note that this does not have to be a publicly accessible URL, so local URLs
   like ``http://localhost:8000`` or ``http://127.0.0.1`` are acceptable as
   long as they match what you are using to access your site.

Customization
-------------
Home Page
+++++++++
.. TODO

Menu
++++
.. TODO

Templates
+++++++++
.. TODO
