""" Backend test abstraction. """
from eox_tenant.test_utils import TestCertificatesModels


def get_certificates_models():
    """ Backend to get certificates models. """
    return TestCertificatesModels()
