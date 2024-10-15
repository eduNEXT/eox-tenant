###############################################
#
# Edunext Open edx extensions tenant commands.
#
###############################################
# Define PIP_COMPILE_OPTS=-v to get more information during make upgrade.
PIP_COMPILE = pip-compile --rebuild --upgrade $(PIP_COMPILE_OPTS)

.DEFAULT_GOAL := help

ifdef TOXENV
TOX := tox -- #to isolate each tox environment if TOXENV is defined
endif

help: ## display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

clean: ## delete most git-ignored files
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

requirements: ## install environment requirements
	pip install -r requirements/base.txt

install-dev-dependencies: ## install tox
	pip install -r requirements/tox.txt

upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
upgrade: ## update the requirements/*.txt files with the latest packages satisfying requirements/*.in
	pip install -qr requirements/pip-tools.txt
	# Make sure to compile files after any other files they include!
	$(PIP_COMPILE) -o requirements/pip-tools.txt requirements/pip-tools.in
	$(PIP_COMPILE) -o requirements/base.txt requirements/base.in
	$(PIP_COMPILE) -o requirements/test.txt requirements/test.in
	$(PIP_COMPILE) -o requirements/tox.txt requirements/tox.in

	grep -e "^django==" requirements/test.txt > requirements/django42.txt
	sed '/^[dD]jango==/d;' requirements/test.txt > requirements/test.tmp
	mv requirements/test.tmp requirements/test.txt

run-integration-tests:
	pip install -r requirements/test.txt
	pytest -rPf ./eox_tenant/test/integration

quality: clean ## check coding style with pycodestyle and pylint
	$(TOX) pycodestyle ./eox_tenant
	$(TOX) pylint ./eox_tenant --rcfile=./setup.cfg
	$(TOX) isort --check-only --diff ./eox_tenant

test-python: clean ## Run test suite.
	$(TOX) pip install -r requirements/test.txt --exists-action w
	$(TOX) coverage run --source="." -m pytest ./eox_tenant --ignore-glob='**/integration/*'
	$(TOX) coverage report -m --fail-under=71

run-tests: test-python quality
