from climadjust.DTOs.experiment import InsertExperimentDTO
from climadjust.DTOs.pagination import PaginationDTO
from climadjust import urls


class ExperimentMixin:

    def get_experiments(self,
                        page=None,
                        size=None,
                        sort_field=None,
                        sort_direction=None):
        """
        Get a paginated list of experiments

        :param page: (optional) int page number
        :param size: (optional) int number of results per page
        :param sort_field: (optional) str field to sort results by (either "id" or "name")
        :param sort_direction: (optional) str sort direction (either "ASC" or "DESC")

        :return: list of experiments
        """
        pagination = PaginationDTO(page, size, sort_field, sort_direction).get_dict()
        params = {**pagination}
        experiments = self.request_get(urls.EXPERIMENTS, params)
        return experiments

    def get_experiments_by_id(self,
                              exp_id):
        """
        Get a specific experiment. In case the experiment is being uploaded the uploaded state will also
        appear.

        :param exp_id: int id of the experiment

        :return: the selected experiment information
        """
        return self.request_get(urls.EXPERIMENTS + str(exp_id))

    def post_experiment(self,
                        name,
                        temporalResolution,
                        temporalResolutionAggFunction,
                        variables,
                        scenarios,
                        models,
                        baconfiguration,
                        spatialResolution,
                        spatialResolutionAggFunction,
                        datasetProjection,
                        datasetReference,
                        spatialCoverage,
                        outputFormat,
                        validation,
                        mask):
        """
        :param name: str experiment name
        :param temporalResolution: str temporal resolution for the experiment (only "DAILY")
        :param variables: list list of variables to perform the bias adjustment on
        :param scenarios: list list of dictionaries, each dictionary contains the scenario name as well as the startDate
                          and the endDate
        :param models: list list of models / members to use
        :param baconfiguration: list list of bias adjustment configurations for each variable
                                (variable, method, and parameters)
        :param spatialResolution: str spatial resolution for the experiment ("NATIVE")
        :param datasetProjection: dict dictionary with the IDs of the projections datasets that will be used for the
                                  experiment
        :param datasetReference: dict dictionary with the IDs of the reference datasets that will be used for the
                                  experiment
        :param spatialCoverage: shapely.geometry.Polygon() Polygon with the spatial coverage over which to execute the
                                experiment
        :param outputFormat: str output format (for example "NETCDF", "GRIB", ...)
        :param validation: str validation activity to perform (for example "NONE")
        :param mask: str a string explaining if land-mask needs to be used (for example "none")

        :return: id of the uploaded experiment
        """
        experiment = InsertExperimentDTO(name, temporalResolution, temporalResolutionAggFunction,
                                         variables,
                                         scenarios, models, baconfiguration,
                                         spatialResolution, spatialResolutionAggFunction,
                                         datasetProjection,
                                         datasetReference, spatialCoverage,
                                         outputFormat, validation, mask).get_dict()
        return self.request_post(urls.EXPERIMENTS, params=experiment)

    def delete_experiment(self, exp_id):
        """
        Delete existing experiment

        :param exp_id: int id of the experiment to be deleted

        :return:
        """
        return self.request_delete(urls.DS_OBSERVATIONS, exp_id)

    def download_experiment(self, exp_id, download_path=None):
        """
        Download finished experiment
        :param exp_id: int id of the experiment to be downloaded
        :param download_path: str optional where to store the results
        :return: downloaded path
        """
        return self.request_download(urls.EXPERIMENTS + str(exp_id) + "/result", download_path=download_path)

