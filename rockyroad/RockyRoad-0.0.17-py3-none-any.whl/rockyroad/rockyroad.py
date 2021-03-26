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


@headers({"Ocp-Apim-Subscription-Key": key})
class RockyRoad(Consumer):
    """Provides a wrapper for the RockyRoad API.

    Usage Example:

        from rockyroad.rockyroad import RockyRoad

        rr = RockyRoad(base_url='INSERT_URL_FOR_API')

        api_response = rr.get_hello_world()
        print(api_response)

        api_response = rr.get_alert_requests()
        print(api_response)

        api_response = rr.get_alert_requests(creator_email='user@acme.com')
        print(api_response)

        api_response = rr.add_alert_request(new_alert_request_json)
        print(api_response)

        api_response = rr.delete_alert_requests(brand=brand, alert_request_id=alert_request_id)
        print(api_response)

        api_response = rr.get_alert_reports()
        print(api_response)

        api_response = rr.get_alert_reports(creator_email='user@acme.com')
        print(api_response)

        api_response = rr.get_utildata(brand=brand, time_period='today')
        print(api_response)

        api_response = rr.get_utildata_stats()
        print(api_response)

        api_response = rr.get_dealers()
        print(api_response)

        api_response = rr.get_customers_and_machines(dealer_name)
        print(api_response)

    """

    @returns.json
    @get("/")
    def get_hello_world(self):
        """This call will return Hello World."""

    @returns.json
    @get("/alert-requests")
    def get_alert_requests(self, creator_email: Query = None):
        """This call will return detailed alert request information for the creator's email specified or all alert requests if no email is specified."""

    @returns.json
    @json
    @post("/alert-requests")
    def add_alert_request(self, new_alert_request: Body):
        """This call will create an alert request with the specified parameters."""

    @returns.json
    @json
    @delete("/alert-requests")
    def delete_alert_requests(
        self, brand: Query(type=str), alert_request_id: Query(type=int)
    ):
        """This call will delete the alert request for the specified brand and alert request id."""

    @returns.json
    @get("/alert-reports")
    def get_alert_reports(self, creator_email: Query = None):
        """This call will return detailed alert report information for the creator's email specified or all alert reports if no email is specified."""

    @returns.json
    @get("/utildata")
    def get_utildata(self, brand: Query(type=str), time_period: Query(type=str)):
        """This call will return utilization data for the time period specified in the query parameter."""

    @returns.json
    @get("/utildata/stats")
    def get_utildata_stats(self):
        """This call will return stats for the utildatastatus table."""

    @returns.json
    @get("/dealers")
    def get_dealers(self):
        """This call will return a list of dealers."""

    @returns.json
    @get("/dealers/customers_and_machines")
    def get_customers_and_machines(self, dealer_name: Query(type=str)):
        """This call will return a list of customers and machines supported by the specified dealer."""
