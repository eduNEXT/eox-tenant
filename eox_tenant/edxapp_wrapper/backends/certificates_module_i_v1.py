"""
Backend Certificates file, here should be all the necessary methods,
classes and modules from lms.djangoapss.certificates.
"""
from lms.djangoapps.certificates import models  # pylint: disable=import-error


def get_certificates_models():
    """
    Backend function.

    Return <lms.djangoapps.certificates.models>.
    """
    return models
