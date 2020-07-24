"""
Backend Certificates file, here should be all the necessary methods,
classes and modules from lms.djangoapss.certificates.
"""
from django.conf import settings
from lms.djangoapps.certificates import models  # pylint: disable=import-error

from eox_tenant.constants import LMS_ENVIRONMENT
from eox_tenant.test_utils import TestCertificatesModels


def get_certificates_models():
    """
    Backend function.

    Return <lms.djangoapps.certificates.models>.
    """

    # The following logic is necessary, because we don't want to use the certificate models as backend,
    # when we are running the platform test, in order to avoid django migration errors.
    # USE_EOX_TENANT is set to False by default, which allows to run the platform tests with its normal behavior,
    # and the plugin tests are run with a different backend.
    return models if getattr(settings, 'USE_EOX_TENANT', False) and LMS_ENVIRONMENT else TestCertificatesModels()
