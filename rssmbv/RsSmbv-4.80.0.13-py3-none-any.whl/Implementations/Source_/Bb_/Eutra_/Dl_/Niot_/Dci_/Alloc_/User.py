from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)

	def set(self, user: enums.EutraEmtcPdcchCfg, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:NIOT:DCI:ALLoc<CH>:USER \n
		Snippet: driver.source.bb.eutra.dl.niot.dci.alloc.user.set(user = enums.EutraEmtcPdcchCfg.PRNTi, channel = repcap.Channel.Default) \n
		Selects the user the DCI is dedicated to. \n
			:param user: USER1| USER2| USER3| USER4| PRNTi| RARNti
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.enum_scalar_to_str(user, enums.EutraEmtcPdcchCfg)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:DCI:ALLoc{channel_cmd_val}:USER {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraEmtcPdcchCfg:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:NIOT:DCI:ALLoc<CH>:USER \n
		Snippet: value: enums.EutraEmtcPdcchCfg = driver.source.bb.eutra.dl.niot.dci.alloc.user.get(channel = repcap.Channel.Default) \n
		Selects the user the DCI is dedicated to. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: user: USER1| USER2| USER3| USER4| PRNTi| RARNti"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:DCI:ALLoc{channel_cmd_val}:USER?')
		return Conversions.str_to_scalar_enum(response, enums.EutraEmtcPdcchCfg)
