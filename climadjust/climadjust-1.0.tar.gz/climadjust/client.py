import os
import logging
import requests
import json
from climadjust import urls
from climadjust.clientMethods.dataset_mixin import DatasetMixin
from climadjust.clientMethods.experiment_mixin import ExperimentMixin
from tenacity import Retrying
from tenacity import stop_after_attempt
from tenacity import stop_after_delay
from tenacity import wait_fixed
from tenacity import retry_if_exception_type


def custom_retry(f):
    # Does more or less the same as @retry but using our class arguments
    def wrapper(*args, **kwargs):
        r = Retrying(stop=(stop_after_delay(args[0].max_time) |
                           stop_after_attempt(args[0].n_retries)),
                     wait=wait_fixed(5),
                     retry=(retry_if_exception_type(requests.exceptions.ConnectionError) |
                            retry_if_exception_type(requests.exceptions.ChunkedEncodingError) |
                            retry_if_exception_type(ConnectionError)))
        return r.call(f, *args, **kwargs)
    return wrapper


class Client(DatasetMixin, ExperimentMixin):
    def __init__(self,
                 UID=None,
                 key=None,
                 quiet=False,
                 debug=True,
                 n_retries=10,
                 max_time=60,
                 base_url=None,
                 ):
        self.quiet = quiet
        self.debug = debug
        self.n_retries = n_retries
        self.max_time = max_time
        self.base_url = urls.BASE_URL if base_url is None else base_url
        if UID is not None and key is not None:
            self.api_key = ':'.join([UID, key])
        else:
            self.api_key = None

        if not self.quiet:
            if self.debug:
                level = logging.DEBUG
            else:
                level = logging.INFO

            logging.basicConfig(level=level,
                                format='%(asctime)s %(levelname)s %(message)s')

        if self.api_key is None:
            # The data is read from the api file
            config_file_path = os.environ.get('CLIMADJUSTAPI_RC', os.path.expanduser('~/.climadjustapirc'))
            if os.path.exists(config_file_path):
                config = _read_config(config_file_path)
                self.api_key = ':'.join([config['UID'], config['Key']])
            else:
                if not self.quiet:
                    logging.error('Neither configuration file nor key argument were found')
                raise NotImplementedError('Neither configuration file nor key argument were found')

    def authenticate(self):
        """
        API authentication. Needed to connect to the API
        """
        UID = self.api_key.split(':')[0]
        key = self.api_key.split(':')[1]
        r = self.__sending_authetication(UID, key)
        self.__set_session(r)

    @custom_retry
    def __sending_authetication(self, UID, key):
        params = json.dumps({'username': UID, 'password': key})
        res = requests.post(self.base_url + urls.AUTH,
                            data=params,
                            headers={'Content-type': 'application/json'})
        self.raise_if_exception(res)
        return res

    def __set_session(self, request):
        content = json.loads(request.content.decode('UTF-8'))  # Active session
        self.token = 'Bearer ' + content['token']
        self.validation = content['validity']

    """ HTTP """
    @custom_retry
    def request_get(self, url, params={}):
        res = requests.get(self.base_url + url,
                           params=params,
                           headers=self.__headers())
        self.raise_if_exception(res)
        return json.loads(res.text)

    @custom_retry
    def request_download(self, url, download_path=None):
        local_filename = download_path if download_path else '/tmp/result.nc'
        """ 
        Create a partial file where downloading. Use the url in order to 
        ensure that name is unique. When download is finished, rename the
        file to the final file.
        """
        partial_filename = local_filename + "_" + url.replace("/", "_") + ".part"
        if os.path.exists(partial_filename):
            self.__download(url, partial_filename, True)
        else:
            self.__download(url, partial_filename, False)
        os.rename(partial_filename, local_filename)
        return local_filename

    @custom_retry
    def request_post(self, url, params):
        params = json.dumps(params)
        res = requests.post(self.base_url + url,
                            data=params,
                            headers=self.__headers())
        print(res.text)
        self.raise_if_exception(res)
        return json.loads(res.text)

    @custom_retry
    def request_upload(self, url, file, params):
        res = requests.post(self.base_url + url,
                            data=params,
                            files={'file': open(file, 'rb')},
                            headers={'Authorization': self.token})
        self.raise_if_exception(res)
        return json.loads(res.text)

    @custom_retry
    def request_delete(self, url, params):
        res = requests.delete(url, params, headers=self.__headers())
        self.raise_if_exception(res)
        return res.text

    def __headers(self):
        return {'Content-type': 'application/json', 'Authorization': self.token}

    def __download(self, url, local_filename, resume=False):
        headers = {'Authorization': self.token}
        if resume:
            downloaded_bytes = os.path.getsize(local_filename)
            headers['Range'] = 'bytes=' + str(downloaded_bytes) + "-"
            file_mode = 'ab'
        else:
            file_mode = 'wb'

        with requests.get(
                self.base_url + url,
                headers=headers,
                stream=True) as r:
            self.raise_if_exception(r)
            with open(local_filename, file_mode) as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    def raise_if_exception(self, res):
        try:
            res.raise_for_status()
        except requests.HTTPError as e:
            if not self.quiet:
                logging.error(e)
            raise


def _read_config(path):
    config = {}
    with open(path) as f:
        for l in f.readlines():
            if ':' in l:
                k, v = l.strip().split(':', 1)
                if k in ('UID', 'Key'):
                    config[k] = v.strip()
    return config


