# This file is part of Sympathy for Data.
# Copyright (c) 2020 Combine Control Systems AB
#
# Sympathy for Data is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Sympathy for Data is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sympathy for Data.  If not, see <http://www.gnu.org/licenses/>.
import keyring

from Qt import QtCore, QtWidgets, QtGui

from . import settings
from . import messages
from .. platform import widget_library as sywidgets
from .. platform.editors import credentials as editor_credentials
from .. platform import exceptions
from .. utils import credentials as utils_credentials
from . interfaces.messages_window import MessageItemRoles as MsgRoles
from . interfaces.messages_window import DetailsWidget
from . interfaces.preferences import PreferenceSectionWidget
from . widgets import settings_widgets as setwidgets
from .. utils import log


core_logger = log.get_logger('core')


class Secret:
    def __init__(self, secret: str, in_sync: bool):
        self._secret = secret
        self._in_sync = False

    @property
    def value(self):
        return self._secret

    @value.setter
    def value(self, value):
        self._secret = value
        self._in_sync = False

    def save(self, service, username):
        if not self._in_sync:
            try:
                keyring.set_password(
                    service, username, self._secret)
                self._in_sync = True
            except Exception as e:
                core_logger.info('Failed to save credential: %s', e)

    def load(self, service, username):
        if not self._in_sync:
            try:
                self._secret = keyring.get_password(service, username)
                self._in_sync = True
            except Exception as e:
                core_logger.info('Failed to load credential: %s', e)

    def delete(self, service, username):
        try:
            keyring.delete_password(service, username)
        except Exception as e:
            core_logger.info('Failed to delete credential: %s', e)
        self._in_sync = False


class SecretCredential:
    type: str = 'secret'

    def __init__(self, name: str, secret: str = '', in_sync: bool = False):
        self._name = name
        self._secret = Secret(secret, in_sync)

    def _store_service(self):
        return 'Sympathy for Data Secret'

    @property
    def key(self):
        return (self.type, self._name)

    @property
    def name(self):
        return self._name

    @property
    def label(self):
        return self.name

    @property
    def secret(self):
        return self._secret.value

    @classmethod
    def label_key(cls, label):
        return (cls.type, label)

    def save(self):
        self._secret.save(self._store_service(), self._name)

    def load(self):
        self._secret.load(self._store_service(), self._name)

    def delete(self):
        self._secret.delete(self._store_service(), self._name)

    def to_dict(self, get_secret=True):
        res = {'type': self.type,
               'name': self._name,
               'secret': self._secret.value}
        if not get_secret:
            res.pop('secret')
        return res

    @classmethod
    def validate_name(cls, name):
        return utils_credentials.validate_secret_name(name)

    def __eq__(self, other):
        return (self.type == other.type and
                self.name == other.name and
                self.secret == other.secret)

    def __ne__(self, other):
        return not self.__eq__(other)


class LoginCredential:
    type: str = 'login'
    in_sync: bool = False

    def __init__(self, resource: str, username: str, password: str = None,
                 in_sync: bool = False):
        self._resource = resource
        self.username = username
        self._password = Secret(password, in_sync)

    def _store_service(self):
        return f'Sympathy for Data Login: {self._resource}'

    @property
    def key(self):
        return (self.type, self.resource)

    @property
    def label(self):
        return self.resource

    @property
    def resource(self):
        return self._resource

    @property
    def password(self):
        return self._password.value

    @classmethod
    def label_key(cls, label):
        return (cls.type, label)

    def save(self):
        self._password.save(self._store_service(), self.username)

    def load(self):
        self._password.load(self._store_service(), self.username)

    def delete(self):
        self._password.delete(self._store_service(), self.username)

    def to_dict(self, get_secret=True):
        res = {
            'type': self.type,
            'resource': self._resource,
            'username': self.username,
            'password': self.password,
        }
        if not get_secret:
            res.pop('password')
        return res

    def __eq__(self, other):
        return (self.type == other.type and
                self.resource == other.resource and
                self.username == other.username and
                self.password == other.password)

    def __ne__(self, other):
        return not self.__eq__(other)


class SecretsMissingMessage(messages.ResultMessage):
    _type = 'secrets'

    def __init__(self, *, resource=None, brief=None, details=None, **kwargs):
        self._resource = resource
        brief = 'Missing Secret Credentials'
        super().__init__(brief=brief, **kwargs)

    def resource(self):
        return self._resource


