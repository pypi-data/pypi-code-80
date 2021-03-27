
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.actions_api import ActionsApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from swx_sdk.api.actions_api import ActionsApi
from swx_sdk.api.collections_api import CollectionsApi
from swx_sdk.api.events_api import EventsApi
from swx_sdk.api.items_api import ItemsApi
from swx_sdk.api.model_versions_api import ModelVersionsApi
from swx_sdk.api.models_api import ModelsApi
from swx_sdk.api.properties_api import PropertiesApi
from swx_sdk.api.things_api import ThingsApi
