# install the package in the edxapp env
pip install -e ../eox-tenant

# test that the commands for eox-tenant are being listed
./manage.py lms help | grep eox

# running the tests using the tutor settings
make test-requirements
pytest -s --ds=lms.envs.tutor.test /openedx/eox-tenant/eox_tenant/test/tutor