class SecretsMissingMessageBuilder(messages.ErrorResultMessageBuilder):
    def build(self, *, error, **kwargs):
        return SecretsMissingMessage(resource=error.resource, **kwargs)


messages.register_error_result_message_builder(
    exceptions.SySecretCredentialError, SecretsMissingMessageBuilder())


class LoginMissingMessage(messages.ResultMessage):
    _type = 'login'

    def __init__(self, *, resource=None, brief=None, details=None, **kwargs):
        self._resource = resource
        brief = 'Missing Login Credentials'
        super().__init__(brief=brief, **kwargs)

    def resource(self):
        return self._resource


class LoginMissingMessageBuilder(messages.ErrorResultMessageBuilder):
    def build(self, *, error, **kwargs):
        return LoginMissingMessage(resource=error.resource, **kwargs)


messages.register_error_result_message_builder(
    exceptions.SyLoginCredentialError, LoginMissingMessageBuilder())


class SecretsMessageDetails(DetailsWidget):
    _type = 'secrets'
    _save_text = 'Save New Secrets'

    def __init__(self, font, parent=None):
        super().__init__(parent=parent)
        layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()

        self._label = QtWidgets.QLabel()
        self._credentials_layout = None
        self._edit_secrets_widget = editor_credentials.NullCredentialsWidget()
        self._create_button = QtWidgets.QPushButton(self._save_text)

        layout.addWidget(self._label)

        button_layout.addWidget(self._create_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        layout.addStretch()

        self.setLayout(layout)
        self._resource = None

        self._create_button.clicked.connect(
            self._handle_create_button_clicked)

    def _is_denied(self):
        credential_action = settings.instance()['credential_action']
        return credential_action == settings.credential_action_deny

    def type(self):
        assert self.type
        return self._type

    def _text(self, item):
        message = item.data(MsgRoles.message)
        brief = message.brief()
        details = message.details()

        res = ''
        if brief and details:
            res = '\n\n'.join([brief, details])
        elif brief:
            res = brief
        elif details:
            res = details

        return res

    def _editor_cls(self):
        return editor_credentials.EditSecretsWidget

    def _replace_edit_secrets_widget(self, widget):
        self._old_edit_secrets_widget = self._edit_secrets_widget
        self.layout().removeWidget(self._old_edit_secrets_widget)
        self._old_edit_secrets_widget.deleteLater()
        self._edit_secrets_widget = widget
        self.layout().insertWidget(1, self._edit_secrets_widget)

    def clear(self):
        super().clear()
        self._resource = None
        self._secrets = {}
        self._replace_edit_secrets_widget(
            editor_credentials.NullCredentialsWidget())

    def update_data(self, item):
        self.clear()
        self._item = item
        self._resource = item.data(MsgRoles.message).resource()
        item_text = self._text(item)
        self._label.setText(item_text)
        item.setData(MsgRoles.text, item_text)

        self._secrets = {}

        if self._resource:
            if self._is_denied():
                self._replace_edit_secrets_widget(
                    editor_credentials.DenyCredentialsWidget(self._resource))
            else:
                self._secrets = instance().request_resource(
                    self._resource, self._type)[1]
                self._replace_edit_secrets_widget(
                    self._editor_cls()(self._resource, self._secrets))

        self._create_button.setEnabled(
            self._resource is not None and bool(self._secrets))

    def _handle_create_button_clicked(self):
        for name, secret in self._edit_secrets_widget.secrets().items():
            if self._secrets[name] != secret:
                self._secrets[secret] = secret
                credential = SecretCredential(name, secret)
                instance().set_credential(credential.key, credential)
        self._remove()


class LoginMessageDetails(SecretsMessageDetails):
    _type = 'login'
    _save_text = 'Save New Login'

    def _editor_cls(self):
        return editor_credentials.EditLoginWidget

    def _handle_create_button_clicked(self):
        secrets = self._edit_secrets_widget.secrets()
        credential = LoginCredential(
            self._resource,
            secrets['username'],
            secrets['password'])
        instance().set_credential(credential.key, credential)
        self._remove()


class CredentialManager(QtCore.QObject):
    _settings_key = settings.credential_array_key

    def __init__(self):
        self._encryption = None
        self._store = {}
        self._load_settings()

    def keys(self):
        return list(self._store.keys())

    def __contains__(self, key):
        return key in self._store

    def _encode_credential(self, credential_dict):
        return dict(credential_dict)

    def _decode_credential(self, credential_dict):
        return dict(credential_dict)

    def _get_stored(self, key):
        raise self._store[key]

    def get_credential(self, key, get_secret=True):
        # settings_val = self._get_stored(key)
        # Will raise KeyError if not in store.
        credential = self._store[key]
        if get_secret:
            credential.load()
        return credential

    def _store_settings(self):
        settings.instance()[self._settings_key] = [
            credential.to_dict(get_secret=False)
            for credential in self._store.values()]

    def _load_settings(self):
        self._store.clear()
        data = settings.instance()[self._settings_key]

        for stored in data:
            if 'type' in stored:
                type = stored['type']
                if type == 'secret':
                    name = stored['name']
                    self._store[(type, name)] = SecretCredential(
                        name, in_sync=True)
                elif type == 'login':
                    resource = stored['resource']
                    username = stored['username']
                    self._store[(type, resource)] = LoginCredential(
                        resource, username, in_sync=True)

    def _set_stored(self, key, value):
        self._store[key] = value
        self._store_settings()

    def set_credential(self, key, credential):
        stored = self._store.get(key)
        if not (stored and stored == credential):
            # Do not replace and saved existing.
            credential.save()
            self._set_stored(key, credential)

    def _remove_stored(self, key):
        self._store.pop(key, None)
        self._store_settings()

    def remove_credential(self, key, credential=None, remove_secret=True):
        if remove_secret:
            try:
                if credential is None:
                    credential = self.get_credential(key, get_secret=True)
                credential.delete()
            except KeyError:
                pass
        self._remove_stored(key)

    def _parse_secrets(self, resource):
        return list(utils_credentials.parse_secrets(resource))

    def resource_names(self, resource):
        return [m.group(1) for m in self._parse_secrets(resource)]

    def request_resource(self, resource: str, mode: str) -> dict:
        """
        Returns all variables found in resource with their corresponding
        values. None in place of missing variables.
        """
        credential_action = settings.instance()['credential_action']
        res = {}
        deny = credential_action == settings.credential_action_deny
        ok = not deny
        utils_credentials.validate_mode(mode)

        if mode == utils_credentials.login_mode.name:
            res = dict.fromkeys(['username', 'password'])
            if not deny:
                try:
                    credential = instance().get_credential(
                        LoginCredential.label_key(resource), get_secret=True)
                except KeyError:
                    res['username'] = None
                    res['password'] = None
                else:
                    res['username'] = credential.username
                    res['password'] = credential.password
        elif mode == utils_credentials.secrets_mode.name:
            names = instance().resource_names(resource) or []
            res = dict.fromkeys(names)
            if not deny:
                for name in names:
                    key = SecretCredential.label_key(name)
                    if key in self:
                        credential = self.get_credential(key, get_secret=True)
                        res[name] = credential.secret
                    else:
                        res[name] = None
        return ok, res

    def edit_resource(self, resource: str, mode: str, secrets: dict) -> dict:
        """
        Set credentials for resource according to provided secrets.
        Returns all variables set and None in place of missing variables.
        """
        credential_action = settings.instance()['credential_action']
        res = {}
        deny = credential_action == settings.credential_action_deny
        ok = not deny
        utils_credentials.validate_mode(mode)
        secrets = secrets or {}

        if mode == utils_credentials.login_mode.name:
            res = dict.fromkeys(['username', 'password'])
            if not deny:
                credential = LoginCredential(
                    resource,
                    secrets['username'],
                    secrets['password'])

                instance().set_credential(credential.key, credential)

                res['username'] = credential.username
                res['password'] = credential.password

        elif mode == utils_credentials.secrets_mode.name:
            names = instance().resource_names(resource) or []
            res = dict.fromkeys(names)
            if not deny:
                for k, v in secrets.items():
                    credential = SecretCredential(k, v)
                    instance().set_credential(credential.key, credential)
                    res[credential.name] = credential.secret
        return ok, res


_instance = CredentialManager()


def instance():
    global _instance
    return _instance


def _credentials_denied_message(node, resource):
    level = messages.Levels.error
    brief = (
        f'Denied credential request for resource: {resource}\n\n'
        'To allow use of credentials, '
        'open:\n  Preferences -> Credentials, and change '
        'When Requested to Allow.')
    return messages.NodeMessage(
        id=(0, resource, node.full_uuid), node=node, level=level,
        brief=brief)


def login_credentials_error_message(node, resource):
    level = messages.Levels.error
    credential_action = settings.instance()['credential_action']
    if credential_action == settings.credential_action_deny:
        res = _credentials_denied_message(node, resource)
    else:
        res = messages.LoginMissingMessage(
            id=(1, resource, node.full_uuid), node=node, resource=resource,
            level=level)
    return res


def secret_credentials_error_message(node, resource):
    level = messages.Levels.error
    credential_action = settings.instance()['credential_action']
    if credential_action == settings.credential_action_deny:
        res = _credentials_denied_message(node, resource)
    else:
        res = messages.SecretsMissingMessage(
            id=(1, resource, node.full_uuid), node=node, resource=resource,
            level=level)
    return res


def create_right_stretch_layout(widget):
    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(widget)
    layout.addStretch()
    return layout


class NewLoginWidget(QtWidgets.QWidget):

    create = QtCore.Signal(LoginCredential)
    cancel = QtCore.Signal()
    type_changed = QtCore.Signal(str)

    type = 'login'

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = sywidgets.FormLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self._type_widget = TypeWidget(self.type)

        self._ok_button = button_box.button(QtWidgets.QDialogButtonBox.Ok)
        self._ok_button.setText("Create")
        button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText("Cancel")

        self._resource_widget = QtWidgets.QLineEdit()
        self._resource_widget.setToolTip(
            'Resource to login to with username and password')
        self._username_widget = editor_credentials.UsernameWidget('')
        self._password_widget = editor_credentials.PasswordWidget('')

        self._ok_button.setEnabled(False)

        layout.addRow('Type', self._type_widget)
        layout.addRow('Resource', self._resource_widget)
        layout.addRow('Username', self._username_widget)
        layout.addRow('Password', self._password_widget)
        layout.addRow(button_box)

        self.setLayout(layout)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        self._resource_widget.textChanged.connect(
            self._handle_resource_changed)
        self._type_widget.type_changed.connect(self.type_changed)

    def clear(self):
        self._resource_widget.setText('')
        self._username_widget.setText('')
        self._password_widget.setText('')

    def accept(self):
        credential = LoginCredential(
            self._resource_widget.text(),
            self._username_widget.get_value(),
            self._password_widget.get_value())
        self.create.emit(credential)

    def reject(self):
        self.cancel.emit()

    def _handle_resource_changed(self, resource):
        ok = True
        tooltip = ''
        if ok:
            keys = self.parentWidget().parentWidget().keys()
            ok = LoginCredential.label_key(resource) not in keys
            if not ok:
                tooltip = 'Resource already exists'
        else:
            tooltip = 'Invalid resource'
        self._ok_button.setToolTip(tooltip)
        self._ok_button.setEnabled(ok)


class ExistingLoginWidget(QtWidgets.QWidget):

    credential_changed = QtCore.Signal(LoginCredential, bool)
    remove = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = sywidgets.FormLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        label = QtWidgets.QLabel('Existing Login')

        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Cancel)
        button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText("Remove")

        self._resource_widget = editor_credentials.ResourceWidget('')
        self._resource_widget.setToolTip('Resource to use the password for')
        self._username_widget = editor_credentials.UsernameWidget('')
        self._password_widget = editor_credentials.PasswordWidget('')

        layout.addRow(label)

        layout.addRow('Resource', self._resource_widget)
        layout.addRow('Username', self._username_widget)
        layout.addRow('Password', self._password_widget)
        layout.addRow(button_box)
        self.setLayout(layout)

        self._username_widget.value_edited.connect(
            self._handle_username_changed)
        self._password_widget.value_edited.connect(
            self._handle_password_changed)
        button_box.rejected.connect(self.remove)

    def _handle_username_changed(self):
        self._handle_changed(False)

    def _handle_password_changed(self):
        self._handle_changed(True)

    def _handle_changed(self, secret_changed):
        credential = LoginCredential(
            self._resource_widget.text(),
            self._username_widget.text(),
            self._password_widget.get_value())
        self.credential_changed.emit(credential, secret_changed)

    def setup(self, credential):
        self._resource_widget.setText(credential.resource)
        self._username_widget.setText(credential.username)
        self._password_widget.from_dict(credential.to_dict())

    def clear(self):
        self._resource_widget.setText('')
        self._username_widget.setText('')
        self._password_widget.clear()


