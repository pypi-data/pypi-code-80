from typing import Any, Dict, List, Optional, Union

from sym.sdk._internal.utils import wrap_with_typed_error
from sym.sdk.errors import SymSystemError
from sym.sdk.resource import SRN
from sym.sdk.user import User

from .integration_handler import IntegrationHandler, IntegrationType, SymHandlerErrors

OrganizationHandle = Union[SRN, str]


class SymHandler(IntegrationHandler):
    integration_type = IntegrationType.SYM

    @wrap_with_typed_error(SymSystemError, SymHandlerErrors)
    def get_flows(
        self,
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
        return self.get_handler(IntegrationType.SYM).get_flows(
            user_id, org_handle, environment_name, flow_name
        )

    @wrap_with_typed_error(SymSystemError, SymHandlerErrors)
    def map_users(
        self, integration_category: str, integration_srn: Optional[str], user_handles: List[str]
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
        return self.get_handler(IntegrationType.SYM).map_users(
            integration_category, integration_srn, user_handles
        )

    def execute(self, method_name: str, parameter_lookups: Optional[Dict[str, Any]] = None):
        raise NotImplementedError()
