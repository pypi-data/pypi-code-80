from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.Utilities import trim_str_response
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 6 total commands, 1 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	@property
	def hddStreaming(self):
		"""hddStreaming commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_hddStreaming'):
			from .Data_.HddStreaming import HddStreaming
			self._hddStreaming = HddStreaming(self._core, self._base)
		return self._hddStreaming

	def get_dselect(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:SIRius:DATA:DSELect \n
		Snippet: value: str = driver.source.bb.sirius.data.get_dselect() \n
		No command help available \n
			:return: dselect: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:SIRius:DATA:DSELect?')
		return trim_str_response(response)

	def set_dselect(self, dselect: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:SIRius:DATA:DSELect \n
		Snippet: driver.source.bb.sirius.data.set_dselect(dselect = '1') \n
		No command help available \n
			:param dselect: No help available
		"""
		param = Conversions.value_to_quoted_str(dselect)
		self._core.io.write(f'SOURce<HwInstance>:BB:SIRius:DATA:DSELect {param}')

	def get_edate(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:SIRius:DATA:EDATe \n
		Snippet: value: str = driver.source.bb.sirius.data.get_edate() \n
		No command help available \n
			:return: edate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:SIRius:DATA:EDATe?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pattern: List[str]: No parameter help available
			- Bit_Count: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bit_Count: int = None

	def get_pattern(self) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:SIRius:DATA:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.sirius.data.get_pattern() \n
		No command help available \n
			:return: structure: for return value, see the help for PatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:SIRius:DATA:PATTern?', self.__class__.PatternStruct())

	def set_pattern(self, value: PatternStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:SIRius:DATA:PATTern \n
		Snippet: driver.source.bb.sirius.data.set_pattern(value = PatternStruct()) \n
		No command help available \n
			:param value: see the help for PatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:SIRius:DATA:PATTern', value)

	# noinspection PyTypeChecker
	def get_value(self) -> enums.DataSour:
		"""SCPI: [SOURce<HW>]:BB:SIRius:DATA \n
		Snippet: value: enums.DataSour = driver.source.bb.sirius.data.get_value() \n
		No command help available \n
			:return: data: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:SIRius:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.DataSour)

	def set_value(self, data: enums.DataSour) -> None:
		"""SCPI: [SOURce<HW>]:BB:SIRius:DATA \n
		Snippet: driver.source.bb.sirius.data.set_value(data = enums.DataSour.DLISt) \n
		No command help available \n
			:param data: No help available
		"""
		param = Conversions.enum_scalar_to_str(data, enums.DataSour)
		self._core.io.write(f'SOURce<HwInstance>:BB:SIRius:DATA {param}')

	def clone(self) -> 'Data':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Data(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
