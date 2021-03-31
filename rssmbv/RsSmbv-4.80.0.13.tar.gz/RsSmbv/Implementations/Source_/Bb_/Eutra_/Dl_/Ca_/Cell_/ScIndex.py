from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScIndex:
	"""ScIndex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scIndex", core, parent)

	def set(self, sched_cell_index: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:CA:CELL<CH>:SCINdex \n
		Snippet: driver.source.bb.eutra.dl.ca.cell.scIndex.set(sched_cell_index = 1, channel = repcap.Channel.Default) \n
		Defines the component carrier/cell that signals the UL and DL grants for the selected SCell. \n
			:param sched_cell_index: integer Range: 0 to 7
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(sched_cell_index)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CA:CELL{channel_cmd_val}:SCINdex {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:CA:CELL<CH>:SCINdex \n
		Snippet: value: int = driver.source.bb.eutra.dl.ca.cell.scIndex.get(channel = repcap.Channel.Default) \n
		Defines the component carrier/cell that signals the UL and DL grants for the selected SCell. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: sched_cell_index: integer Range: 0 to 7"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CA:CELL{channel_cmd_val}:SCINdex?')
		return Conversions.str_to_int(response)
