from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, carrier_sul_state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SYINfo:SUL:STATe \n
		Snippet: driver.source.bb.nr5G.node.cell.syInfo.sul.state.set(carrier_sul_state = False, channel = repcap.Channel.Default) \n
		Defines if the carrier supports supplementary uplink (SUL) or not. \n
			:param carrier_sul_state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.bool_to_str(carrier_sul_state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SYINfo:SUL:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SYINfo:SUL:STATe \n
		Snippet: value: bool = driver.source.bb.nr5G.node.cell.syInfo.sul.state.get(channel = repcap.Channel.Default) \n
		Defines if the carrier supports supplementary uplink (SUL) or not. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: carrier_sul_state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SYINfo:SUL:STATe?')
		return Conversions.str_to_bool(response)
