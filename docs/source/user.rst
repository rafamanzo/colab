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


Dado que o Trac ja está instalado :

- Vocẽ pode instalá-lo facilmente da seguinte maneira:

.. code-block:: sh

  $ pip install trac

Para ativar o plugin do Trac deve-se primeiramente configurar o banco de dados
do trac em:

1. vim /etc/colab/settings.yml


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

2. Ainda no mesmo arquivo descomentar o Trac em PROXIED_APPS

.. code-block:: yaml

  PROXIED_APPS:
    # gitlab:
    # upstream: 'http://localhost:8090/gitlab/'
    # private_token: ''
    trac:
      upstream: 'http://localhost:5000/trac/'

3. Criar o banco de dados no postgresql com usuário colab

.. code-block:: sh

  $ sudo -u postgres psql
  $ create database trac owner colab;

4. Agora você deve gerar as migrações do trac

.. code-block:: sh

  # Dado que você está na pasta do colab
  $ workon colab
  $ colab-admin makemigrations trac
  $ colab-admin migrate

5. Por fim basta importar os dados do trac ( pode levar algumtempo ).

.. code-block:: sh

  # Dado que você está na pasta do colab
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
