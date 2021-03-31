from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pindex:
	"""Pindex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pindex", core, parent)

	def set(self, pi_ndex: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:TRIGger:OUTPut<CH>:PINDex \n
		Snippet: driver.source.bb.btooth.trigger.output.pindex.set(pi_ndex = 1, channel = repcap.Channel.Default) \n
		No command help available \n
			:param pi_ndex: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(pi_ndex)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:TRIGger:OUTPut{channel_cmd_val}:PINDex {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:TRIGger:OUTPut<CH>:PINDex \n
		Snippet: value: int = driver.source.bb.btooth.trigger.output.pindex.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: pi_ndex: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:TRIGger:OUTPut{channel_cmd_val}:PINDex?')
		return Conversions.str_to_int(response)
