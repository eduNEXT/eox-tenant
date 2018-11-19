"""
Setup file for eox-tenant Django plugin.
"""
import os
import re
import pip
from distutils.core import setup


REQUIREMENTS_FILES = [
    "base",
]

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


def get_requirements(env="base"):
    """
    Retrieves the requirements for this plugin.
    """
    links = []
    requires = []
    if env not in REQUIREMENTS_FILES:
        return links, requires
    filename_reqs = "requirements/{}.txt".format(env)
    # new versions of pip requires a session
    requirements = pip.req.parse_requirements(
        filename_reqs,
        session=pip.download.PipSession()
    )
    for item in requirements:
        # we want to handle package names and also repo urls
        if getattr(item, "url", None):  # older pip has url
            links.append(str(item.url))
        if getattr(item, "link", None):  # newer pip has link
            links.append(str(item.link))
        if item.req:
            requires.append(str(item.req))
    return links, requires


links, requires = get_requirements()


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
    },
    install_requires=requires,
    dependency_links=links
)
