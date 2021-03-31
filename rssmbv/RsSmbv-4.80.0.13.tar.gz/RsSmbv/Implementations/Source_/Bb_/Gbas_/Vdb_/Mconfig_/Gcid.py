from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gcid:
	"""Gcid commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gcid", core, parent)

	def set(self, gcid: enums.GbasGcid, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:GCID \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.gcid.set(gcid = enums.GbasGcid.FC, channel = repcap.Channel.Default) \n
		Sets the ground station continuity/integrity designator. \n
			:param gcid: FC| FD
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.enum_scalar_to_str(gcid, enums.GbasGcid)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:GCID {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.GbasGcid:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:GCID \n
		Snippet: value: enums.GbasGcid = driver.source.bb.gbas.vdb.mconfig.gcid.get(channel = repcap.Channel.Default) \n
		Sets the ground station continuity/integrity designator. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: gcid: FC| FD"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:GCID?')
		return Conversions.str_to_scalar_enum(response, enums.GbasGcid)
