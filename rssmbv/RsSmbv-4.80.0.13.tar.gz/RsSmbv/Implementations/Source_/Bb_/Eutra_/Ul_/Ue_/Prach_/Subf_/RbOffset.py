from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RbOffset:
	"""RbOffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rbOffset", core, parent)

	def set(self, rb_offset: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:SUBF<CH>:RBOFfset \n
		Snippet: driver.source.bb.eutra.ul.ue.prach.subf.rbOffset.set(rb_offset = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Queries the starting RB, as set with the command method RsSmbv.Source.Bb.Eutra.Ul.Prach.foffset. \n
			:param rb_offset: integer Range: 0 to 109
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.decimal_value_to_str(rb_offset)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PRACh:SUBF{channel_cmd_val}:RBOFfset {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:SUBF<CH>:RBOFfset \n
		Snippet: value: int = driver.source.bb.eutra.ul.ue.prach.subf.rbOffset.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Queries the starting RB, as set with the command method RsSmbv.Source.Bb.Eutra.Ul.Prach.foffset. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: rb_offset: integer Range: 0 to 109"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PRACh:SUBF{channel_cmd_val}:RBOFfset?')
		return Conversions.str_to_int(response)
