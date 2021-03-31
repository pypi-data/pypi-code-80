# -*-coding:utf8 -*

from makeitsoft import utils, logger, service_operation
import shutil
from jinja2 import Environment, FileSystemLoader, Template
import os
import tarfile
import json
import gettext
_ = gettext.gettext

file_dir = os.path.dirname(os.path.abspath(__file__))


def copy_template_dir(conf, app):
    utils.copyDirectory(
        os.path.join(file_dir, 'templates', app),
        os.path.join(conf.output_dir, app)
    )


def scaffold_app_file(output_dir, variables, app_dir_name, pfilename):
    templates_dir = os.path.join(file_dir, 'templates')
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('{}/{}'.format(app_dir_name, pfilename))
    filename = os.path.join(output_dir, app_dir_name, pfilename)
    with open(filename, 'wb') as fh:
        fh.write(
            template.render(
                variables=variables
            ).encode('utf-8')
        )


def scaffold_app(output_dir, variables, app_dir_name):
    scaffold_app_file(output_dir, variables, app_dir_name, 'docker-compose.yml')


def scaffold_add_solution_from_archive(output_dir, conf_general, archive_path):
    # Creating /tmp dir
    tmp_dir_path = os.path.join('/tmp-makeitsoft')
    if not os.path.exists(tmp_dir_path):
        os.makedirs(tmp_dir_path)

    # Extract archive
    tf = tarfile.open(archive_path)
    tf.extractall(tmp_dir_path)

    # Read conf from archive
    conf_app_to_add_path = os.path.join(tmp_dir_path, 'conf.yml')
    env = Environment(loader=FileSystemLoader(tmp_dir_path))
    template = env.get_template('conf.yml')
    with open(conf_app_to_add_path, 'wb') as fh:
        fh.write(
            template.render(
                conf_general=conf_general
            ).encode('utf-8')
        )
    conf_app_to_add = utils.load_file(conf_app_to_add_path)

    # Scaffolding the new app
    os.mkdir(os.path.join(output_dir, conf_app_to_add['id']))
    conf_app_to_add['ip'] = conf_general['ip']
    template = env.get_template('docker-compose.yml')
    filename = os.path.join(output_dir, conf_app_to_add['id'], 'docker-compose.yml')
    with open(filename, 'wb') as fh:
        fh.write(
            template.render(
                variables=conf_app_to_add
            ).encode('utf-8')
        )
    # Copying logo file
    shutil.copyfile(
        os.path.join(tmp_dir_path, '{}.png'.format(conf_app_to_add['id'])),
        os.path.join(output_dir, 'portail-solutions', 'apps', 'backend', 'logos', '{}.png'.format(conf_app_to_add['id']))
    )

    # Modification des fichiers config.json
    add_solution_to_config_file(conf_app_to_add, output_dir, 'config.json')

    add_solution_to_config_bat_file(output_dir, conf_app_to_add['id'])
    add_dns_entry_for_the_new_solution(conf_general, output_dir, conf_app_to_add['id'])

    return conf_app_to_add['id']


def scaffold_remove_solution(conf, solution_to_remove, is_to_reset_before_install):
    # Modification des fichiers config.json
    remove_solution_from_config_file(conf.output_dir, 'config.json', solution_to_remove)

    if is_to_reset_before_install:
       # Suppression et purge des conteneurs
       service_operation.reset(conf, solution_to_remove)

    #add_solution_to_config_bat_file(conf.output_dir, solution_to_remove)

    # Delete app to remove
    shutil.rmtree(os.path.join(conf.output_dir, solution_to_remove), ignore_errors=True)


def add_solution_to_config_file(conf_app_to_add_final, output_dir, config_file):
    filename = os.path.join(output_dir, 'portail-solutions', 'apps', 'backend', 'config', config_file)
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        data['apps'].append({
            "id": conf_app_to_add_final['id'],
            "url": conf_app_to_add_final['url'],
            "url_direct": conf_app_to_add_final['url_direct'],
            "label_fr": conf_app_to_add_final['label_fr'],
            "label_en": conf_app_to_add_final['label_en'],
            "version": conf_app_to_add_final['version'],
            "manuel": conf_app_to_add_final['manuel'],
            "aide": conf_app_to_add_final['aide'],
            "description_fr": conf_app_to_add_final['description_fr'],
            "description_en": conf_app_to_add_final['description_en']
        })
    os.remove(filename)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def remove_solution_from_config_file(output_dir, config_file, solution_to_remove):
    filename = os.path.join(output_dir, 'portail-solutions', 'apps', 'backend', 'config', config_file)
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        solution_to_remove_index = find_solution_index(data['apps'], solution_to_remove)
        del data['apps'][solution_to_remove_index]
    os.remove(filename)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def find_solution_index(apps_list, solution_to_remove):
    pos = -1
    # Iterate over list items by index pos
    for i in range(len(apps_list)):
        # Check if items matches the given element
        if apps_list[i]['id'] == solution_to_remove:
            pos = i
            break
    if pos == -1:
        raise ValueError('La solution {} n\'est pas installée'.format(solution_to_remove))
    return pos


