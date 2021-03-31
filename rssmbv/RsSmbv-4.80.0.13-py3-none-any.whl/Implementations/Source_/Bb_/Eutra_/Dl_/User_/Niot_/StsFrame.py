from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StsFrame:
	"""StsFrame commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stsFrame", core, parent)

	def set(self, search_sp_start_sf: enums.EutraNbiotSearchSpaceStSubframe, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:NIOT:STSFrame \n
		Snippet: driver.source.bb.eutra.dl.user.niot.stsFrame.set(search_sp_start_sf = enums.EutraNbiotSearchSpaceStSubframe.S1_5, channel = repcap.Channel.Default) \n
		Sets the serach space start subframe (G) . \n
			:param search_sp_start_sf: S1_5| S2| S4| S8| S16| S32| S48| S64
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(search_sp_start_sf, enums.EutraNbiotSearchSpaceStSubframe)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:NIOT:STSFrame {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraNbiotSearchSpaceStSubframe:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:NIOT:STSFrame \n
		Snippet: value: enums.EutraNbiotSearchSpaceStSubframe = driver.source.bb.eutra.dl.user.niot.stsFrame.get(channel = repcap.Channel.Default) \n
		Sets the serach space start subframe (G) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: search_sp_start_sf: S1_5| S2| S4| S8| S16| S32| S48| S64"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:NIOT:STSFrame?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbiotSearchSpaceStSubframe)
