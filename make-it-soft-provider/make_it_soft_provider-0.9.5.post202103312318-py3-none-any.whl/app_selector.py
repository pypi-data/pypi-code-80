# -*-coding:utf8 -*

from makeitsoft import utils
import PyInquirer
from PyInquirer import style_from_dict, Token
import gettext
_ = gettext.gettext


def language_question(conf, style):
    languages = utils.Dict2Obj(conf.languages)
    languages_list = list(languages.values.values())
    questions = [
        {
            'type': 'list',
            'name': 'default_language',
            'message': utils._('Choisissez votre langue par defaut :'),
            'default': languages.default,
            'choices': languages_list
        }
    ]
    selected_default_language = PyInquirer.prompt(questions, style=style)
    utils.change_language(selected_default_language['default_language'])
    return selected_default_language


def general_questions(conf, style):
    repositories = utils.Dict2Obj(conf.repositories)
    repositories_list = list(repositories.values.values())
    default = utils.Dict2Obj(conf.default)

    questions = [
        {
            'type': 'list',
            'name': 'repository',
            'message': utils._('Choisissez votre depot d\'image docker a utiliser pour l\'installation :'),
            'default': repositories.default,
            'choices': repositories_list
        },
        {
            'type': 'input',
            'name': 'domain',
            'message': utils._('Precisez le domain de destination de la solution :'),
            'default': default.domain
        },
        {
            'type': 'confirm',
            'name': 'is_access_direct',
            'message': utils._('Acces Direct par defaut ?'),
            'default': True
        },
        {
            'type': 'input',
            'name': 'admin_password',
            'message': utils._('Mot de passe de l\'administrateur :'),
            'default': default.admin_password
        },
        {
            'type': 'input',
            'name': 'current_ipaddr',
            'message': utils._('Adresse IP du serveur :'),
            'default': utils.get_server_ip_addr()
        }
    ]
    return PyInquirer.prompt(questions, style=style)


def selecting_feature(feature):
    apps = list(feature.apps.values())

    questions = {
        'type': 'checkbox',
        'name': feature.key,
        'message': feature.name + ': ',
        'choices': apps
    }
    return questions


def selecting_apps(conf, style):
    features = list(conf.library.values())
    questions = []

    for feature in features:
        questions.append(selecting_feature(utils.Dict2Obj(feature)))

    return PyInquirer.prompt(questions, style=style)


def retrieve_user_choices(conf, args):
    style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })

    language = language_question(conf, style)
    general = general_questions(conf, style)
    if 'repository' not in general:
        return
    selected_apps = selecting_apps(conf, style) if args.is_use_basic_catalog else dict()
    return {
        'default_language': language['default_language'],
        'repository': general['repository'],
        'domain': general['domain'],
        'admin_password': general['admin_password'],
        'is_access_direct': general['is_access_direct'],
        'current_ipaddr': general['current_ipaddr'],
        'features': selected_apps
    }


