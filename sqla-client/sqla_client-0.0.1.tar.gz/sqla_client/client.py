import requests


class SQLA(object):
    def __init__(self, sqla_url, pat):
        self.sqla_url = sqla_url
        self.session = requests.Session()
        self.session.headers.update({"Authorization": "Bearer {}".format(pat)})

    def test_credentials(self):
        try:
            response = self._get("api/session")
            return True
        except requests.exceptions.HTTPError:
            return False

    def queries(self, page=1, page_size=25):
        """GET sql/queries"""
        return self._get(
            "sql/queries", params=dict(page=page, page_size=page_size)
        ).json()

    def dashboards(self, page=1, page_size=25):
        """GET sql/dashboards"""
        return self._get(
            "sql/dashboards", params=dict(page=page, page_size=page_size)
        ).json()

    def dashboard(self, slug):
        """GET sql/dashboards/{slug}"""
        return self._get("sql/dashboards/{}".format(slug)).json()

    def create_dashboard(self, name):
        return self._post("sql/dashboards", json={"name": name}).json()

    def update_dashboard(self, dashboard_id, properties):
        return self._post(
            "sql/dashboards/{}".format(dashboard_id), json=properties
        ).json()

    def create_widget(self, dashboard_id, visualization_id, text, options):
        data = {
            "dashboard_id": dashboard_id,
            "visualization_id": visualization_id,
            "text": text,
            "options": options,
            "width": 1,
        }
        return self._post("sql/widgets", json=data)

    def duplicate_dashboard(self, slug, new_name=None):
        current_dashboard = self.dashboard(slug)

        if new_name is None:
            new_name = "Copy of: {}".format(current_dashboard["name"])

        new_dashboard = self.create_dashboard(new_name)
        if current_dashboard["tags"]:
            self.update_dashboard(
                new_dashboard["id"], {"tags": current_dashboard["tags"]}
            )

        for widget in current_dashboard["widgets"]:
            visualization_id = None
            if "visualization" in widget:
                visualization_id = widget["visualization"]["id"]
            self.create_widget(
                new_dashboard["id"], visualization_id, widget["text"], widget["options"]
            )

        return new_dashboard

    def duplicate_query(self, query_id, new_name=None):

        response = self._post(f"sql/queries/{query_id}/fork")
        new_query = response.json()

        if not new_name:
            return new_query

        new_query["name"] = new_name

        return self.update_query(new_query.get("id"), new_query).json()

    def scheduled_queries(self):
        """Loads all queries and returns only the scheduled ones."""
        queries = self.paginate(self.queries)
        return filter(lambda query: query["schedule"] is not None, queries)

    def update_query(self, query_id, data):
        """POST /sql/queries/{query_id} with the provided data object."""
        path = "sql/queries/{}".format(query_id)
        return self._post(path, json=data)

    def paginate(self, resource):
        """Load all items of a paginated resource"""
        stop_loading = False
        page = 1
        page_size = 100

        items = []

        while not stop_loading:
            response = resource(page=page, page_size=page_size)

            items += response["results"]
            page += 1

            stop_loading = response["page"] * response["page_size"] >= response["count"]

        return items

    def _get(self, path, **kwargs):
        return self._request("GET", path, **kwargs)

    def _post(self, path, **kwargs):
        return self._request("POST", path, **kwargs)

    def _request(self, method, path, **kwargs):
        url = "{}/api/2.0/preview/{}".format(self.sqla_url, path)
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response
