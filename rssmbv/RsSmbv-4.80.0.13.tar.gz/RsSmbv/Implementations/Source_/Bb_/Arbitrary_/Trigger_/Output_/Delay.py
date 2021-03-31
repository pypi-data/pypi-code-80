from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delay:
	"""Delay commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delay", core, parent)

	def set(self, delay: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TRIGger:OUTPut<CH>:DELay \n
		Snippet: driver.source.bb.arbitrary.trigger.output.delay.set(delay = 1, channel = repcap.Channel.Default) \n
		Defines the delay between the signal on the marker outputs and the start of the signals. \n
			:param delay: integer Range: 0 to depends on other values, Unit: Symbol
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(delay)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TRIGger:OUTPut{channel_cmd_val}:DELay {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:TRIGger:OUTPut<CH>:DELay \n
		Snippet: value: int = driver.source.bb.arbitrary.trigger.output.delay.get(channel = repcap.Channel.Default) \n
		Defines the delay between the signal on the marker outputs and the start of the signals. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: delay: integer Range: 0 to depends on other values, Unit: Symbol"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ARBitrary:TRIGger:OUTPut{channel_cmd_val}:DELay?')
		return Conversions.str_to_int(response)
