from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Insert:
	"""Insert commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("insert", core, parent)

	def set(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, pseudoRange=repcap.PseudoRange.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:PRERrors:PROFile<GR>:INSert \n
		Snippet: driver.source.bb.gnss.svid.qzss.prErrors.profile.insert.set(channel = repcap.Channel.Default, stream = repcap.Stream.Default, pseudoRange = repcap.PseudoRange.Default) \n
		Inserts a row befor the selected pseudorange error. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:param pseudoRange: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Profile')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		pseudoRange_cmd_val = self._base.get_repcap_cmd_value(pseudoRange, repcap.PseudoRange)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:PRERrors:PROFile{pseudoRange_cmd_val}:INSert')

	def set_with_opc(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, pseudoRange=repcap.PseudoRange.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		pseudoRange_cmd_val = self._base.get_repcap_cmd_value(pseudoRange, repcap.PseudoRange)
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:PRERrors:PROFile<GR>:INSert \n
		Snippet: driver.source.bb.gnss.svid.qzss.prErrors.profile.insert.set_with_opc(channel = repcap.Channel.Default, stream = repcap.Stream.Default, pseudoRange = repcap.PseudoRange.Default) \n
		Inserts a row befor the selected pseudorange error. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:param pseudoRange: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Profile')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:PRERrors:PROFile{pseudoRange_cmd_val}:INSert')
