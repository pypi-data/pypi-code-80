import requests
from .plan import XPBoardsPlan
from .dataset import XPBoardsDataSet

class XPBoardsServices:
    __API_VERSION = 'v1'
    __BASE_URL = f'https://hom.web.xpboards.com.br/api/{__API_VERSION}'
    __DEFAULT_HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json' }


    def __init__(self, email, password):
        self.__token = self.__generate_token(email, password)

    def __handle_request_errors(self, message):
        raise Exception(message)

    def __handle_response(self, response):
        errors = response.get('errors', None)
        
        if errors:
            self.__handle_request_errors(message=f'Got the following errors from api service: {repr(errors)}')

        data = response.get('data', None)
        
        if data == None:
            self.__handle_request_errors(message=f'No "data" found in the response body')

        if not isinstance(data, list):
            code = data.get('code', None)

            if code == 'max_dataset_count':
                self.__handle_request_errors(message=f'Got the following message from api service: {data["message"]}') 

        return data

    def __generate_token(self, email, password):
        url = f'{self.__BASE_URL}/login'
        headers = self.__DEFAULT_HEADERS
        body = {
            'email': email,
            'password': password
        }

        response = requests.post(
            url=url,
            headers=headers,
            json=body
        )

        data = self.__handle_response(response.json())
        token = data.get('access_token', None)

        if token != None:
            return token['accessToken']
        else:
            raise Exception(f'Expecting token, instead got {repr(data)}')

    def get_token(self):
        return self.__token

    def __get_auth_headers(self):
        headers = self.__DEFAULT_HEADERS
        headers['Authorization'] = f'Bearer {self.__token}'

        return headers

    def get_plan(self):
        url = f'{self.__BASE_URL}/userdata'
        headers = self.__get_auth_headers()

        response = requests.get(
            url=url,
            headers=headers
        )

        return XPBoardsPlan(self.__handle_response(response.json()))

    def list_datasets(self):
        url = f'{self.__BASE_URL}/dataset'
        headers = self.__get_auth_headers()

        response = requests.get(
            url=url,
            headers=headers
        )

        return self.__handle_response(response.json())

    def list_dataset_items(self, dataset_id, raw=False):
        url = f'{self.__BASE_URL}/dataset/{dataset_id}'
        headers = self.__get_auth_headers()

        response = requests.get(
            url=url,
            headers=headers
        )

        data = self.__handle_response(response.json())

        if raw:
            return data
        else:
            return XPBoardsDataSet(data, convert_types=True)

    def create_dataset(self, data, name=None):

        if isinstance(data, XPBoardsDataSet):
            
            if name:
                data.name = name

            url = f'{self.__BASE_URL}/dataset'
            headers = self.__get_auth_headers()

            response = requests.post(
                url=url,
                headers=headers,
                json=data.to_api()
            )

            data = self.__handle_response(response.json())

            return data

        else:
            raise Exception('The "data" param is not a XPBoardsDataSet instance')

    def update_dataset(self, dataset_id, data):
        """
            Replaces specified dataset with sent data
        """

        if isinstance(data, XPBoardsDataSet):
            
            url = f'{self.__BASE_URL}/dataset/{dataset_id}'
            headers = self.__get_auth_headers()

            response = requests.put(
                url=url,
                headers=headers,
                json=data.to_api()
            )

            data = self.__handle_response(response.json())

            return data

        else:
            raise Exception('The "data" param is not a XPBoardsDataSet instance')


    def clear_dataset(self, dataset_id, data):
        """
            Clear all dataset items
        """

        if isinstance(data, XPBoardsDataSet):
            
            url = f'{self.__BASE_URL}/dataset/{dataset_id}'
            headers = self.__get_auth_headers()

            cleared_data = data.to_api()
            cleared_data['rows'] = []

            response = requests.put(
                url=url,
                headers=headers,
                json=cleared_data
            )

            data = self.__handle_response(response.json())

            return data

        else:
            raise Exception('The "data" param is not a XPBoardsDataSet instance')