""" backend """
try:
    from branding import api as branding_api
except ImportError:
    branding_api = object


def get_branding_api():
    """ backend function """
    return branding_api