def add_solution_to_config_bat_file(output_dir, new_app_name):
    file_path = os.path.join(output_dir, 'portail-solutions', 'apps', 'frontend', 'config', 'domain-config.bat')
    if os.path.exists(file_path):
       f = open(file_path, "r")
       contents = f.readlines()
       f.close()
       contents[1] = '{}{} '.format(contents[1], new_app_name)
       f = open(file_path, "w")
       f.writelines(contents)
       f.close()


def add_dns_entry_for_the_new_solution(conf_general, output_dir, new_app_name):
    file_path = os.path.join(output_dir, 'portail-solutions', 'bind', 'bind', 'lib', 'make-it-soft.local.hosts')
    if os.path.exists(file_path):
        with open(file_path, 'a') as file:
            file.write('{}.{}.	IN	A	{}\n'.format(new_app_name, conf_general['domain'], conf_general['ip']))


def scaffold_portal(conf, variables):
    copy_template_dir(conf, 'portail-solutions')
    scaffold_app_file(conf.output_dir, variables, 'portail-solutions', 'docker-compose.yml')
    scaffold_app_file(conf.output_dir, variables, os.path.join('portail-solutions/haproxy'), 'haproxy.cfg')
    scaffold_app_file(conf.output_dir, variables, os.path.join('portail-solutions/haproxy'), 'Dockerfile')
    scaffold_app_file(conf.output_dir, variables, os.path.join('portail-solutions/apps/backend/config'), 'config.json')
    scaffold_app_file(conf.output_dir, variables, os.path.join('portail-solutions/apps/frontend/config'), 'domain-config.bat')
    scaffold_app_file(conf.output_dir, variables, os.path.join('portail-solutions/apps/frontend/lang'), 'lang-available.json')
    scaffold_app_file(conf.output_dir, variables, os.path.join('portail-solutions/apps/frontend/lang'), 'lang-en.json')
    scaffold_app_file(conf.output_dir, variables, os.path.join('portail-solutions/apps/frontend/lang'), 'lang-fr.json')
    scaffold_app_file(conf.output_dir, variables, os.path.join('portail-solutions/apps/frontend'), 'endpoint.json')
    scaffold_app_file(conf.output_dir, variables, os.path.join('portail-solutions/bind/bind/etc'), 'named.conf.local')
    scaffold_app_file(conf.output_dir, variables, os.path.join('portail-solutions/bind/bind/lib'), 'make-it-soft.local.hosts')
    scaffold_app_file(conf.output_dir, variables, os.path.join('.'), 'service.sh')
    scaffold_app_file(conf.output_dir, variables, os.path.join('.'), 'conf.general.yml')


def scaffold_apps(conf, selection):
    logger.info('Adresse IP : {}'.format(selection['current_ipaddr']))

    variables = {
        'output_dir': conf.output_dir,
        'ip': selection['current_ipaddr'],
        'default_language': selection['default_language'],
        'depot': selection['repository'],
        'domain': selection['domain'],
        'admin_password': selection['admin_password'],
        'is_access_direct': selection['is_access_direct'],
        'library': conf.library,
        'portal': conf.portal
    }

    selected_apps_details = []

    for feature in selection['features']:
        if selection['features'][feature] is not None:
            for app in selection['features'][feature]:
                copy_template_dir(conf, app)
                scaffold_app(conf.output_dir, variables, app)
                app_detail = conf.portal['available_apps'][app]
                app_detail['url'] = Template(app_detail['url']).render(variables=variables)
                app_detail['url_direct'] = Template(app_detail['url_direct']).render(variables=variables)
                selected_apps_details.append(app_detail)

    variables['selected_apps_details'] = selected_apps_details
    scaffold_portal(conf, variables)
