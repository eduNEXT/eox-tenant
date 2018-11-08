"""
Setup file for eox-tenant Django plugin.
"""
import os
import re
from distutils.core import setup


def get_version():
    """
    Retrives the version string from __init__.py.
    """
    file_path = os.path.join('eox_tenant', '__init__.py')
    initfile_lines = open(file_path, 'rt').readlines()
    version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        match_string = re.search(version_regex, line, re.M)
        if match_string:
            return match_string.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (file_path,))

setup(
    name='eox-tenant',
    version=get_version(),
    description='Edunext Open edx extensions tenant.',
    author='eduNEXT',
    author_email='contact@edunext.co',
    packages=['eox_tenant'],
    zip_safe=False,
    entry_points={
        "lms.djangoapp": [
            "eox_tenant = eox_tenant.apps:EdunextOpenedxExtensionsTenantConfig"
        ],
    }
)
