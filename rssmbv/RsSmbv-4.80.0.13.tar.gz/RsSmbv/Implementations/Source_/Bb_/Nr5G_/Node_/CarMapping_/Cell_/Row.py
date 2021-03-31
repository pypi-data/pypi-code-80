from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Row:
	"""Row commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("row", core, parent)

	def set(self, map_cell_num: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CARMapping:CELL:[ROW<CH>] \n
		Snippet: driver.source.bb.nr5G.node.carMapping.cell.row.set(map_cell_num = 1, channel = repcap.Channel.Default) \n
		No command help available \n
			:param map_cell_num: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(map_cell_num)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CARMapping:CELL:ROW{channel_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CARMapping:CELL:[ROW<CH>] \n
		Snippet: value: int = driver.source.bb.nr5G.node.carMapping.cell.row.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: map_cell_num: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CARMapping:CELL:ROW{channel_cmd_val}?')
		return Conversions.str_to_int(response)
