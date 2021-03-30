from typing import Any, AnyStr, Dict, List, Optional
from urllib.parse import urljoin

import requests

from ruleau.execute import ExecutionResult


class ApiAdapter:

    base_url: AnyStr
    api_key: Optional[AnyStr]
    result: ExecutionResult
    payload: Dict[AnyStr, Any]

    def __init__(
        self,
        base_url: AnyStr,
        payload: Dict[AnyStr, Any],
        result: ExecutionResult,
        api_key: Optional[AnyStr] = None,
    ):
        """
        :param base_url: Base URL of the ruleau API
        :param payload: Payload the rules executed upon
        :param result: Execution result of the ruleset
        :param api_key: (Optional) API key to authenticate with the API
        """
        self.base_url = base_url
        self.api_key = api_key
        self.result = result
        self.payload = payload

    @staticmethod
    def flatten(
        results: dict, output: list = [], order: int = 0
    ) -> List[Dict[AnyStr, Any]]:
        """Flatten the processed execution result
        :param results: Processed results of each rule
        :param output: Output to append flattened results to
        :param order: Execution Order of the rule
        :return:
        """
        if len(results["dependencies"]):
            # If there are dependencies in the list, recurse, flatten, order
            for dependency in results["dependencies"]:
                ApiAdapter.flatten(dependency, output, order + 1)
            results["dependencies"] = [x["name"] for x in results["dependencies"]]
        # Add the order to store in the API
        results["order"] = order
        # Append processed output to the final output
        output.append(results)
        return output

    @staticmethod
    def process(result: ExecutionResult) -> Dict[AnyStr, Any]:
        """Process the execution result into a dictionary
        :param result: Final processed result of the execution
        :return: A dictionary of all the data related to a case
        """
        return {
            "id": result.executed_rule.id,
            "name": result.executed_rule.name
            if result.executed_rule.name is not None
            else result.executed_rule.__name__,
            "description": result.executed_rule.__doc__,
            "dependencies": [
                ApiAdapter.process(result.dependant_results.results[rule.__name__])
                for rule in result.executed_rule.depends_on
            ],
            "result": {"result": result.value, "payload": result.payload.accessed},
        }

    def send(self) -> bool:
        """Send the case payload to the the API
        :return: boolean
        """
        rules = ApiAdapter.flatten(ApiAdapter.process(self.result), [])
        request_payload = {"payload": self.payload, "rules": rules}
        # Post the case results to the API
        response = requests.post(
            urljoin(self.base_url, "/api/v1/cases"), json=request_payload
        )
        return response.status_code == 201
