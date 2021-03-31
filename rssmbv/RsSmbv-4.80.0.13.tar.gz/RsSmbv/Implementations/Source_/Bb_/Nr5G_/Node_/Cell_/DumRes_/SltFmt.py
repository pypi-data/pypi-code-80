from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SltFmt:
	"""SltFmt commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sltFmt", core, parent)

	def set(self, slot_fmt: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:DUMRes:SLTFmt \n
		Snippet: driver.source.bb.nr5G.node.cell.dumRes.sltFmt.set(slot_fmt = 1, channel = repcap.Channel.Default) \n
		No command help available \n
			:param slot_fmt: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(slot_fmt)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:DUMRes:SLTFmt {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:DUMRes:SLTFmt \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.dumRes.sltFmt.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: slot_fmt: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:DUMRes:SLTFmt?')
		return Conversions.str_to_int(response)
