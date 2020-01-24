"""
This files should contain all the context managers for the tenant_wise module.
"""
import logging

from contextlib import contextmanager

logger = logging.getLogger(__name__)


@contextmanager
def proxy_regression(module, model, regressive_model, current_model):
    """
    Allow to execute an operation with a different model to a given module.
    """
    try:
        previous_model = getattr(module, model)
        setattr(module, model, regressive_model)
        current_model.__class__ = regressive_model
        yield current_model
    except AttributeError as error:
        logger.error('The error %s has been generated for the module %s and model %s', error, module, model)
        raise

    current_model.__class__ = previous_model
    setattr(module, model, previous_model)
