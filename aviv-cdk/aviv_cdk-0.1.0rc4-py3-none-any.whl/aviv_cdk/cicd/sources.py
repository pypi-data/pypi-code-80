import logging
import typing

SourceRepositoryAttrs = typing.Dict[typing.Literal['owner', 'repo', 'branch'], str]
GitRepositoryInfo = typing.Dict[typing.Literal['url', 'branch'], str]

def git_repository_info() -> GitRepositoryInfo:
    import subprocess
    cmd = lambda input: subprocess.check_output(input, shell=True).decode('UTF-8').rstrip()
    url=cmd("git remote get-url origin")
    if url.endswith('.git'):
        url = url.replace('.git', '')

    return dict(
        url=url,
        branch=cmd("git branch --show-current")
    )


def github_url_split(url: str, branch: str='main') -> SourceRepositoryAttrs:
    """Splits a https github url to return a dict with:
    - owner     Github organization
    - repo      the git repository
    - branch    the branch

    Args:
        url (str): a https://github.com/your-org/myrepo
        branch (str, optional): [description]. Defaults to 'main'.

    Returns:
        dict: owner/repo/branch
    """
    repo_attrs = dict()
    valid = 'https://github.com/'
    if not url.startswith(valid):
        logging.error(f"Not an https Github URL: {url}")
        raise NotImplementedError(f"Must start with {valid}")

    # Cleanup URL, only keep `owner/repo[@branch]`
    url = url.replace(valid, '')
    if url.endswith('.git'):
        url = url.replace('.git', '')

    purl = url.split('/')
    repo_attrs['owner'] = purl[0]
    repo_attrs['repo'] = '/'.join(purl[1:])
    repo_attrs['branch'] = branch
    # If we have a specific branch
    if repo_attrs['repo'].find('@') > 0:
        prepo = repo_attrs['repo'].split('@')
        repo_attrs['repo'] = prepo[0]
        repo_attrs['branch'] = prepo[1]
    return repo_attrs
