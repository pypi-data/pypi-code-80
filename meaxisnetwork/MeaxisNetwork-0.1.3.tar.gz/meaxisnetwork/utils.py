import requests
import json

def get_url(API):
	return f"https://api.meaxisnetwork.net/v3/{API}"

def HTTPRequest(API, method, **kwargs):
	'''
	Sends a HTTP Request through the MeaxisNetwork API.
	'''
	cookies = {}
	params = {}
	data = {}

	for key, value in kwargs.items():
		vars()[key] = value


	URL = get_url(API)

	return vars(requests)[method](URL, params = params, data = data, cookies = cookies)


def check_response(Response):
	if Response.status_code != 200:
		response_text = Response.text
		error_code = response_text[-9:].replace("(", "").replace(")", "").replace('"', '')
		error_data = {"error_message": response_text.replace('"', ''), "http_status_code": Response.status_code, "documentation_reference": f"https://meaxisnetwork.net/create/docs/api/error-codes#{error_code}", "error_code": error_code}
		return json.dumps(error_data, indent = 2)
	else:
		return True