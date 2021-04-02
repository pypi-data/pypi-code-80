import requests
import json

def getSessionCookie(email, password):
    url = 'https://octoeverywhere.com/api/user/login'

    values = {'Email': email, 'Password': password}

    headers = {
        "Content-Type": "application/json"
    }

    session = requests.Session()

    r = session.post(url, data=json.dumps(values), headers=headers)

    if r.status_code == 200:
        return session.cookies.get_dict()
    else:
        raise Exception("Incorrect login info with status code of " + str(r.status_code))
