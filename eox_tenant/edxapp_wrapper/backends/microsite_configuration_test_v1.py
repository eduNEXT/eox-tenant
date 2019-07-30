""" Backend abstraction. """

from eox_tenant.backends.base import AbstractBaseMicrositeBackend


def get_base_microsite_backend():
    """ Backend to get BaseMicrositeBackend. """
    try:
        from microsite_configuration.backends.base import BaseMicrositeBackend as InterfaceConnectionBackend
    except ImportError:
        InterfaceConnectionBackend = AbstractBaseMicrositeBackend
    return InterfaceConnectionBackend


def get_base_microsite_template_backend():
    """ Backend to get BaseMicrositeTemplateBackend. """
    try:
        from microsite_configuration.backends.base import BaseMicrositeTemplateBackend
    except ImportError:
        BaseMicrositeTemplateBackend = object
    return BaseMicrositeTemplateBackend


def get_microsite():
    """ Backend to get microsite. """
    try:
        from microsite_configuration import microsite  # pylint: disable=import-error
    except ImportError:
        microsite = object
    return microsite


def get_microsite_get_value(*args, **kwargs):
    """ Backend to get get_value. """
    from microsite_configuration.microsite import get_value  # pylint: disable=import-error
    return get_value(*args, **kwargs)


def get_is_request_in_microsite():
    """ Backend to get is_request_in_microsite. """
    from microsite_configuration.microsite import is_request_in_microsite  # pylint: disable=import-error
    return is_request_in_microsite
