#!/bin/bash

# install the package in the edxapp env
pip install -e ../eox-tenant

# test that the commands for eox-tenant are being listed at the lms
is_command_installed=$(./manage.py lms help | grep eox | wc -l)
if [ $is_command_installed == 0 ] ; then
  echo 'package was not installed correctly'
  exit -1;
fi

# run migrations
./manage.py lms migrate eox_tenant

# running the tests using the tutor settings
make test-requirements
pytest -s --ds=lms.envs.tutor.test /openedx/eox-tenant/eox_tenant/test/tutor
