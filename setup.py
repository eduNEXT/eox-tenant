"""
Setup file for eox-tenant Django plugin.
"""
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst', 'r') as fh:
    README = fh.read()

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
    long_description=README,
    long_description_content_type='text/x-rst',
    packages=['eox_tenant'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    license='AGPL',
    zip_safe=False,
    install_requires=[
        "django-mysql>=3.6; python_version=='3.5'",
    ],
    entry_points={
        "lms.djangoapp": [
            "eox_tenant = eox_tenant.apps:EdunextOpenedxExtensionsTenantConfig"
        ],
        "cms.djangoapp": [
            "eox_tenant = eox_tenant.apps:EdunextOpenedxExtensionsTenantConfig"
        ],
    }
)
