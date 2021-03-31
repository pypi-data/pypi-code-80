from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Iode:
	"""Iode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("iode", core, parent)

	def set(self, io_de: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:NMESsage:LNAV:EPHemeris:IODE \n
		Snippet: driver.source.bb.gnss.svid.gps.nmessage.lnav.ephemeris.iode.set(io_de = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the issue of data, emphemeris. \n
			:param io_de: integer Range: 0 to 255
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.decimal_value_to_str(io_de)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:NMESsage:LNAV:EPHemeris:IODE {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:NMESsage:LNAV:EPHemeris:IODE \n
		Snippet: value: int = driver.source.bb.gnss.svid.gps.nmessage.lnav.ephemeris.iode.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the issue of data, emphemeris. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: io_de: integer Range: 0 to 255"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:NMESsage:LNAV:EPHemeris:IODE?')
		return Conversions.str_to_int(response)
