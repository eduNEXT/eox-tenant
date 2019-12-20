"""
Backend Certificates file, here should be all the necessary methods,
classes and modules from lms.djangoapss.certificates.
"""
from django.conf import settings

from lms.djangoapps.certificates import models  # pylint: disable=import-error

from eox_tenant.test_utils import TestCertificatesModels


def get_certificates_models():
    """
    Backend function.

    Return <lms.djangoapps.certificates.models>.
    """
    return models if getattr(settings, 'USE_EOX_TENANT', False) else TestCertificatesModels()