class TypeWidget(QtWidgets.QComboBox):
    type_changed = QtCore.Signal(str)
    _types = ['Login', 'Secret']

    def __init__(self, type, parent=None):
        self._type = type.title()
        super().__init__(parent=parent)
        self.addItems(self._types)
        self.currentTextChanged.connect(self._handle_type_changed)
        self.clear()

    def clear(self):
        self.currentTextChanged.disconnect(self._handle_type_changed)
        self.setCurrentText(self._type.title())
        self.currentTextChanged.connect(self._handle_type_changed)

    def _handle_type_changed(self, text):
        self.type_changed.emit(text.lower())
        self.clear()


class NewSecretWidget(QtWidgets.QWidget):

    create = QtCore.Signal(SecretCredential)
    cancel = QtCore.Signal()
    type_changed = QtCore.Signal(str)

    type = 'secret'

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = sywidgets.FormLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self._type_widget = TypeWidget(self.type)

        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self._ok_button = button_box.button(QtWidgets.QDialogButtonBox.Ok)
        self._ok_button.setText("Create")
        button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText("Cancel")

        self._name_widget = QtWidgets.QLineEdit()
        self._name_widget.setToolTip('Name to use the secret for')
        self._secret_widget = editor_credentials.SecretWidget('')

        self._ok_button.setEnabled(False)

        layout.addRow('Type', self._type_widget)
        layout.addRow('Name', self._name_widget)
        layout.addRow('Secret', self._secret_widget)
        layout.addRow(button_box)

        self.setLayout(layout)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        self._name_widget.textChanged.connect(self._handle_name_changed)
        self._type_widget.type_changed.connect(self.type_changed)

    def clear(self):
        self._name_widget.setText('')
        self._secret_widget.setText('')
        self._type_widget.clear()

    def accept(self):
        credential = SecretCredential(
            self._name_widget.text(), self._secret_widget.get_value())
        self.create.emit(credential)

    def reject(self):
        self.cancel.emit()

    def _handle_name_changed(self, name):
        ok = SecretCredential.validate_name(name)
        tooltip = ''
        if ok:
            keys = self.parentWidget().parentWidget().keys()
            ok = SecretCredential.label_key(name) not in keys
            if not ok:
                tooltip = 'Name already exists'
        else:
            tooltip = 'Invalid name'
        self._ok_button.setToolTip(tooltip)
        self._ok_button.setEnabled(ok)


