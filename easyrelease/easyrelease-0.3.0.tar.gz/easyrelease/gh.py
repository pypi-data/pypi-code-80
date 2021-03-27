# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_gh.ipynb (unless otherwise specified).

__all__ = ['get_repo_name', 'get_base_repo_url', 'write_gh_template', 'get_last_tag', 'get_commit_msgs',
           'add_pull_request_link', 'release_report', 'get_gh_credentials', 'get_tags', 'get_gh_config',
           'make_gh_release', 'make_changelog']

# Cell
import os
import re
import yaml
import subprocess
import requests
from requests.auth import HTTPBasicAuth
import json
from urllib.parse import urlparse
from .utils import (
    get_config,
    read_credentials,
    check_project_root,
    get_template,
    check_git_dir,
)

# Cell
def get_repo_name(git_url):
    "Get repo name out of `git_url`"
    url_path = urlparse(git_url).path
    path_comp = url_path.split("/")
    path_comp = [c for c in path_comp if c != ""]
    repo_name = "/".join(path_comp[0:2])
    return repo_name

# Cell
def get_base_repo_url(git_url):
    "Get base repo URL from `git_url`"
    repo_name = get_repo_name(git_url)
    url_comp = urlparse(git_url)
    scheme = url_comp.scheme
    netloc = url_comp.netloc
    return f"{scheme}://{netloc}/{repo_name}"

# Cell
@check_project_root
def write_gh_template():
    "Write GitHub template for assigning commit messages to categories"
    print("Generating .gh-release-config.yaml")
    if os.path.exists(".gh-release-config.yaml"):
        print(".gh-release-config.yaml already exists. Skipping this step")
    else:
        template = get_template("gh-release-config-template.yaml")
        template = "\n".join(template.split("\n"))  # remove redundant whitespaces
        with open(".gh-release-config.yaml", "w") as f:
            f.write(template)

# Cell
@check_project_root
def get_last_tag():
    "Get last git tag. If there is no tag, then it outputs the first commit hash"
    last_tag = subprocess.run(["git", "describe", "--tags", "--abbrev=0"],
                          capture_output=True).stdout.decode("utf").strip()
    if last_tag != "":
        return last_tag
    else:
        cfg = get_config()
        main_branch = cfg["branch"]
        commits_list = (
            subprocess.run(["git", "rev-list", main_branch], capture_output=True)
            .stdout.decode("utf").strip().split("\n")
        )
        first_commit = commits_list[-1]
        return first_commit

# Cell
def get_commit_msgs(from_tag=None, to="HEAD"):
    "Get commits `from_tag` to `to`. If `from_tag` is None then it will get the commits from latest tag"
    last_tag = from_tag if from_tag is not None else get_last_tag()
    commit_msgs = subprocess.run(["git", "log", f"{last_tag}..{to}", "--pretty=%s"],
                          capture_output=True).stdout.decode("utf").strip().split("\n")
    return commit_msgs

# Cell
@check_project_root
def add_pull_request_link(msg):
    "Add pull request link to commit message `s` if reference is found, e.g. #100"
    cfg = get_config()
    git_url = cfg["git_url"]
    base_repo_url = get_base_repo_url(git_url)
    msg_with_link = re.sub("(#)(\d+)", rf"[\1\2]({base_repo_url}/pull/\2)", msg)
    return msg_with_link

# Cell
@check_project_root
def release_report(gh_config, commit_msgs, report_title=""):
    "Get release report using `report_title`, commit messages `commit_msgs` and GitHub config `gh_config`"
    gh_categories = gh_config["gh_categories"]
    report_list = [report_title]
    for d in gh_categories:
        gh_cat_commits = [add_pull_request_link(f"* {msg}") for msg in commit_msgs if d["keyword"] in msg]
        gh_cat_report = f"{d['title']}\n" + "{}".format("\n".join(gh_cat_commits)) if len(gh_cat_commits) > 0 else ""
        report_list.append(gh_cat_report)
    report_list = [rep for rep in report_list if rep != ""]
    report = "\n\n".join(report_list)
    return report

# Cell
@check_project_root
def get_gh_credentials():
    "Get GitHub credentials from file .gh-credentials"
    cfg = read_credentials(".gh-credentials")
    return (cfg["gh_user"], cfg["gh_token"])

# Cell
def get_tags():
    "Get git tags as list. If multiple tags in one commit, then it puts them into a tuple"
    commit_tags = (
        subprocess.run(["git", "show-ref", "--tags"], capture_output=True)
        .stdout.decode("utf")
        .strip()
        .split("\n")
    )
    commit_tags = [
        (commit_hash, tag.split("/")[-1])
        for t in commit_tags
        for commit_hash, tag in [t.split()]
    ]
    out_tags = []
    for i, (comhash, tag) in enumerate(commit_tags):
        if i > 0 and comhash == commit_tags[i-1][0]:
            out_tags[-1] += " / " + tag
        else:
            out_tags.append(tag)
    return out_tags

# Cell
@check_project_root
def get_gh_config():
    "Get GitHub config"
    with open(".gh-release-config.yaml") as f:
        gh_config = yaml.safe_load(f)
    return gh_config

# Cell
def make_gh_release(draft=False, prerelease=False):
    "Make a GitHub release. Indicate if there is a `draft` or a `prerelease` with default False both"
    cfg = get_config()  # package config
    gh_user, gh_token = get_gh_credentials()
    release_version = cfg["version"]
    user = cfg["user"]
    lib_name = cfg["lib_name"]
    repo_name = get_repo_name(cfg["git_url"])
    target_branch = cfg["branch"]
    commit_msgs = get_commit_msgs()
    gh_config = get_gh_config()
    report = release_report(commit_msgs=commit_msgs, gh_config=gh_config)
    # generate data for release
    gh_data = {
        "tag_name": release_version,
        "target_commitish": target_branch,
        "name": f"Release version {release_version}",
        "body": report,
        "draft": draft,
        "prerelease": prerelease
    }
    gh_api_url = f"https://api.github.com/repos/{repo_name}/releases"
    draft_msg = " draft" if draft else ""
    prerelease_msg = "pre-" if prerelease else ""
    print(f"Creating GitHub {prerelease_msg}release{draft_msg}")
    r = requests.post(
        url=gh_api_url, data=json.dumps(gh_data), auth=HTTPBasicAuth(gh_user, gh_token)
    )
    print(f"Status code: {r.status_code}")
    print(r.text)
    # download new tag from GitHub
    subprocess.run(["git", "fetch"])

# Cell
@check_project_root
def make_changelog():
    "Generate CHANGELOG.md file with release notes"
    gh_config = get_gh_config()
    tags = get_tags()
    changelog_title = "# Release notes"
    reports = []
    for from_tag, to in zip(tags[:-1], tags[1:]):
        from_tag_adj = from_tag.split(" / ")[0]  # adjusted for potential multiple tags for one commit
        to_tag_adj = to.split(" / ")[0]  # adjusted for potential multiple tags for one commit
        commit_msgs = get_commit_msgs(from_tag=from_tag_adj, to=to_tag_adj)
        reports.append(release_report(report_title=f"## {to}", commit_msgs=commit_msgs, gh_config=gh_config))
    changelog = changelog_title + "\n\n" + "\n\n".join(reports[::-1])
    with open("CHANGELOG.md", "w") as f:
        f.write(changelog)