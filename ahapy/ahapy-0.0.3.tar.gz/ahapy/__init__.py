import requests


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

        super(AhaV1, self).__init__(sub_domain, api_key)

    def _count(self, endpoint, **options):
        url = self.url + self.version + endpoint
        response = self.session.get(url, params=options)
        r = response.json()
        self.count = r['pagination']['total_records']
        return self.count
    
    def query (self, endpoint, **options):
        """
        Query for Aha.io V1 endpoint
        """
        while True:
            url = self.url + self.version + endpoint
            if self.page <= self.total_pages:
                url = url + '?page=' + str(self.page)
                response = self.session.get(url, params=options)
            else:
                response = self.session.get(url, params=options)
                r = response.json()
                self.count = r['pagination']['total_records']

            if not response.ok:
                print("Response status code: " + str(response.status_code))
                print("Response text: " + response.text)
            
            r = response.json()

            self.total_pages = r['pagination']['total_pages']
            self.page = r['pagination']['current_page'] + 1
            
            if r[endpoint]:
                for i in r[endpoint]:
                    yield i
            
            if self.page > self.total_pages:
                break

