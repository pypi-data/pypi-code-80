# -*-coding:utf8 -*

from makeitsoft import utils, logger, app_scaffolder, app_selector, service_operation
import os
import gettext
_ = gettext.gettext

def load_configuration(conf_file_path):
    return utils.Dict2Obj(utils.load_file(conf_file_path))


def welcome_message(conf):
    logger.success(utils._('Bienvenue sur le generateur < {} > version < {} > !!!').format(conf.name, conf.version),
                   show_preffix=False)
    logger.info(
        utils._('Cet utilitaire vous permettra de deployer suivant vos choix un pack de solutions d\'entreprise developpe par la societe {}').format(conf.powered_by), show_preffix=False)


def initialize(conf, args):
    if args.input:
        selection = utils.load_file(os.path.join(args.input))
        selection['features'] = selection['features'] if args.is_use_basic_catalog else dict()
        selection['current_ipaddr'] = selection['current_ipaddr'] if 'current_ipaddr' in selection and selection['current_ipaddr'] is not None else utils.get_server_ip_addr()
    else:
        selection = app_selector.retrieve_user_choices(conf, args)

    if args.is_use_basic_catalog and (selection is None or not selection['features']):
        return
    logger.info('Selection: {}'.format(selection))

    app_scaffolder.scaffold_apps(conf, selection)
    os.chmod(os.path.join(conf.output_dir, 'service.sh'), 0o755)

    if args.is_auto_start:
        logger.info(utils._('Demarrage de l\'instance MakeItSoft...'))
        service_operation.start(conf)
        logger.success(utils._('Demarrage de l\'instance MakeItSoft terminee'))
    else:
        logger.info(utils._('Pour demarrer les apps: ./service.sh start'))


def add_solution(conf, args):
    conf_general_path = os.path.join(conf.output_dir, 'conf.general.yml')
    if args.input_solution_archive is None:
        logger.error(utils._('Le parametre --input-solution-archive est obligatoire pour l\'operation <add_solution>'))
        return
    archive_path = os.path.join(args.input_solution_archive)
    if not os.path.exists(archive_path):
        logger.error(utils._('Aucune archive detectee au chemin: {}').format(archive_path))
        return
    if not os.path.exists(conf_general_path):
        logger.error(utils._('Aucune installation detectee dans le dossier: {}').format(conf_general_path))
        return
    conf_general = utils.load_file(os.path.join(conf_general_path))

    app_id = app_scaffolder.scaffold_add_solution_from_archive(conf.output_dir, conf_general, archive_path)
    if args.is_to_start_after_install:
        service_operation.start(conf, app_id)


def remove_solution(conf, args):
    conf_general_path = os.path.join(conf.output_dir, 'conf.general.yml')
    if args.solution_to_remove is None:
        logger.error(utils._('Le parametre --solution-to-remove est obligatoire pour l\'operation <remove_solution>'))
        return
    if not os.path.exists(conf_general_path):
        logger.error(utils._('Aucune installation detectee dans le dossier: {}').format(conf_general_path))
        return
    try:
        app_scaffolder.scaffold_remove_solution(conf, args.solution_to_remove, args.is_to_reset_before_install)
    except ValueError as err:
        logger.error(utils._(err))


def main(args):
    utils.change_language('en')
    file_dir = os.path.dirname(os.path.abspath(__file__))
    conf = load_configuration(os.path.join(file_dir, 'conf', 'business-solution.yml'))
    if args.destination:
        conf.output_dir = args.destination

    logger.info('Output Directory: {}'.format(conf.output_dir))
    welcome_message(conf)
    if args.operation == 'add_solution':
        add_solution(conf, args)
    elif args.operation == 'remove_solution':
        remove_solution(conf, args)
    else:
        initialize(conf, args)

    logger.success(utils._('Operation terminee !!!'))
    logger.info(utils._('Au revoir !!!'))