"""House the Solr API interaction."""

import csv
import datetime
import json
import logging
import pytz
import requests

import urllib.parse as urlparse
from urllib.parse import urlencode

logger = logging.getLogger(__name__)


class Solr(object):
    """Provide the API layer to Solr instances."""

    ENDPOINTS = {
        'truncate_docs_by_query': '{collection}/update',
        'index_json_docs': '{collection}/update/json/docs',
        'schema': '{collection}/schema',
        'collections': 'admin/collections?wt=json&action={action}&',
        'index': "{collection}/update",
        'delta_select': '{collection}/select?q={type_name}%3A{data_type}'
                        '&rows=0&wt=json&stats=true&stats.field={field_name}'
    }

    def __init__(self, collection, dsn='http://localhost:8983/solr/',
                 auth_type='basic', username=None, password=None):
        """Initiate commonly used variables in the Solr object."""
        self.collection = collection
        self.dsn = dsn
        self.auth_type = auth_type
        self.username = username
        self.password = password
        self.auth = (username, password)

        # Authentication is pretty new concept as a wrapper for solr.
        # Initially, only basic auth is supported

        supported_auth_types = ['basic']

        if self.auth_type not in supported_auth_types:
                raise NotImplementedError('{} is not a supported auth type'
                                          'Currently, we only support one of'
                                          'the following {}'.format(self.auth_type, str(supported_auth_types)))

    def _get_endpoint(self, endpoint):
        """Give a properly formatted absoluter URL for API requests.

        We do some checking and processing on the dsn and endpoint text because
        urljoin doesn't play nicely with trailing and leading '/'s

        :param endpoint: the api endpoint we're sending a request to
        :type endpoint: str
        :return: the absolute URI to send a request to
        :rtype: str
        """
        if not self.dsn.endswith('/'):
            self.dsn += '/'
            logger.debug('corrected dsn to {}'.format(self.dsn))

        endpoint = self.ENDPOINTS[endpoint]

        return urlparse.urljoin(self.dsn, endpoint)

    def collections(self, action='CLUSTERSTATUS', **kwargs):
        """Provide a layer to interact with the collections Solr endpoint.

        The collections endpoint requires params in the URL string. The
        available actions can be found at
        https://cwiki.apache.org/confluence/display/solr/Collections+API

        The kwargs arguments can be used to provide the arguments to the URL
        structure. The kwargs will be used to create a query string and append
        that to the base URL. The kwargs are automagically url encoded. So, the
        idea here is that you can pass named arguments that represent the API
        that Solr exposes for collections infinitely and it will be urlencoded
        in a reliable fashion to the API endpoint.

        Usage:
          - solr_inst.collections(action='CREATE', name='some', numShards='2')

        :param action: The endpoint action
        :param kwargs: key values of URL params we want to send to the endpoint
        :return: request response object
        :rtype: requests.models.Response
        """
        query_string = urlencode(kwargs)
        url = self._get_endpoint('collections').format(action=action) \
            + query_string

        logger.debug('Submitting a collections request to {}'.format(url))
        res = requests.get(url, auth=self.auth)
        logger.debug('Request response: {}'.format(res.json()))

        res.raise_for_status()

        return res

    def schema(self, get=None, **kwargs):
        """Provide an API interface for the Schema endpoint.

        Kwargs in our use case is used to call different functions relative
        to the `schema` endpoint.
        https://cwiki.apache.org/confluence/display/solr/Schema+API

        NB: To pass a command to Solr, your kwargs items must use underscores
            in the command instead of a dash (because Python interprets the
            dash in the command as an expression and disallows it). See usage
            below

        Usage:
          - # this command passes a single request to Solr
            solr_inst.schema(add_field='{"name":"new_field","type":"tdate"}')

          - # this command passes multiple commands on the same type to Solr
            solr_inst.schema(add_field='[
              {"name":"new_field","type":"tdate"},
              {"name":"new_field_2","type":"tdate"}
            ]')

          - # this command passes multiple commands of different types to Solr
            solr_inst.schema(add_field='{"name":"new_field","type":"tdate"}',
                             delete_field='{"name":"existing_field"}')

        :param get:
        :param kwargs:
        :return: the requests response object
        :rtype: requests.models.Response
        """
        if get is not None:
            logger.debug('The request is a GET request')
            url = self._get_endpoint('schema').format(
                collection=self.collection)

            # Do some URL cleaning
            if not url.endswith('/'):
                url += '/'
            url += get

            # fetch the schmea
            response = requests.get(url, auth=self.auth)
        else:
            logger.debug('The request is not a GET request')
            data = ''
            for action, value in kwargs.items():
                data += '"{}":{}'.format(action.replace('_', '-'), value)
            data = "{" + data + "}"

            logger.debug('Constructed query string {}'.format(data))

            response = self.post_to_solr(data, 'schema')

        return response

    def update_docs(self, docs, commit=False, overwrite_check=True, **kwargs):
        """Index a list of solr docs using the default update handler.

        Note that docs needs to have keys and values in solr format.
        example for adding to existing solr entry:
            docs = [{"id": "123", "new_val_s": "New Value"}]
            kwarg_commands = {"new_val_s": "add"}

            update_docs(
                docs,
                commit=True,
                **kwarg_commands
            )

        This can handle solr commands (add, set etc) at a root level per doc in
         in the list. If there are nested docs, these will automatically be
         converted to the solr _childDocuments_ format.

        :param docs: list of solr documents to index
        :type docs: list
        :param commit: should the commit command be issued as part of the index
        :type commit: bool
        :param overwrite_check: if docs are known to be unique, this may
            improve performance by disabling solrs check for uniqueness
        :type overwrite_check: bool
        :param kwargs: applies solr command to a field. in the format of
            field_name=command
        :return: requests response object
        :rtype: requests.models.Response
        """
        assert isinstance(docs, list)
        for doc in docs:
            assert isinstance(doc, dict)

        logger.info('Received list of {} solr docs for indexing...'.format(
            len(docs)
        ))

        # Set query params
        params = {}

        if commit:
            logger.debug('Setting commit instruction to true')
            params['commit'] = 'true'

        if not overwrite_check:
            logger.debug(
                'overwrite_check set to False, thus Solr will not check for'
                'duplicate documents based on doc ID'
            )
            params['overwrite'] = 'false'

        # transform dict object to correct format for solr update.
        data = []
        for doc in docs:
            # If there are any commands to be applied to fields, do so
            doc = self.set_solr_commands(doc, kwargs)
            # If there are any child docs, convert to solr child doc notation
            doc = self.solr_doc_to_solr_child_docs(doc)

            data.append(doc)

        response = self.post_to_solr(json.dumps(data), 'index', params=params)

        return response

    def update_by_json(self, doc, commit=False, overwrite_check=True):
        """Index a single doc to solr using the solr json doc handler.

        Note that docs needs to have keys and values in solr format.
        Example use:
            doc = json.dumps({
                "id": "123",
                "entry_s": "My new entry"
            })
            update_by_json(
                doc,
                commit=True
            )

        :param doc: a single json solr style doc
        :type doc: str
        :param commit: True to commit changes in Solr; False otherwise
        :type commit: bool
        :param overwrite_check: Disable the Solr unique key check.
        :type overwrite_check: bool
        :return: requests response object
        :rtype: requests.models.Response
        """
        # Check that structure of incoming object is as expected
        assert isinstance(doc, str)
        assert isinstance(json.loads(doc), dict)

        params = {}

        if commit:
            logger.debug('Setting commit instruction to true')
            params['commit'] = 'true'

        if not overwrite_check:
            logger.debug(
                'overwrite_check set to False, thus Solr will not check for'
                'duplicate documents based on doc ID'
            )
            params['overwrite'] = 'false'

        # Solr requires a special format for nested lists in a doc
        data = json.dumps(self.solr_doc_to_solr_child_docs(json.loads(doc)))

        logger.debug(data)

        response = self.post_to_solr(data, 'index_json_docs', params=params)
        return response

    def update_by_csv(self, csv_file, column_headers=None, **kwargs):
        """Post CSV media to Solr url.

        :param csv_file: CSV media as string
        :type csv_file: file or FileIO[str]
        :param column_headers: if absent in the CSV file, provide the headers
        :type column_headers: list
        :param kwargs: Solr CSV index params as per https://goo.gl/L2XC3V
        :return: Solr Response
        :rtype: requests.models.Response
        """
        # Establish CSV headers
        headers_in_file = False
        if not column_headers:
            reader = csv.DictReader(csv_file)
            column_headers = reader.fieldnames
            headers_in_file = True

        # Get the url query params for mv field splitting
        suffix, params = self.generate_mv_fields_url_suffix(column_headers)

        # Deal with pattern for providing field names to Solr
        if not headers_in_file:
            params['fieldnames'] = ','.join(map(str, column_headers))

        # Add in any other options to the query
        for k, v in kwargs.items():
            params[k] = v

        # Execute the index request
        response = self.post_to_solr(csv, 'index', 'application/csv', params)

        return response

    def get_max_field_value(self, data_type,
                            type_name='type', field_name='delta'):
        """Look up the delta of any given type in Solr.

        :param type_name: the name of the type field e.g. type c for customers
            where type is type_name
        :type type_name: str
        :param field_name: the name of the field to query e.g. max value for
            field delta
        :type field_name: str
        :param data_type: document type e.g. type c for customers where c is
            data_type
        :type data_type: str
        :return: delta field value
        :rtype: str
        """
        logger.info('Delta on {}. Type {}'.format(self.collection, data_type))

        url = self._get_endpoint('delta_select').format(
            collection=self.collection,
            type_name=type_name,
            data_type=data_type,
            field_name=field_name)

        logger.debug('Delta url {}'.format(url))

        res = requests.get(url, auth=self.auth)
        res.raise_for_status()

        res_content = res.json()
        delta = res_content['stats']['stats_fields'][field_name]['max']

        logger.info('Delta: {}'.format(delta))
        return delta

    def truncate_docs_by_query(self, query_value, query_field='type'):
        """Truncate Solr documents filtered by query result.

        :param query_value: filter value for data to truncate
        :param query_field: field name for which to filter truncation against
        :return: Solr response object
        :rtype: requests.models.Response
        """
        logger.info('Truncating solr docs with filter {}:{}'.format(
            query_field,
            query_value
        ))

        data = {
            'delete': {
                query_field: query_value
            }
        }

        response = self.post_to_solr(data, 'truncate_docs_by_query')

        return response

    def generate_mv_fields_url_suffix(self, header):
        """Generate the URL suffix required to index multi-valued fields.

        Returns a suffix used on the solr update URL to tell the update handler
        which of the fields in the provided CSV file are multi-valued fields.

        :param header: list of column names as strings
        :type header: list
        :return: mv url suffix string and dict of query components
        :rtype: (str,dict)
        """
        # get list of dynamic fields from solr
        solr_schema = json.loads(self.schema(get='dynamicfields').text)
        dyn_fields = solr_schema['dynamicFields']

        mv_fields = []
        for field in dyn_fields:
            # Solr Dynamic Fields always have an astrix. Remove this.
            if 'multiValued' in field:
                if field['multiValued']:
                    mv_fields.append(field['name'].replace('*', ''))

        url_query_components = {}
        for column in header:
            if any([ext in column for ext in mv_fields]):
                url_query_components['f.{}.split'.format(column)] = 'true'

        url_suffix = urlencode(url_query_components)

        logger.debug(url_query_components)
        logger.debug(url_suffix)

        return url_suffix, url_query_components

    def post_to_solr(self, data, end_point,
                     content_type='application/json', params=None):
        """Post solr style json doc to selected endpoint.

        :param data: solr documents
        :type data: str
        :param end_point:
        :type end_point: str
        :param content_type:
        :type content_type: str
        :param params:
        :type params:
        :return: Solr response object
        :rtype: requests.models.Response
        """
        logger.debug('Data being submitted to index request {}'.format(data))

        url = self._get_endpoint(end_point).format(collection=self.collection)
        logger.debug('url set to {}'.format(url))

        headers = {
            'charset': 'utf-8',
            'content-type': content_type
        }

        res = requests.post(
            url,
            data=data,
            headers=headers,
            params=params,
            auth=self.auth
        )

        # Execute the index request
        logger.debug("Index URL: {}".format(res.url))
        logger.debug(res.text)

        # Check that response was successful
        res.raise_for_status()

        return res

    @staticmethod
    def solr_doc_to_solr_child_docs(solr_doc, parent_field_name='parent_s',
                                    path=""):
        """Convert list or dict indices to valid Solr _childDocuments_ format.

        Essentially, this script converts all lists that are not under the
        _childDocuments_ namespace and puts them in that namespace. The result
        of this is that, on every level, there is no other list in the
        dictionary other than the one named '_childDocuments_'

        :param solr_doc: the solr doc dict to transform
        :type solr_doc: dict
        :param parent_field_name: the name of the path to insert into the child
          docs
        :param path: the path to the child doc from the root level doc
        :type parent_field_name: str
        :return: an appropriately JSON transformed string
        :rtype: dict
        """
        child_items = []
        assert isinstance(solr_doc, dict)
        # Sorted else there is a chance that unit test is false
        for key in sorted(solr_doc.keys()):
            is_processed = False
            val = solr_doc[key]
            if not isinstance(val, list):
                continue

            # If the key contains a list of dicts, then those dicts need to
            #   be added as a flat list.  If this has happened, then the
            #   child needs to be removed from the original solr_doc.
            for item in val:
                if not isinstance(item, dict):
                    continue
                logger.debug(
                    'Found an item at key "{}" which will be '
                    'moved into _childDocuments_'.format(key)
                )
                item.update({parent_field_name: key})
                new_path = path + (".{}".format(key) if path else "{}".format(key))
                item['nested_path_s'] = new_path

                child_items.append(Solr.solr_doc_to_solr_child_docs(
                    item, path=new_path))
                is_processed = True
            # If the child item is a dict and gets added to _childDocs_,
            #   Then pop it.  Else don't.
            if is_processed:
                solr_doc.pop(key)
        logger.debug(
            '{} child_items put into _childDocuments_'.format(len(child_items))
        )

        if child_items:
            solr_doc.update({'_childDocuments_': child_items})

        return solr_doc

    @staticmethod
    def set_solr_commands(doc, commands):
        """Set field in Solr doc with supplied command.

        :param doc: solr doc to which commands will be applied
        :type doc: dict
        :param commands: collection of field:commands to be set
        :type commands: dict
        :return: updated solr doc
        :rtype: dict
        """
        for field, command in commands.items():
            logger.debug('updating {} to command {}'.format(field, command))
            try:
                doc[field] = {command: doc[field]}
                logger.debug('updated doc to {}'.format(doc[field]))
            except KeyError:
                logger.info('{} does not exist in doc. Skipping set of '
                            'command to {}'.format(field, command))

        return doc

    @staticmethod
    def format_date(python_date):
        """Convert a python date into a solr date.

        :param python_date: Python datetime object
        :type python_date: datetime.datetime.date
        :return: Solr date sting
        :rtype: str
        """
        if not python_date:
            return None
        # in format YYYY-MM-DDTHH:MM:SS.Z
        solr_date = datetime.datetime.strftime(
            python_date.astimezone(pytz.utc),
            "%Y-%m-%dT%H:%M:%SZ"
        )
        return solr_date

    @staticmethod
    def solr_type_serializer(key, val):
        """Check type of the value and modify key/value as required by Solr.

        :param key: The key that usually gets modified.
        :type key: str
        :param val: The value which defines the type identifier.
        :type val: Any
        :return: the modified key, value pair.
        :rtype: tuple
        """
        if isinstance(val, str):
            key += '_s'
        elif isinstance(val, bool):
            key += '_b'
            val = str(val).lower()
        elif isinstance(val, int):
            key += '_i'
        elif isinstance(val, float):
            key += '_f'
        elif isinstance(val, datetime.datetime):
            key += '_tdt'
            val = Solr.format_date(val)
        elif isinstance(val, Point):
            key += Point.solr_suffix
            val = val.solr_format()
        elif isinstance(val, Currency):
            key += Currency.solr_suffix
            val = val.solr_format()

        return key, val


class Point(object):
    """A latlon point."""

    solr_suffix = "_p"

    def __init__(self, lat, lon):
        """Define a latlong point.

        :param lat: Latitudinal point.
        :type lat: float or int
        :param lon: Longitudinal point.
        :type lon: float
        """
        self.lat = float(lat)
        self.lon = float(lon)

    def solr_format(self):
        """Format a point as required by Solr.

        :return: Solr formatted point.
        :rtype: str
        """
        return "{},{}".format(self.lat, self.lon)


class Currency(object):
    """Create a currency object."""

    solr_suffix = "_c"

    def __init__(self, value, symbol):
        """Define currency value.

        :param value: The value of the currency
        :type value: float or int
        :param symbol: The symbol of the currency
        :type symbol: str
        """
        self.value = float(value)
        self.symbol = symbol

    def solr_format(self):
        """Format currency as required by Solr.

        :return: Solr formatted currency.
        :rtype: str
        """
        return "{}{}".format(self.symbol, self.value)
