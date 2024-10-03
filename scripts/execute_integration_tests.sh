#!/bin/bash

echo "Install test-requirements"
make install-dev-dependencies

echo "Run tests"
pytest -rPf ./eox_tenant/test/integration
