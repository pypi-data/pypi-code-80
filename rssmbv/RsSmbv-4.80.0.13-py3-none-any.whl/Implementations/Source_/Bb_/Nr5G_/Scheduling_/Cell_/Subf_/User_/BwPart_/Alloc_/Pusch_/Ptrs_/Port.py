from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import enums
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Port:
	"""Port commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("port", core, parent)

	def set(self, max_nrof_ports: enums.MaxNrofPorts, channel=repcap.Channel.Default, stream=repcap.Stream.Default, availableUser=repcap.AvailableUser.Default, bandwidthPart=repcap.BandwidthPart.Default, allocation=repcap.Allocation.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER<DIR>:BWPart<GR>:ALLoc<USER>:PUSCh:PTRS:PORT \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pusch.ptrs.port.set(max_nrof_ports = enums.MaxNrofPorts.P1, channel = repcap.Channel.Default, stream = repcap.Stream.Default, availableUser = repcap.AvailableUser.Default, bandwidthPart = repcap.BandwidthPart.Default, allocation = repcap.Allocation.Default) \n
		Sets the maximum number of configured PTRS ports. \n
			:param max_nrof_ports: P1| P2
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bandwidthPart: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocation: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')"""
		param = Conversions.enum_scalar_to_str(max_nrof_ports, enums.MaxNrofPorts)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		bandwidthPart_cmd_val = self._base.get_repcap_cmd_value(bandwidthPart, repcap.BandwidthPart)
		allocation_cmd_val = self._base.get_repcap_cmd_value(allocation, repcap.Allocation)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER{availableUser_cmd_val}:BWPart{bandwidthPart_cmd_val}:ALLoc{allocation_cmd_val}:PUSCh:PTRS:PORT {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, availableUser=repcap.AvailableUser.Default, bandwidthPart=repcap.BandwidthPart.Default, allocation=repcap.Allocation.Default) -> enums.MaxNrofPorts:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER<DIR>:BWPart<GR>:ALLoc<USER>:PUSCh:PTRS:PORT \n
		Snippet: value: enums.MaxNrofPorts = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pusch.ptrs.port.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, availableUser = repcap.AvailableUser.Default, bandwidthPart = repcap.BandwidthPart.Default, allocation = repcap.Allocation.Default) \n
		Sets the maximum number of configured PTRS ports. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bandwidthPart: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocation: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: max_nrof_ports: P1| P2"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		bandwidthPart_cmd_val = self._base.get_repcap_cmd_value(bandwidthPart, repcap.BandwidthPart)
		allocation_cmd_val = self._base.get_repcap_cmd_value(allocation, repcap.Allocation)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER{availableUser_cmd_val}:BWPart{bandwidthPart_cmd_val}:ALLoc{allocation_cmd_val}:PUSCh:PTRS:PORT?')
		return Conversions.str_to_scalar_enum(response, enums.MaxNrofPorts)
