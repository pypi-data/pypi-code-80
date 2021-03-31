from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sposition:
	"""Sposition commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sposition", core, parent)

	def set(self, sposition: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:SIRius:TERRestrial:TRIGger:OUTPut<CH>:SPOSition \n
		Snippet: driver.source.bb.sirius.terrestrial.trigger.output.sposition.set(sposition = 1, channel = repcap.Channel.Default) \n
		No command help available \n
			:param sposition: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(sposition)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:SIRius:TERRestrial:TRIGger:OUTPut{channel_cmd_val}:SPOSition {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:SIRius:TERRestrial:TRIGger:OUTPut<CH>:SPOSition \n
		Snippet: value: int = driver.source.bb.sirius.terrestrial.trigger.output.sposition.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: sposition: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:SIRius:TERRestrial:TRIGger:OUTPut{channel_cmd_val}:SPOSition?')
		return Conversions.str_to_int(response)
