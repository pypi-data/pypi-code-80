from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModPreset:
	"""ModPreset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modPreset", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:OFDM:MODPreset \n
		Snippet: driver.source.bb.ofdm.modPreset.set() \n
		Calls the default settings for the selected moduilation type, see method RsSmbv.Source.Bb.Ofdm.modulation. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:MODPreset')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:OFDM:MODPreset \n
		Snippet: driver.source.bb.ofdm.modPreset.set_with_opc() \n
		Calls the default settings for the selected moduilation type, see method RsSmbv.Source.Bb.Ofdm.modulation. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:OFDM:MODPreset')
