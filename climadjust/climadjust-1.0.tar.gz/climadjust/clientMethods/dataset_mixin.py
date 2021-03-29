from climadjust.DTOs.dataset import DatasetDTO, InsertDatasetDTO
from climadjust.DTOs.pagination import PaginationDTO
from climadjust import urls


class DatasetMixin:
    """ Observations """
    def get_observation_datasets(self, name=None, page=None,
                                 size=None, sort_field=None, sort_direction=None):
        """
        Get a paginated list of observation datasets
        :param name: (optional) str dataset name
        :param page: (optional) int page number
        :param size: (optional) int number of results per page
        :param sort_field: (optional) str field to sort results by (either "type" or "name")
        :param sort_direction: (optional) str sort direction (either "ASC" or "DESC")

        :return: list of observation datasets

        """
        ds = DatasetDTO(name).get_dict()
        pagination = PaginationDTO(page, size, sort_field, sort_direction).get_dict()
        params = {**ds, **pagination}
        datasets = self.request_get(urls.DS_OBSERVATIONS, params)
        return datasets

    def get_observation_dataset_by_id(self, ds_id: int):
        """
        Get an observation dataset. In case the dataset is being uploaded the uploaded state will also
        appear.
        :param ds_id: int id of the observation dataset
        :return: the selected dataset information
        """
        return self.request_get(urls.DS_OBSERVATIONS + str(ds_id))

    def post_observation_dataset(self, file, name, ds_format, variables):
        """
        Uploads an observation dataset
        :param file: str path to the dataset to be uploaded
        :param name: str dataset name
        :param ds_format: str dataset format (either "NETCDF" or "VALUE_TEXT")
        :param variables:  list[dict] list of variables. Variable format should be:
            {"standardName": "tas", "customName": "tas", "standardUnit": "Celsius", "customUnit": "Celsius"}
        :return: id of the uploaded dataset
        """
        ds = InsertDatasetDTO(name, ds_format, variables).get_dict()
        return self.request_upload(urls.DS_OBSERVATIONS, file=file, params=ds)

    def get_validation(self, ds_id):
        """
        Gets validation warning/errors and GEOJSON info from an uploaded dataset
        :param ds_id: int id of the uploaded dataset
        :return: dict of validation warning/errors and a GEOJSON with info from the dataset
        """
        return self.request_get(urls.DS_OBSERVATIONS + str(ds_id) + "/validation")

    def delete_observation_dataset(self, id: int):
        """
        Delete existing observation dataset
        :param id: int id of the dataset
        :return:
        """
        return self.request_delete(urls.DS_OBSERVATIONS, id)

    """ Projections """
    def get_projection_datasets(self, name=None, page=None, size=None,
                                sort_field=None, sort_direction=None):
        """
        Get a paginated list of projection datasets
        :param name: (optional) str dataset name
        :param page: (optional) int page number
        :param size: (optional) int number of results per page
        :param sort_field: (optional) str field to sort results by (either "type" or "name")
        :param sort_direction: (optional) str sort direction (either "ASC" or "DESC")
        :return: list of projection datasets
        """
        ds = DatasetDTO(name).get_dict()
        pagination = PaginationDTO(page, size, sort_field, sort_direction).get_dict()
        params = {**ds, **pagination}
        datasets = self.request_get(urls.DS_PROJECTIONS, params)
        return datasets

    def get_projection_datasets_by_id(self, id: int):
        """
        Get a projection dataset info
        :param id: int id of the projection dataset
        :return: dict with dataset info
        """
        return self.request_get(urls.DS_PROJECTIONS + str(id))

    def get_projection_models_for_dataset_scenarios_variables(self,
                                                              dataset_name,
                                                              scenarios,
                                                              variables):
        return self.request_get(urls.DS_PROJECTIONS +
                                'search?project=' +
                                dataset_name +
                                '&scenarios=' +
                                scenarios +
                                '&variables=' +
                                variables)
