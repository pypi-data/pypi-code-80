from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ptpc:
	"""Ptpc commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ptpc", core, parent)

	def set(self, pusch_tpc: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:UL:CELL<ST>:SEQelem:PTPC \n
		Snippet: driver.source.bb.eutra.dl.user.asPy.ul.cell.seqElem.ptpc.set(pusch_tpc = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the PUSCH TPC. \n
			:param pusch_tpc: integer Range: 0 to 3
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(pusch_tpc)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:UL:CELL{stream_cmd_val}:SEQelem:PTPC {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:UL:CELL<ST>:SEQelem:PTPC \n
		Snippet: value: int = driver.source.bb.eutra.dl.user.asPy.ul.cell.seqElem.ptpc.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the PUSCH TPC. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: pusch_tpc: integer Range: 0 to 3"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:UL:CELL{stream_cmd_val}:SEQelem:PTPC?')
		return Conversions.str_to_int(response)
