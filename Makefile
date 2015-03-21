
VIRTUALENV_PATH = /tmp/colab-venv
PATH := $(VIRTUALENV_PATH)/bin:${PATH}

DJANGO_SETTINGS_MODULE = tests.settings
export DJANGO_SETTINGS_MODULE
COLAB_SETTINGS = tests/settings.yaml
export COLAB_SETTINGS

ifndef RELEASE
  RELEASE = 1
endif

all:
	echo $(RELEASE)

install:
	virtualenv $(VIRTUALENV_PATH)
	pip install .
	virtualenv --relocatable $(VIRTUALENV_PATH)

test_install: install_solr
	pip install flake8

install_solr:
	# Install java
	which apt-get && sudo apt-get install default-jre -y || echo # deb
	which yum && sudo yum install java -y || echo # rpm
	
	colab-admin build_solr_schema > /tmp/schema.xml
	SOLR_VERSION=4.10.3  SOLR_CONFS="/tmp/schema.xml" ci/install_solr.sh

travis_install: test_install
	psql -c "CREATE USER colab WITH PASSWORD 'colab' CREATEDB;" -U postgres

test:
	python setup.py test
	flake8 colab

coveralls:
	pip install coveralls
	coveralls

rpm:
	ci/build_rpm.sh

clean:
	$(RM) -r $(VIRTUALENV_PATH)
