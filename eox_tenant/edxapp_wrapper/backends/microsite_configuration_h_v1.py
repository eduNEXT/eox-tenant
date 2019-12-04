""" Backend abstraction. """

from eox_tenant.backends.base import AbstractBaseMicrositeBackend


def get_base_microsite_backend():
    """ Backend to get BaseMicrositeBackend. """
    try:
        from microsite_configuration.backends.base import BaseMicrositeBackend as InterfaceConnectionBackend
    except ImportError:
        InterfaceConnectionBackend = AbstractBaseMicrositeBackend
    return InterfaceConnectionBackend
