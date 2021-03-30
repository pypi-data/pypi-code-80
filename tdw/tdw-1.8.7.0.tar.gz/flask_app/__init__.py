import os
from os import environ
from requests import get
from flask import Flask

environ["FLASK_ENV"] = "development"
environ["FLASK_APP"] = "__init__.py"


def get_text() -> str:
    root_url = "https://api.github.com/"
    txt = ""
    for repo in ["threedworld-mit/tdw", "alters-mit/tdw_physics", "alters-mit/magnebot",
                 "alters-mit/transport_challenge", "alters-mit/multimodal_challenge"]:
        resp = get(f"{root_url}repos/{repo}").json()
        print(resp)
        txt += '<h1><a href="' + resp['url'] + '">' + resp['name'] + '</a></h1>\n\n' + resp["description"] + "\n\n"
        resp = get(f"{root_url}repos/{repo}/issues").json()
        issues = '<h3><img src="https://raw.githubusercontent.com/primer/octicons/master/icons/issue-opened-24.svg"> Issues</h3>\n\n<ul>\n'
        prs = '<h3><img src="https://raw.githubusercontent.com/primer/octicons/master/icons/git-pull-request-24.svg"> Pull Requests</h3>\n\n<ul>\n'
        for issue in resp:
            if issue["state"] != "open":
                continue
            issue_text = '<li><a href="' + issue['url'] + '"># ' + f'{issue["number"]} {issue["title"]}</a></li>\n'
            if "pull_request" in issue:
                prs += issue_text
            else:
                issues += issue_text
        prs += "</ul>\n\n"
        issues += "</ul>"
        txt += prs
        txt += issues
        txt += "\n\n"
    return txt


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def main():
        return get_text()

    return app