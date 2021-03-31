from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RbNumber:
	"""RbNumber commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rbNumber", core, parent)

	def set(self, prs_rs_num_rb: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:RSET<ST>:RBNumber \n
		Snippet: driver.source.bb.nr5G.node.cell.prs.rset.rbNumber.set(prs_rs_num_rb = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the number of resource blocks (RBs) for all resources in the resource set in multiples of 4 RBs. \n
			:param prs_rs_num_rb: integer Range: 24 to 272
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rset')"""
		param = Conversions.decimal_value_to_str(prs_rs_num_rb)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:RSET{stream_cmd_val}:RBNumber {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:RSET<ST>:RBNumber \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.prs.rset.rbNumber.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the number of resource blocks (RBs) for all resources in the resource set in multiples of 4 RBs. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rset')
			:return: prs_rs_num_rb: integer Range: 24 to 272"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:RSET{stream_cmd_val}:RBNumber?')
		return Conversions.str_to_int(response)
