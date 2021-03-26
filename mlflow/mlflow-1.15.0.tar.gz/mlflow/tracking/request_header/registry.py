import entrypoints
import warnings
import logging

from mlflow.tracking.request_header.databricks_request_header_provider import (
    DatabricksRequestHeaderProvider,
)

_logger = logging.getLogger(__name__)


class RequestHeaderProviderRegistry(object):
    def __init__(self):
        self._registry = []

    def register(self, request_header_provider):
        self._registry.append(request_header_provider())

    def register_entrypoints(self):
        """Register tracking stores provided by other packages"""
        for entrypoint in entrypoints.get_group_all("mlflow.request_header_provider"):
            try:
                self.register(entrypoint.load())
            except (AttributeError, ImportError) as exc:
                warnings.warn(
                    'Failure attempting to register request header provider "{}": {}'.format(
                        entrypoint.name, str(exc)
                    ),
                    stacklevel=2,
                )

    def __iter__(self):
        return iter(self._registry)


_request_header_provider_registry = RequestHeaderProviderRegistry()
_request_header_provider_registry.register(DatabricksRequestHeaderProvider)

_request_header_provider_registry.register_entrypoints()


def resolve_request_headers(request_headers=None):
    """Generate a set of request headers from registered providers. Request headers are resolved in
    the order that providers are registered. Argument headers are applied last.

    This function iterates through all request header providers in the registry. Additional context
    providers can be registered as described in
    :py:class:`mlflow.tracking.request_header.RequestHeaderProvider`.

    :param tags: A dictionary of request headers to override. If specified, headers passed in this
        argument will override those inferred from the context.
    :return: A dicitonary of resolved headers.
    """

    all_request_headers = {}
    for provider in _request_header_provider_registry:
        try:
            if provider.in_context():
                all_request_headers.update(provider.request_headers())
        except Exception as e:
            _logger.warning("Encountered unexpected error during resolving request headers: %s", e)

    if request_headers is not None:
        all_request_headers.update(request_headers)

    return all_request_headers
