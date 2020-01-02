"""
Utils to run tests
"""
from django.db import models

try:
    from django_fake_model import models as fake

    class CertificatesFakeModel(fake.FakeModel):
        """
        Fake Model for certificates.
        """

        course_id = models.CharField(max_length=255, blank=True, default=None)
        status = models.CharField(max_length=32, default='unavailable')

except ImportError:
    CertificatesFakeModel = object


class TestCertificateStatuses(object):
    """
    Test Enum for certificate statuses
    """
    generating = 'generating'
    audit_passing = 'audit_passing'
    audit_notpassing = 'audit_notpassing'


class test_theming_helpers(object):
    """
    Test class for theming helpers
    """
    def get_current_request(self):
        """
        Test method
        """
        return object


class TestSiteConfigurationModels(object):
    """
    Test class for SiteConfigurationModels.
    """

    SiteConfiguration = object


class TestCertificatesModels(object):
    """
    Test class for SiteConfigurationModels.
    """

    GeneratedCertificate = CertificatesFakeModel
    CertificateStatuses = TestCertificateStatuses