class ExistingSecretWidget(QtWidgets.QWidget):

    credential_changed = QtCore.Signal(SecretCredential, bool)
    remove = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = sywidgets.FormLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        label = QtWidgets.QLabel('Existing Secret')

        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Cancel)
        button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText("Remove")

        self._name_widget = editor_credentials.ResourceWidget()
        self._name_widget.setToolTip('Name to use the secret for')
        self._secret_widget = editor_credentials.SecretWidget('')

        layout.addRow(label)

        layout.addRow('Name', self._name_widget)
        layout.addRow('Secret', self._secret_widget)
        layout.addRow(button_box)
        self.setLayout(layout)

        self._secret_widget.value_edited.connect(self._handle_secret_changed)
        button_box.rejected.connect(self.remove)

    def _handle_secret_changed(self):
        credential = SecretCredential(
            self._name_widget.text(),
            self._secret_widget.text())
        self.credential_changed.emit(credential, True)

    def setup(self, credential):
        self._name_widget.setText(credential.label)
        self._secret_widget.from_dict(credential.to_dict())

    def clear(self):
        self._name_widget.setText('')
        self._secret_widget.clear()


class CredentialSectionWidget(PreferenceSectionWidget):
    """docstring for PreferenceSectionWidget"""

    _name = 'Credentials'
    _apply_order = 10000

    _action_choice = settings.credential_action_choice

    key_role = QtCore.Qt.UserRole
    credential_role = QtCore.Qt.UserRole + 1
    dirty_role = QtCore.Qt.UserRole + 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._remove_set = set()

        layout = QtWidgets.QVBoxLayout()

        self._no_credential_widget = QtWidgets.QWidget()
        self._new_secret_widget = NewSecretWidget()
        self._existing_secret_widget = ExistingSecretWidget()
        self._new_login_widget = NewLoginWidget()
        self._existing_login_widget = ExistingLoginWidget()

        items_layout = QtWidgets.QHBoxLayout()
        select_layout = QtWidgets.QVBoxLayout()
        general_layout = self._layout = self._create_layout()
        credential_layout = QtWidgets.QVBoxLayout()

        self._credential_widget = QtWidgets.QStackedWidget()
        items_layout.addLayout(select_layout)
        items_layout.addLayout(credential_layout)

        self._credential_widget.addWidget(self._no_credential_widget)
        self._credential_widget.addWidget(self._new_secret_widget)
        self._credential_widget.addWidget(self._existing_secret_widget)
        self._credential_widget.addWidget(self._new_login_widget)
        self._credential_widget.addWidget(self._existing_login_widget)

        hline = sywidgets.HLine()
        credential_layout.addWidget(self._credential_widget)
        credential_layout.addStretch()
        items_layout.setContentsMargins(0, 0, 0, 0)

        layout.addLayout(general_layout)
        layout.addWidget(hline)
        layout.addLayout(items_layout)

        self._current_credential = None

        self._credential_filter = sywidgets.ClearButtonLineEdit(
            placeholder='Filter', clear_button=True)

        select_width = 200

        self._credential_filter.setMaximumWidth(select_width)

        self._credential_list = QtWidgets.QListView()
        self._credential_model = QtGui.QStandardItemModel()
        self._credential_list.setMaximumWidth(select_width)
        self._search_model = sywidgets.OrderedSearchFilterModel(
            self._credential_list)
        self._search_model.setSourceModel(self._credential_model)
        self._credential_list.setModel(self._search_model)

        self._create_button = QtWidgets.QPushButton('Create New Credential')
        self._create_button.setMaximumWidth(select_width)

        self._action_combo = setwidgets.StringComboBox(
            'credential_action', settings.credential_action_choice)

        general_layout.addRow('When requested', self._action_combo)
        select_layout.addWidget(self._credential_filter)
        select_layout.addWidget(self._credential_list)
        select_layout.addWidget(self._create_button)

        self.setLayout(layout)

        self._credential_list.selectionModel().selectionChanged.connect(
            self._handle_credential_list_index_changed)

        self._existing_secret_widget.remove.connect(self._handle_remove)
        self._existing_login_widget.remove.connect(self._handle_remove)

        self._create_button.clicked.connect(self._handle_create_button_clicked)

        self._new_secret_widget.create.connect(self._handle_create)
        self._new_login_widget.create.connect(self._handle_create)
        self._new_secret_widget.cancel.connect(self._handle_cancel)
        self._new_login_widget.cancel.connect(self._handle_cancel)
        self._new_secret_widget.type_changed.connect(self._handle_type_changed)
        self._new_login_widget.type_changed.connect(self._handle_type_changed)

        self._existing_secret_widget.credential_changed.connect(
            self._handle_credential_changed)

        self._existing_login_widget.credential_changed.connect(
            self._handle_credential_changed)

        self._credential_filter.textChanged.connect(
            self._handle_filter_text_changed)

    def _get_credential(self, item):
        credential = item.data(self.credential_role)
        if item.data(self.dirty_role) is False:
            credential.load()
        return credential

    def _remove_credential(self, item):
        key = item.data(self.key_role)
        self._remove_set.add(key)

    def _handle_remove(self):
        for item in self._selected_items():
            self._remove_credential(item)
            self._credential_model.takeRow(
                item.row())

    def _handle_create_button_clicked(self):
        self._credential_list.clearSelection()
        self._new_secret_widget.clear()
        self._new_login_widget.clear()
        self._credential_widget.setCurrentWidget(
            self._new_credential_widget('login'))
        self._create_button.setEnabled(False)

    def _handle_create(self, credential):
        self._create_button.setEnabled(True)
        item = self._create_item(credential.key, credential, dirty=True)
        self._add_item(item)

        self._credential_list.selectionModel().clear()

        self._credential_list.selectionModel().setCurrentIndex(
            self._search_model.mapFromSource(item.index()),
            QtCore.QItemSelectionModel.Select)

    def _handle_cancel(self):
        self._create_button.setEnabled(True)
        self._credential_widget.setCurrentWidget(self._no_credential_widget)

    def _new_credential_widget(self, text):
        if text == 'secret':
            return self._new_secret_widget
        elif text == 'login':
            return self._new_login_widget
        assert False, 'Unknown type'

    def _existing_credential_widget(self, text):
        if text == 'secret':
            return self._existing_secret_widget
        elif text == 'login':
            return self._existing_login_widget
        assert False, 'Unknown type'

    def _handle_type_changed(self, text):
        self._credential_widget.setCurrentWidget(
            self._new_credential_widget(text))

    def _handle_credential_list_index_changed(self, selected, deselected):
        new = None

        self._create_button.setEnabled(True)

        new_indices = selected.indexes()
        old_indices = deselected.indexes()

        if new_indices and new_indices[0].isValid():
            new = self._credential_model.itemFromIndex(
                self._search_model.mapToSource(new_indices[0]))

        if old_indices and old_indices[0].isValid():
            # old = self._credential_model.itemFromIndex(
            #     self._search_model.mapToSource(old_indices[0]))
            pass

        self._existing_secret_widget.clear()
        self._existing_login_widget.clear()

        selection = new is not None
        if selection:
            credential = self._get_credential(new)
            widget = self._existing_credential_widget(credential.type)
            self._credential_widget.setCurrentWidget(widget)
            widget.setup(credential)
        else:
            self._credential_widget.setCurrentWidget(
                self._no_credential_widget)

    def _handle_credential_changed(self, credential, changed):
        for item in self._selected_items():
            self._set_item_data(item, self.credential_role, credential)
            self._set_item_data(item, self.dirty_role, True)

    def _handle_filter_text_changed(self, text):
        self._search_model.set_filter(text)

    def _selected_items(self):
        return [self._credential_model.itemFromIndex(
            self._search_model.mapToSource(index))
                for index in self._credential_list.selectedIndexes()]

    def _set_item_data(self, item, role, data):
        item.setData(data, role)

    def _create_item(self, label, credential, dirty):
        item = QtGui.QStandardItem(credential.label)
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        self._set_item_data(item, self.key_role, credential.key)
        self._set_item_data(item, self.credential_role, credential)
        self._set_item_data(item, self.dirty_role, dirty)
        return item

    def _add_item(self, item):
        self._credential_model.appendRow(item)
        if not self._selected_items():
            if self._search_model.rowCount():
                self._credential_list.setCurrentIndex(
                    self._search_model.index(0, 0))

    def update_data(self):
        try:
            self._credential_list.selectionModel().selectionChanged.disconnect(
                self._handle_credential_list_index_changed)

            self._remove_set.clear()
            self._credential_model.clear()
            self._create_button.setEnabled(True)
            credentials_ = instance()

            for key in credentials_.keys():
                credential = credentials_.get_credential(key, get_secret=False)
                item = self._create_item(
                    credential.label, credential, dirty=False)
                self._add_item(item)

            self._credential_widget.setCurrentWidget(
                self._no_credential_widget)
            self._credential_list.clearSelection()
        finally:
            self._credential_list.selectionModel().selectionChanged.connect(
                self._handle_credential_list_index_changed)

    def keys(self):
        res = []
        for i in range(self._credential_model.rowCount()):
            item = self._credential_model.item(i)
            key = item.data(self.key_role)
            res.append(key)
        return res

    def save(self):
        self._action_combo.save()

        try:
            self._credential_list.selectionModel().selectionChanged.disconnect(
                self._handle_credential_list_index_changed)

            credentials_ = instance()
            for key in self._remove_set:
                credentials_.remove_credential(key)

            for i in range(self._credential_model.rowCount()):
                item = self._credential_model.item(i)
                if item.data(self.dirty_role):
                    credential = item.data(self.credential_role)
                    key = item.data(self.key_role)
                    instance().set_credential(key, credential)

            self._remove_set.clear()
            self._credential_model.clear()

        finally:
            self._credential_list.selectionModel().selectionChanged.connect(
                self._handle_credential_list_index_changed)
