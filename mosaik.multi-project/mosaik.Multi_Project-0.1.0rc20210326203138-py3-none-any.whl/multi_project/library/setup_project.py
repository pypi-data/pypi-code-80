import os
import shutil
import subprocess

from builtins import IOError

from mosaik_multi_project.multi_project.library.parse_config import \
    parse_simulator_config


def setup_project(
    project,
    *,
    operations,
    projects_path,
):
    alias, \
        branch, project_path, repo_path, repository, \
        venv_python_name, venv_python_path, \
        tox_environment_name, tox_python_path, tox_requirements_txt_file_path, \
        container_name, venv_requirements_txt_file_path = \
        parse_simulator_config(
            projects_path=projects_path,
            simulator=project,
        )

    if 'git_clone' in operations:
        print(f'[{alias}] Ensuring cloned repository ...')
        subprocess.Popen(
            args=f'git clone {repository} {repo_path}'
                 f''.split(),
            cwd=str(projects_path),
        ).wait()

    if 'git_remote' in operations:
        print(f'[{alias}] Ensuring correct remote ...')
        subprocess.Popen(
            args=f'git remote set-url origin {str(repository)}'
                 f''.split(),
            cwd=str(repo_path),
        ).wait()

    if 'git_fetch' in operations:
        print(f'[{alias}] Ensuring current repository ...')
        subprocess.Popen(
            args='git fetch origin'
                 ''.split(),
            cwd=str(repo_path),
        ).wait()

    if 'git_checkout' in operations:
        print(f'[{alias}] Ensuring correct branch ...')
        subprocess.Popen(
            args=f'git checkout {branch}'
                 f''.split(),
            cwd=str(repo_path),
        ).wait()

    if 'git_pull' in operations:
        print(f'[{alias}] Ensuring current working copy ...')
        subprocess.Popen(
            args='git pull '
                 '--ff-only '  # Avoid automatic merges
                 ''.split(),
            cwd=str(repo_path),
        ).wait()

    # print(venv_requirements_txt_file_path)
    # if venv_requirements_txt_file_path is None:
    #     print(f'[{alias}] Not a Python project, so stopping here.')
    #     return

    if 'init_remove' in operations:
        print(f'[{alias}] Ensuring namespace directory ...')
        try:
            os.remove(os.path.join(str(project_path), '__init__.py'))
        except IOError:
            # No such file is fine.
            pass

    if 'venv_remove' in operations:
        print(f'[{alias}] Removing old venv directory ...')
        try:
            shutil.rmtree(project_path / 'venv')
        except Exception:
            pass

    if 'venv_create' in operations:
        print(f'[{alias}] Creating new virtual environment ...')
        subprocess.Popen(
            args=f'{venv_python_name} -m venv '  # Yes, use global Python here
                 'venv '
                 ''.split(),
            cwd=str(project_path),
        ).wait()

    if 'venv_ensure_pip' in operations:
        print(f'[{alias}] Ensuring pip install ...')
        subprocess.Popen(
            args=f'{venv_python_path} -m ensurepip'
                 f''.split(),
            cwd=str(project_path),
        ).wait()

    if 'venv_upgrade_pip' in operations:
        print(f'[{alias}] Upgrading venv pip ...')
        subprocess.Popen(
            args=f'{venv_python_path} -m pip install --quiet --quiet --upgrade '
                 f'pip'
                 f''.split(),
            cwd=str(project_path),
        ).wait()

    if 'venv_install_pur' in operations:
        print(f'[{alias}] Ensuring current pur ...')
        subprocess.Popen(
            args=f'{venv_python_path} -m pip install --quiet --quiet --upgrade '
                 f'pur'
                 f''.split(),
            cwd=str(project_path),
        ).wait()

    if 'venv_pur' in operations:
        print(f'[{alias}] Upgrading venv requirements ...')
        subprocess.Popen(
            args=f'{venv_python_path} -m pur '
                 f'-r {venv_requirements_txt_file_path}'
                 f''.split(),
            cwd=str(project_path),
        ).wait()

    if 'venv_install' in operations:
        print(f'[{alias}] Installing venv requirements ...')
        subprocess.Popen(
            args=f'{venv_python_path} -m pip install --quiet --quiet --upgrade '
                 f'-r {project_path / venv_requirements_txt_file_path}'
                 f''.split(),
            cwd=str(project_path),
        ).wait()

    if 'venv_install_wheel' in operations:
        print(f'[{alias}] Installing wheel into venv ...')
        subprocess.Popen(
            args=f'{venv_python_path} -m pip install --quiet --quiet --upgrade '
                 f'wheel'
                 f''.split(),
            cwd=str(project_path),
        ).wait()

    if tox_python_path is None:
        print(f'[{alias}] No Tox required, so skipping.')
    else:
        if 'tox_remove' in operations:
            print(f'[{alias}] Removing old tox directory ...')
            try:
                shutil.rmtree(project_path / '.tox')
            except BaseException:
                pass

        if 'tox_create' in operations:
            print(f'[{alias}] Setting up tox environments ...')
            subprocess.Popen(
                args=f'{venv_python_path} -m tox '
                     f'-e {tox_environment_name} '
                     # f'--parallel all '
                     f'--notest '
                     f''.split(),
                cwd=str(project_path),
            ).wait()

        if 'tox_install_pur' in operations:
            print(f'[{alias}] Ensuring current pur ...')
            subprocess.Popen(
                args=f'{tox_python_path} -m pip '
                     'install --quiet --quiet --upgrade '
                     f'pur'
                     f''.split(),
                cwd=str(project_path),
            ).wait()

        if 'tox_pur' in operations:
            print(f'[{alias}] Updating tox requirements ...')
            subprocess.Popen(
                args=f'{tox_python_path} -m pur '
                     f'-r {venv_requirements_txt_file_path}'
                     f''.split(),
                cwd=str(project_path),
            ).wait()

        if 'tox_create' in operations:
            print(f'[{alias}] Testing new requirements and code ...')
            subprocess.Popen(
                args=f'{venv_python_path} -m tox '
                     f'-e {tox_environment_name} '
                     # f'--parallel all '
                     f'--notest '
                     f''.split(),
                cwd=str(project_path),
            ).wait()

    if container_name is None:
        print(f'[{alias}] No Docker container required, so skipping.')
    else:
        if 'docker_build' in operations:
            print(f'[{alias}] Building docker container image ...')
            subprocess.Popen(
                args=f'docker build --pull --tag {container_name}:latest .'
                     f''.split(),
                cwd=str(project_path),
            ).wait()

    # TODO Stage and commit upgraded requirements

    print(f'[{alias}] Done running the requested operations on this project.')
