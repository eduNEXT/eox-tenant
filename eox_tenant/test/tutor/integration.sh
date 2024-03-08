#!/bin/bash

# install the package in the edxapp env
echo "Install package"
pip install -e ../eox-tenant

# test that the commands for eox-tenant are being listed at the lms
echo "Tests django commands"
is_command_installed=$(./manage.py lms help | grep eox | wc -l)
if [ $is_command_installed == 0 ] ; then
  echo 'package was not installed correctly'
  exit -1;
fi

# run migrations
echo "Run migrations"
./manage.py lms migrate eox_tenant

# install pytest
echo "Install test-requirements"
make test-requirements

# running the tests using the tutor settings
echo "Install test-requirements"
pytest -s --ds=lms.envs.tutor.test /openedx/eox-tenant/eox_tenant/test/tutor
