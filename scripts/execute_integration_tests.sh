#!/bin/bash

echo "Install test-requirements"
make test-requirements

echo "Run tests"
pytest -rPf ./eox_tenant/test/integration
