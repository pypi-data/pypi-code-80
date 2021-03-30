from uplink import Consumer, get, post, delete, returns, headers, Body, json, Query
import os

try:
    key = os.environ["OCP_APIM_SUBSCRIPTION_KEY"]
except KeyError as e:
    print(
        f"""ERROR: Define the environment variable {e} with your subscription key.  For example:

    export OCP_APIM_SUBSCRIPTION_KEY="INSERT_YOUR_SUBSCRIPTION_KEY"

    """
    )
    key = None


# @headers({"Ocp-Apim-Subscription-Key": key})
# class RockyRoad(Consumer):
#     """Provides a wrapper for the RockyRoad API.

#     Usage Example:

#         from rockyroad.rockyroad import RockyRoad

#         rr = RockyRoad(base_url='INSERT_URL_FOR_API')

#         api_response = rr.get_hello_world()
#         print(api_response)

#         api_response = rr.get_alert_requests()
#         print(api_response)

#         api_response = rr.get_alert_requests(creator_email='user@acme.com')
#         print(api_response)

#         api_response = rr.add_alert_request(new_alert_request_json)
#         print(api_response)

#         api_response = rr.delete_alert_requests(brand=brand, alert_request_id=alert_request_id)
#         print(api_response)

#         api_response = rr.get_alert_reports()
#         print(api_response)

#         api_response = rr.get_alert_reports(creator_email='user@acme.com')
#         print(api_response)

#         api_response = rr.get_utildata(brand=brand, time_period='today')
#         print(api_response)

#         api_response = rr.get_utildata_stats()
#         print(api_response)

#         api_response = rr.get_dealers()
#         print(api_response)

#         api_response = rr.get_customers_and_machines(dealer_name)
#         print(api_response)

#     """

#     @returns.json
#     @get("/")
#     def get_hello_world(self):
#         """This call will return Hello World."""

#     @returns.json
#     @get("/alert-requests")
#     def _get_alert_requests(self, creator_email: Query = None):
#         """This call will return detailed alert request information for the creator's email specified or all alert requests if no email is specified."""

#     @returns.json
#     @json
#     @post("/alert-requests")
#     def add_alert_request(self, new_alert_request: Body):
#         """This call will create an alert request with the specified parameters."""

#     @returns.json
#     @json
#     @delete("/alert-requests")
#     def delete_alert_requests(
#         self, brand: Query(type=str), alert_request_id: Query(type=int)
#     ):
#         """This call will delete the alert request for the specified brand and alert request id."""

#     @returns.json
#     @get("/alert-reports")
#     def get_alert_reports(self, creator_email: Query = None):
#         """This call will return detailed alert report information for the creator's email specified or all alert reports if no email is specified."""

#     @returns.json
#     @get("/utildata")
#     def get_utildata(self, brand: Query(type=str), time_period: Query(type=str)):
#         """This call will return utilization data for the time period specified in the query parameter."""

#     @returns.json
#     @get("/utildata/stats")
#     def get_utildata_stats(self):
#         """This call will return stats for the utildatastatus table."""

#     @returns.json
#     @get("/dealers")
#     def get_dealers(self):
#         """This call will return a list of dealers."""

#     @returns.json
#     @get("/dealers/customers-and-machines")
#     def get_customers_and_machines(self, dealer_name: Query(type=str)):
#         """This call will return a list of customers and machines supported by the specified dealer."""


def build(base_url):
    """Returns a resource to interface with the RockyRoad API.

    Usage Example:

        from rockyroad.rockyroad import build

        service = build(base_url='INSERT_URL_FOR_API')

        api_response = service.helloWorld().list()
        print(api_response)

        api_response = service.alertRequests().list()
        print(api_response)

        api_response = service.alertRequests().list(creator_email='user@acme.com')
        print(api_response)

        api_response = service.alertRequests().insert(new_alert_request_json)
        print(api_response)

        api_response = service.alertRequests().delete(brand=brand, alert_request_id=alert_request_id)
        print(api_response)

        api_response = service.alertReports().list()
        print(api_response)

        api_response = service.alertReports().list(creator_email='user@acme.com')
        print(api_response)

        api_response = service.utilData().list(brand=brand, time_period='today')
        print(api_response)

        api_response = service.utilStats().list()
        print(api_response)

        api_response = service.dealers().list()
        print(api_response)

        api_response = service.customers().list(dealer_name=dealer_name)
        print(api_response)

    """
    return Resource(base_url=base_url)


class Resource(object):
    """Inteface to resources for the RockyRoad API."""

    def __init__(self, *args, **kw):
        self._base_url = kw["base_url"]

    def helloWorld(self):
        return self.__HelloWorld(self)

    def alertRequests(self):
        return self.__AlertRequests(self)

    def alertReports(self):
        return self.__AlertReports(self)

    def utilData(self):
        return self.__UtilData(self)

    def utilStats(self):
        return self.__UtilStats(self)

    def dealers(self):
        return self.__Dealers(self)

    def customers(self):
        return self.__Customers(self)

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __HelloWorld(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @get("/")
        def list(self):
            """This call will return Hello World."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __AlertRequests(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @get("/alert-requests")
        def list(self, creator_email: Query = None):
            """This call will return detailed alert request information for the creator's email specified or all alert requests if no email is specified."""

        @returns.json
        @json
        @post("/alert-requests")
        def insert(self, new_alert_request: Body):
            """This call will create an alert request with the specified parameters."""

        @returns.json
        @delete("/alert-requests")
        def delete(self, brand: Query(type=str), alert_request_id: Query(type=int)):
            """This call will delete the alert request for the specified brand and alert request id."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __AlertReports(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @get("/alert-reports")
        def list(self, creator_email: Query = None):
            """This call will return detailed alert report information for the creator's email specified or all alert reports if no email is specified."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __UtilData(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @get("/utildata")
        def list(self, brand: Query(type=str), time_period: Query(type=str)):
            """This call will return utilization data for the time period specified in the query parameter."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __UtilStats(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @get("/utilstats")
        def list(self):
            """This call will return stats for the utildatastatus table."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Dealers(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @get("/dealers")
        def list(self):
            """This call will return a list of dealers."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Customers(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @get("/customers")
        def list(self, dealer_name: Query(type=str)):
            """This call will return a list of customers and machines supported by the specified dealer."""