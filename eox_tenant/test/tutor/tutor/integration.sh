#!/bin/bash

# Install the package in the edxapp env
echo "Install package"
pip install -e ../eox-tenant

# Install test requirements from openedx
echo "Install test-requirements"
make test-requirements

# Running the tests using the tutor settings
echo "Run tests"
pytest -s --ds=lms.envs.tutor.test /openedx/eox-tenant/eox_tenant/test/tutor
