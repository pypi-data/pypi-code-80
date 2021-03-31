from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fall:
	"""Fall commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fall", core, parent)

	def get_time(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:FALL:TIME \n
		Snippet: value: float = driver.source.bb.pramp.ramp.fall.get_time() \n
		No command help available \n
			:return: falltime: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:FALL:TIME?')
		return Conversions.str_to_float(response)

	def set_time(self, falltime: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:FALL:TIME \n
		Snippet: driver.source.bb.pramp.ramp.fall.set_time(falltime = 1.0) \n
		No command help available \n
			:param falltime: No help available
		"""
		param = Conversions.decimal_value_to_str(falltime)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:RAMP:FALL:TIME {param}')
