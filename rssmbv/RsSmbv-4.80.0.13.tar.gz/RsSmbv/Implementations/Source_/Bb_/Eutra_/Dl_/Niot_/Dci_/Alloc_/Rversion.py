from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rversion:
	"""Rversion commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rversion", core, parent)

	def set(self, redundancy_vers: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:NIOT:DCI:ALLoc<CH>:RVERsion \n
		Snippet: driver.source.bb.eutra.dl.niot.dci.alloc.rversion.set(redundancy_vers = 1, channel = repcap.Channel.Default) \n
		Sets the DCI field redundancy version. \n
			:param redundancy_vers: integer Range: 0 to 1
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.decimal_value_to_str(redundancy_vers)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:DCI:ALLoc{channel_cmd_val}:RVERsion {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:NIOT:DCI:ALLoc<CH>:RVERsion \n
		Snippet: value: int = driver.source.bb.eutra.dl.niot.dci.alloc.rversion.get(channel = repcap.Channel.Default) \n
		Sets the DCI field redundancy version. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: redundancy_vers: integer Range: 0 to 1"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:DCI:ALLoc{channel_cmd_val}:RVERsion?')
		return Conversions.str_to_int(response)
