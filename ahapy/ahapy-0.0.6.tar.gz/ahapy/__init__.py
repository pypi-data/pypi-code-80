import requests
import re


class BaseAPI(object):
    def __init__(self, sub_domain, api_key):
        self.sub_domain = sub_domain 
        self.api_key = api_key

        self.url = 'https://{}.aha.io/api'.format(self.sub_domain)

        self.session = requests.Session()
        self.session.headers.update({'Authorization': 'Bearer ' + api_key})



class AhaV1(BaseAPI):
    def __init__(self, sub_domain, api_key):
        self.sub_domain = sub_domain 
        self.api_key = api_key
        self.version = '/v1/'
        self.page = 1
        self.total_pages = 0
        self.count = 0
        self.endpoint = ''

        super(AhaV1, self).__init__(sub_domain, api_key)


    def _count(self, endpoint, **options):
        url = self.url + self.version + endpoint
        response = self.session.get(url, params=options)
        r = response.json()
        self.count = r['pagination']['total_records']
        return self.count
    

    def _parse_endpoint_arg(self, endpoint_arg):
        s = re.split('/', endpoint_arg)
        if re.match('[a-z]', s[-1]):
            return s[-1]
        else:
            return s[-2]


    def _is_paginated(self, json_response):
        if 'pagination' in json_response.keys():
            return True
        else:
            return False


    def query(self, endpoint, **options):
        """
        Query for Aha.io V1 endpoint
        """
        self.endpoint = self._parse_endpoint_arg(endpoint)

        while True:
            url = self.url + self.version + endpoint
            if self.page <= self.total_pages:
                url = url + '?page=' + str(self.page)
                response = self.session.get(url, params=options)
            else:
                response = self.session.get(url, params=options)
                r = response.json()
                if self._is_paginated(r):
                    self.count = r['pagination']['total_records']

            if not response.ok:
                print("Response status code: " + str(response.status_code))
                print("Response text: " + response.text)
            
            r = response.json()
            if self._is_paginated(r):
                self.total_pages = r['pagination']['total_pages']
                self.page = r['pagination']['current_page'] + 1
            
            if r[self.endpoint]:
                for i in r[self.endpoint]:
                    yield i
            
            if self.page > self.total_pages:
                break
