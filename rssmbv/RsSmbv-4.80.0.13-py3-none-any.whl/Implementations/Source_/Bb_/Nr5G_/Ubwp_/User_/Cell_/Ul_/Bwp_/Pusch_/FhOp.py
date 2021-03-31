from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import enums
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FhOp:
	"""FhOp commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fhOp", core, parent)

	def set(self, sel_freq_hopp: enums.UlfReqHopping, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:PUSCh:FHOP \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.ul.bwp.pusch.fhOp.set(sel_freq_hopp = enums.UlfReqHopping.DIS, channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default) \n
		Disables or enables inter- or intra-slot frequency hopping. \n
			:param sel_freq_hopp: DIS| INTRA| INTER DIS Disable frequency hopping. INTRA Enable intra slot frequency hopping. Both intra- and inter-subframe hopping are performed. The PUSCH position in terms of used resource blocks is changed each slot and each subframe. INTER Enable inter-slot frequency hopping. The PUSCH position in terms of used resource blocks is changed each subframe.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')"""
		param = Conversions.enum_scalar_to_str(sel_freq_hopp, enums.UlfReqHopping)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:PUSCh:FHOP {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> enums.UlfReqHopping:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:PUSCh:FHOP \n
		Snippet: value: enums.UlfReqHopping = driver.source.bb.nr5G.ubwp.user.cell.ul.bwp.pusch.fhOp.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default) \n
		Disables or enables inter- or intra-slot frequency hopping. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:return: sel_freq_hopp: DIS| INTRA| INTER DIS Disable frequency hopping. INTRA Enable intra slot frequency hopping. Both intra- and inter-subframe hopping are performed. The PUSCH position in terms of used resource blocks is changed each slot and each subframe. INTER Enable inter-slot frequency hopping. The PUSCH position in terms of used resource blocks is changed each subframe."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:PUSCh:FHOP?')
		return Conversions.str_to_scalar_enum(response, enums.UlfReqHopping)
