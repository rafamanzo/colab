
WHEEL_DIR = .colab-wheel/

DJANGO_SETTINGS_MODULE = tests.settings
COLAB_SETTINGS = tests/settings.yaml
SOLR_VERSION = 4.10.3

export DJANGO_SETTINGS_MODULE
export COLAB_SETTINGS
export SOLR_VERSION

all:
	pip install wheel
	pip wheel --wheel-dir=$(WHEEL_DIR) .

install:
	pip install --use-wheel --no-index --find-links=$(WHEEL_DIR) .

install_solr: install
	# Install java
	which apt-get && sudo apt-get install default-jre -y || echo # deb
	which yum && sudo yum install java -y || echo # rpm
	
	colab-admin build_solr_schema > /tmp/schema.xml
	SOLR_CONFS="/tmp/schema.xml" ci/install_solr.sh

run_solr:
	cd solr-$(SOLR_VERSION)/example/; java -jar start.jar

test_install: install_solr
	pip install flake8

ci_install: test_install
	dropdb test_colab --if-exists -U postgres
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
	$(RM) -r $(WHEEL_DIR)
