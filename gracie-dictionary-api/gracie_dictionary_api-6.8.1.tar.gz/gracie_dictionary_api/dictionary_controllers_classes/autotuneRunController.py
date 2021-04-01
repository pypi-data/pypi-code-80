from gracie_dictionary_api import GracieBaseAPI


class autotuneRunController(GracieBaseAPI):
    """Autotune Run Controller"""

    _controller_name = "autotuneRunController"

    def add(self, **kwargs):
        """

        Args:
            languageId: (string): Language id to retrieve parameters for, default is caller's language
            name: (string): Name of new autotune-run to add

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneRun/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, **kwargs):
        """

        Args:
            id: (string): Id of existing autotune-run to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneRun/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            orderAsc: (boolean): true = ascending (default); false = descending
            orderBy: (string): Sort results by order: NAME

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneRun/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, **kwargs):
        """

        Args:
            id: (string): Id of existing autotune-run

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneRun/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def run(self, **kwargs):
        """

        Args:
            firstIterationUpdatesSkills: (boolean): firstIterationUpdatesSkills
            id: (string): Id of existing autotune-run to run
            maxIterations: (integer): Max number of iterations to run.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'firstIterationUpdatesSkills': {'name': 'firstIterationUpdatesSkills', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': False, 'in': 'query'}, 'maxIterations': {'name': 'maxIterations', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneRun/run'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
