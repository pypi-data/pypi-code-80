from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Si16:
	"""Si16 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("si16", core, parent)

	def set(self, user_alloc_dci_sfi: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default, availableUser=repcap.AvailableUser.Default, bandwidthPart=repcap.BandwidthPart.Default, allocation=repcap.Allocation.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER<DIR>:BWPart<GR>:ALLoc<USER>:CS:DCI:SI16 \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cs.dci.si16.set(user_alloc_dci_sfi = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default, availableUser = repcap.AvailableUser.Default, bandwidthPart = repcap.BandwidthPart.Default, allocation = repcap.Allocation.Default) \n
		Sets the DCI format 2_0 field slot format indicator. \n
			:param user_alloc_dci_sfi: integer Range: 0 to 255
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bandwidthPart: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocation: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')"""
		param = Conversions.decimal_value_to_str(user_alloc_dci_sfi)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		bandwidthPart_cmd_val = self._base.get_repcap_cmd_value(bandwidthPart, repcap.BandwidthPart)
		allocation_cmd_val = self._base.get_repcap_cmd_value(allocation, repcap.Allocation)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER{availableUser_cmd_val}:BWPart{bandwidthPart_cmd_val}:ALLoc{allocation_cmd_val}:CS:DCI:SI16 {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, availableUser=repcap.AvailableUser.Default, bandwidthPart=repcap.BandwidthPart.Default, allocation=repcap.Allocation.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER<DIR>:BWPart<GR>:ALLoc<USER>:CS:DCI:SI16 \n
		Snippet: value: int = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cs.dci.si16.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, availableUser = repcap.AvailableUser.Default, bandwidthPart = repcap.BandwidthPart.Default, allocation = repcap.Allocation.Default) \n
		Sets the DCI format 2_0 field slot format indicator. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bandwidthPart: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocation: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: user_alloc_dci_sfi: integer Range: 0 to 255"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		bandwidthPart_cmd_val = self._base.get_repcap_cmd_value(bandwidthPart, repcap.BandwidthPart)
		allocation_cmd_val = self._base.get_repcap_cmd_value(allocation, repcap.Allocation)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER{availableUser_cmd_val}:BWPart{bandwidthPart_cmd_val}:ALLoc{allocation_cmd_val}:CS:DCI:SI16?')
		return Conversions.str_to_int(response)
