# install the package in the edxapp env
pip install -e ../eox-tenant

# test that the commands for eox-tenant are being listed
./manage.py lms help | grep eox

#
# cd ../eox-tenant
# make test-integration-tutor
make test-requirements
python -Wd -m pytest -p no:randomly --ds=lms.envs.test /openedx/eox-tenant/eox_tenant/test/tutor
