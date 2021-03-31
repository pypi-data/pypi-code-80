"""Functionality serving to inspect the Client's Sym Deployment.  These are primarily intended for
clients themselves writing Templates and Integrations"""

from typing import Dict, List, Optional, Union

from sym.sdk._internal.integrations.sym_handler import SymHandler, SymHandlerErrors
from sym.sdk._internal.utils import wrap_with_typed_error
from sym.sdk.errors import SymSystemError
from sym.sdk.resource import SRN
from sym.sdk.user import User

OrganizationHandle = Union[SRN, str]


@wrap_with_typed_error(SymSystemError, SymHandlerErrors)
def get_flows(
    user_id: str,
    org_handle: Optional[OrganizationHandle],
    environment_name: Optional[str] = None,
    flow_name: Optional[str] = None,
    show_all_environments: bool = False,
) -> Dict[str, dict]:
    """Accessor for the collection of flows visible to the given user/suborganization.

    Args:
        user_id: The user on who's behalf flows are being sought.
        org_handle: Optional handle for a suborganization of the organization hosting this deployment.  None
                will be interpreted to mean the deployed organization.  An exception will be thrown
                if this does not match the hosting organization structure and privileges.
        environment_name: If set, filters out flows to the specified environment.
                            Otherwise implicitly filters to the client's main ("prod") environment
        flow_name: Selects the given flow name, error if not found.
        show_all_environments: Ignore environments and show all specified flows across all environments

    Returns:
        Dict[str, dict]: Flow details keyed by Flow slugs
    """
    return SymHandler.get_handler().get_flows(user_id, org_handle, environment_name, flow_name)


@wrap_with_typed_error(SymSystemError, SymHandlerErrors)
def map_users(
    integration_category: str, integration_srn: Optional[str], user_handles: List[str]
) -> Dict[str, User]:
    """Lookup function to map a collection of Integration User Handles to Sym Users.

    Args:
        integration_category: Type of integration.  Sufficient information if the deployment only hosts one
        integration of type integration_category.
        integration_srn: SRN of the specified integration if multiple instances of that category are deployed.
        user_handles: IDs for a collection of users as provided by the given integration.

    Returns:
        Dict[str, User]: Sym User Details for each mapped user found within the current Sym Database.
    """
    return SymHandler.get_handler().map_users(integration_category, integration_srn, user_handles)


def debug(message: str, *, user: Optional[User] = None):
    """Send a debug message.

    This method takes a message and sends it to a :class:`~sym.sdk.user.User`
    via an appropriate channel (e.g. Slack).

    It can be helpful to debug the output of various Integrations.

    Args:
        user: The :class:`~sym.sdk.user.User` to send the message to. Defaults to the Implementer of this Flow.
    """
