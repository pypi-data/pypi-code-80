from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup
from ..............Internal import Conversions
from .............. import enums
from .............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MaxCandidate:
	"""MaxCandidate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("maxCandidate", core, parent)

	def set(self, max_candidate: enums.NumbersC, channel=repcap.Channel.Default, stream=repcap.Stream.Default, availableUser=repcap.AvailableUser.Default, bandwidthPart=repcap.BandwidthPart.Default, allocation=repcap.Allocation.Default, spaceIx=repcap.SpaceIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER<DIR>:BWPart<GR>:ALLoc<USER>:CS:DMRS:SPACe<S2US>:MAXCandidate \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cs.dmrs.space.maxCandidate.set(max_candidate = enums.NumbersC._1, channel = repcap.Channel.Default, stream = repcap.Stream.Default, availableUser = repcap.AvailableUser.Default, bandwidthPart = repcap.BandwidthPart.Default, allocation = repcap.Allocation.Default, spaceIx = repcap.SpaceIx.Default) \n
		Sets the maximum number of candidates allowed for the selected aggregation level. \n
			:param max_candidate: 1| 2| 3| 4| 5| 6| 8
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bandwidthPart: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocation: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:param spaceIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Space')"""
		param = Conversions.enum_scalar_to_str(max_candidate, enums.NumbersC)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		bandwidthPart_cmd_val = self._base.get_repcap_cmd_value(bandwidthPart, repcap.BandwidthPart)
		allocation_cmd_val = self._base.get_repcap_cmd_value(allocation, repcap.Allocation)
		spaceIx_cmd_val = self._base.get_repcap_cmd_value(spaceIx, repcap.SpaceIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER{availableUser_cmd_val}:BWPart{bandwidthPart_cmd_val}:ALLoc{allocation_cmd_val}:CS:DMRS:SPACe{spaceIx_cmd_val}:MAXCandidate {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, availableUser=repcap.AvailableUser.Default, bandwidthPart=repcap.BandwidthPart.Default, allocation=repcap.Allocation.Default, spaceIx=repcap.SpaceIx.Default) -> enums.NumbersC:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER<DIR>:BWPart<GR>:ALLoc<USER>:CS:DMRS:SPACe<S2US>:MAXCandidate \n
		Snippet: value: enums.NumbersC = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cs.dmrs.space.maxCandidate.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, availableUser = repcap.AvailableUser.Default, bandwidthPart = repcap.BandwidthPart.Default, allocation = repcap.Allocation.Default, spaceIx = repcap.SpaceIx.Default) \n
		Sets the maximum number of candidates allowed for the selected aggregation level. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bandwidthPart: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocation: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:param spaceIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Space')
			:return: max_candidate: 1| 2| 3| 4| 5| 6| 8"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		bandwidthPart_cmd_val = self._base.get_repcap_cmd_value(bandwidthPart, repcap.BandwidthPart)
		allocation_cmd_val = self._base.get_repcap_cmd_value(allocation, repcap.Allocation)
		spaceIx_cmd_val = self._base.get_repcap_cmd_value(spaceIx, repcap.SpaceIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER{availableUser_cmd_val}:BWPart{bandwidthPart_cmd_val}:ALLoc{allocation_cmd_val}:CS:DMRS:SPACe{spaceIx_cmd_val}:MAXCandidate?')
		return Conversions.str_to_scalar_enum(response, enums.NumbersC)
