from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Codewords:
	"""Codewords commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("codewords", core, parent)

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraCw1CodeWord:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH>:CODWords \n
		Snippet: value: enums.EutraCw1CodeWord = driver.source.bb.eutra.dl.emtc.alloc.codewords.get(channel = repcap.Channel.Default) \n
		Queries the number of the codewords. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: code_word: CW11| CW12"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{channel_cmd_val}:CODWords?')
		return Conversions.str_to_scalar_enum(response, enums.EutraCw1CodeWord)
