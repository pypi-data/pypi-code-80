from gracie_dictionary_api import GracieBaseAPI


class autotuneIterationController(GracieBaseAPI):
    """Autotune Iteration Controller"""

    _controller_name = "autotuneIterationController"

    def list(self, **kwargs):
        """

        Args:
            autotuneRunId: (string): Id of existing autotune-run

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'autotuneRunId': {'name': 'autotuneRunId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneIteration/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def restore(self, **kwargs):
        """

        Args:
            id: (string): Id of existing autotune-iteration

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneIteration/restore'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def resume(self, **kwargs):
        """

        Args:
            firstIterationRerunsTesting: (boolean): true - in first resumed iteration run backup and test. false - make documents movement based on previous iteration result.
            firstIterationUpdatesSkills: (boolean): firstIterationUpdatesSkills
            id: (string): Id of existing autotune-iteration
            maxIterations: (integer): Max number of iterations to run.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'firstIterationRerunsTesting': {'name': 'firstIterationRerunsTesting', 'required': False, 'in': 'query'}, 'firstIterationUpdatesSkills': {'name': 'firstIterationUpdatesSkills', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': False, 'in': 'query'}, 'maxIterations': {'name': 'maxIterations', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneIteration/resume'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, **kwargs):
        """

        Args:
            id: (string): Id of existing autotune-iteration

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneIteration/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
