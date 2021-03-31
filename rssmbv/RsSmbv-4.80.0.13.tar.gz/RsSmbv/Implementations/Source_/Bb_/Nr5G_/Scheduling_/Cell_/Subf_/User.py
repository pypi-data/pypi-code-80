from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 346 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: AvailableUser, default value after init: AvailableUser.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_availableUser_get', 'repcap_availableUser_set', repcap.AvailableUser.Nr0)

	def repcap_availableUser_set(self, enum_value: repcap.AvailableUser) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AvailableUser.Default
		Default value after init: AvailableUser.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_availableUser_get(self) -> repcap.AvailableUser:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def bwPart(self):
		"""bwPart commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_bwPart'):
			from .User_.BwPart import BwPart
			self._bwPart = BwPart(self._core, self._base)
		return self._bwPart

	@property
	def nbwParts(self):
		"""nbwParts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nbwParts'):
			from .User_.NbwParts import NbwParts
			self._nbwParts = NbwParts(self._core, self._base)
		return self._nbwParts

	def clone(self) -> 'User':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = User(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
