from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Xddn:
	"""Xddn commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("xddn", core, parent)

	def set(self, xn_dot_dot: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:SBAS<ST>:SIMulated:ORBit:XDDN \n
		Snippet: driver.source.bb.gnss.svid.sbas.simulated.orbit.xddn.set(xn_dot_dot = 1.0, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the moon and sun acceleration parameters X''n, Y''n and Z''n. \n
			:param xn_dot_dot: float
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')"""
		param = Conversions.decimal_value_to_str(xn_dot_dot)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:SBAS{stream_cmd_val}:SIMulated:ORBit:XDDN {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:SBAS<ST>:SIMulated:ORBit:XDDN \n
		Snippet: value: float = driver.source.bb.gnss.svid.sbas.simulated.orbit.xddn.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the moon and sun acceleration parameters X''n, Y''n and Z''n. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:return: xn_dot_dot: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:SBAS{stream_cmd_val}:SIMulated:ORBit:XDDN?')
		return Conversions.str_to_float(response)
