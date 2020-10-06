""" backend """
try:
    from branding import api as branding_api  # pylint: disable=import-error
except ImportError:
    branding_api = object


def get_branding_api():
    """ backend function """
    return branding_api
