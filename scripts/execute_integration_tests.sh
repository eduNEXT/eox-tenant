#!/bin/bash

echo "Install test-requirements"
make test-requirements

echo "Run tests"
pytest -s --ds=lms.envs.tutor.test /openedx/eox-tenant/eox_tenant/test/integration
