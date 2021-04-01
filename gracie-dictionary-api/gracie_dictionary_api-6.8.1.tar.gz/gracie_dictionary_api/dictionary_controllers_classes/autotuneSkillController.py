from gracie_dictionary_api import GracieBaseAPI


class autotuneSkillController(GracieBaseAPI):
    """Autotune Skill Controller"""

    _controller_name = "autotuneSkillController"

    def addAllSkills(self, **kwargs):
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
        api = '/autotuneSkill/addAllSkills'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def addSkill(self, skillId, **kwargs):
        """

        Args:
            autotuneRunId: (string): Id of existing autotune-run
            skillId: (string): Id of skill

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'autotuneRunId': {'name': 'autotuneRunId', 'required': False, 'in': 'query'}, 'skillId': {'name': 'skillId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneSkill/addSkill'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def addSkillset(self, skillsetId, **kwargs):
        """

        Args:
            autotuneRunId: (string): Id of existing autotune-run
            skillsetId: (string): Id of skillset

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'autotuneRunId': {'name': 'autotuneRunId', 'required': False, 'in': 'query'}, 'skillsetId': {'name': 'skillsetId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneSkill/addSkillset'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, skillId, **kwargs):
        """

        Args:
            autotuneRunId: (string): Id of existing autotune-run to delete
            skillId: (string): Id of skill

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'autotuneRunId': {'name': 'autotuneRunId', 'required': False, 'in': 'query'}, 'skillId': {'name': 'skillId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneSkill/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            autotuneRunId: (string): Id of existing autotune-run
            orderAsc: (boolean): true = ascending (default); false = descending
            orderBy: (string): Sort results by order: NAME

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'autotuneRunId': {'name': 'autotuneRunId', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneSkill/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
