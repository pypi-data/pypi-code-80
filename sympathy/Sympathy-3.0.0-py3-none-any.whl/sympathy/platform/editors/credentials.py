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
import Qt.QtCore as QtCore
import Qt.QtWidgets as QtWidgets
from sympathy.platform import widget_library as sywidgets


class PasswordLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setEchoMode(self.EchoMode.Password)


class LineValueMixin:
    def __init__(self, value=None, **kwargs):
        super().__init__(**kwargs)
        self.set_value(value)

    def get_value(self):
        return self.text()

    def set_value(self, value):
        self.setText(value)

    def clear(self):
        self.setText('')


class CredentialMixin(LineValueMixin):
    type = None

    def __init__(self, value=None, parent=None):
        super().__init__(parent=parent)

        self._reset = False
        if value is None:
            self.setPlaceholderText('Not set')
        elif value:
            self.set_value(value)

        self.textEdited.connect(self._handle_value_edited)

    def _handle_value_edited(self, value):
        if not self._reset:
            self.value_edited.emit(value)

    def clear(self):
        self.from_dict({self.type: ''})

    def to_dict(self):
        return {
            self.type: self.get_value(),
        }

    def from_dict(self, data):
        try:
            self._reset = True
            self.set_value(data[self.type])
        finally:
            self._reset = False


class ShowPasswordLineEdit(QtWidgets.QWidget):
    """
    Works as a QLineEdit for passwords with a button to show the text
    temporarily. The button state is cleared on setText for convenience since
    setText in all current uses means showing a new password. This could be
    made explicit if it causes problems.

    Implements the current required subset of QLineEdit interface. Add more
    operations when needed.
    """

    textEdited = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self._show_widget = sywidgets.ShowButton()
        self._show_widget.setFocusPolicy(QtCore.Qt.NoFocus)
        self._password_widget = PasswordLineEdit()
        layout.addWidget(self._password_widget)
        layout.addWidget(self._show_widget)
        self.setLayout(layout)
        self._show_widget.toggled.connect(self._handle_show_widget_toggled)
        self._password_widget.textEdited.connect(self.textEdited)

    def _handle_show_widget_toggled(self, checked=False):
        if checked:
            self._password_widget.setEchoMode(
                self._password_widget.EchoMode.Normal)
        else:
            self._password_widget.setEchoMode(
                self._password_widget.EchoMode.Password)

    def text(self):
        return self._password_widget.text()

    def setText(self, value):
        self._show_widget.setChecked(False)
        return self._password_widget.setText(value)

    def get_value(self):
        return self.text()

    def set_value(self, value):
        self.setText(value)

    def setPlaceholderText(self, text):
        self._password_widget.setPlaceholderText(text)


class SecretWidget(CredentialMixin, ShowPasswordLineEdit):
    type = 'secret'
    value_edited = QtCore.Signal(str)

    def __init__(self, value='', parent=None):
        super().__init__(value=value, parent=parent)


class UsernameWidget(CredentialMixin, QtWidgets.QLineEdit):
    type = 'username'
    value_edited = QtCore.Signal(str)

    def __init__(self, value='', parent=None):
        super().__init__(value=value, parent=parent)


class PasswordWidget(CredentialMixin, ShowPasswordLineEdit):
    type = 'password'
    value_edited = QtCore.Signal(str)

    def __init__(self, value='', parent=None):
        super().__init__(value=value, parent=parent)


class ResourceEditWidget(LineValueMixin, QtWidgets.QLineEdit):
    pass


class ResourceWidget(LineValueMixin, sywidgets.ReadOnlyLineEdit):
    pass


class NullCredentialsWidget(QtWidgets.QWidget):
    def secrets(self):
        return {}


class DenyCredentialsWidget(NullCredentialsWidget):

    def __init__(self, resource, parent=None):
        super().__init__(parent=parent)
        layout = sywidgets.FormLayout()
        self.setLayout(layout)
        deny_label = QtWidgets.QLabel(
            'Credential requests are denied by current settings')
        self.setToolTip(
            'Set to Allow in preferences to use Credentials')
        layout.addRow(deny_label)

        resource_widget = ResourceWidget(resource)
        layout.addRow('Resource', resource_widget)

    def secrets(self):
        return {}


class EditSecretsWidget(QtWidgets.QWidget):

    def __init__(self, resource, secrets, parent=None):
        super().__init__(parent=parent)

        layout = sywidgets.FormLayout()
        self.setLayout(layout)

        resource_widget = ResourceWidget(resource)
        layout.addRow('Resource', resource_widget)

        # button_box = QtWidgets.QDialogButtonBox()
        # button_layout = QtWidgets.QHBoxLayout()
        hline = sywidgets.HLine()
        layout.addRow(hline)

        self._secret_widgets = {}
        self._init_fields(layout, secrets)

    def _init_fields(self, layout, secrets):

        for k, v in secrets.items():
            widget = SecretWidget(v)
            self._secret_widgets[k] = widget
            layout.addRow(k, widget)

        if not secrets:
            layout.addRow(QtWidgets.QLabel("No secrets stored for this resource"))

    def secrets(self):
        return {k.lower(): v.get_value() for k, v in
                self._secret_widgets.items()}


class EditLoginWidget(EditSecretsWidget):

    def _init_fields(self, layout, secrets):
        self._password_widget = PasswordWidget(secrets['password'])
        self._username_widget = UsernameWidget(secrets['username'])

        layout.addRow('Username', self._username_widget)
        layout.addRow('Password', self._password_widget)

    def secrets(self):
        return {
            'username': self._username_widget.get_value(),
            'password': self._password_widget.get_value(),
        }


class EditSecretsDialog(QtWidgets.QDialog):
    _title = 'Edit Secrets'

    def __init__(self, resource, secrets, parent=None):
        super().__init__(parent=parent)
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle(self._title)
        self._edit_widget = self._editor_cls()(resource, secrets, parent=self)
        layout.addWidget(self._edit_widget)
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok |
            QtWidgets.QDialogButtonBox.Cancel)
        layout.addStretch()
        layout.addWidget(button_box)

        button_box.button(
            QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.accept)
        button_box.button(
            QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)

        self.setMinimumWidth(400)
        policy = QtWidgets.QSizePolicy()
        policy.setHorizontalStretch(1)
        policy.setHorizontalPolicy(QtWidgets.QSizePolicy.Preferred)
        policy.setVerticalPolicy(QtWidgets.QSizePolicy.Maximum)
        self.setSizePolicy(policy)

    def _editor_cls(self):
        return EditSecretsWidget

    def secrets(self):
        return self._edit_widget.secrets()


class EditLoginDialog(EditSecretsDialog):
    _title = 'Edit Login'

    def _editor_cls(self):
        return EditLoginWidget


def add_form_row(layout, label, widget):
    # layout.addRow(label, widget)
    label_widget = QtWidgets.QLabel(label)
    hlayout = QtWidgets.QHBoxLayout()
    hlayout.addWidget(label_widget)
    hlayout.addWidget(widget)
    hlayout.setStretchFactor(widget, 1)
    layout.addLayout(hlayout)
    return hlayout, label


def _form_layout():
    # layout = QtWidgets.QFormLayout()
    layout = QtWidgets.QVBoxLayout()
    return layout


def standard_button_box(dialog):
    box = QtWidgets.QDialogButtonBox()
    box.addButton(QtWidgets.QDialogButtonBox.Ok)
    box.addButton(QtWidgets.QDialogButtonBox.Cancel)
    box.accepted.connect(dialog.accept)
    box.rejected.connect(dialog.reject)
    return box
