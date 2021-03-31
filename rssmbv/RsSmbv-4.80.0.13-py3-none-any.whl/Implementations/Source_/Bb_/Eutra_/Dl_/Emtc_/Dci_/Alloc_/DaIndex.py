from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DaIndex:
	"""DaIndex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("daIndex", core, parent)

	def set(self, dlas_sign_index: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:DCI:ALLoc<CH>:DAINdex \n
		Snippet: driver.source.bb.eutra.dl.emtc.dci.alloc.daIndex.set(dlas_sign_index = 1, channel = repcap.Channel.Default) \n
		In TDD mode and if UL/DL Configuration 0 is used, sets the DCI field downlink assignment index (DAI) . \n
			:param dlas_sign_index: integer Range: 0 to 3
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.decimal_value_to_str(dlas_sign_index)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:DCI:ALLoc{channel_cmd_val}:DAINdex {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:DCI:ALLoc<CH>:DAINdex \n
		Snippet: value: int = driver.source.bb.eutra.dl.emtc.dci.alloc.daIndex.get(channel = repcap.Channel.Default) \n
		In TDD mode and if UL/DL Configuration 0 is used, sets the DCI field downlink assignment index (DAI) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: dlas_sign_index: integer Range: 0 to 3"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:DCI:ALLoc{channel_cmd_val}:DAINdex?')
		return Conversions.str_to_int(response)
