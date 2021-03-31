from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Psweep:
	"""Psweep commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("psweep", core, parent)

	def get_continuous(self) -> bool:
		"""SCPI: INITiate<HW>:PSWeep:CONTinuous \n
		Snippet: value: bool = driver.initiate.psweep.get_continuous() \n
		No command help available \n
			:return: sw_pow_init_state: No help available
		"""
		response = self._core.io.query_str('INITiate<HwInstance>:PSWeep:CONTinuous?')
		return Conversions.str_to_bool(response)

	def set_continuous(self, sw_pow_init_state: bool) -> None:
		"""SCPI: INITiate<HW>:PSWeep:CONTinuous \n
		Snippet: driver.initiate.psweep.set_continuous(sw_pow_init_state = False) \n
		No command help available \n
			:param sw_pow_init_state: No help available
		"""
		param = Conversions.bool_to_str(sw_pow_init_state)
		self._core.io.write(f'INITiate<HwInstance>:PSWeep:CONTinuous {param}')
