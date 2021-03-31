from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class McmPosition:
	"""McmPosition commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcmPosition", core, parent)

	def set(self, mcm_position: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:XMRadio:TERRestrial:TRIGger:OUTPut<CH>:MCMPosition \n
		Snippet: driver.source.bb.xmradio.terrestrial.trigger.output.mcmPosition.set(mcm_position = 1, channel = repcap.Channel.Default) \n
		No command help available \n
			:param mcm_position: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(mcm_position)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:XMRadio:TERRestrial:TRIGger:OUTPut{channel_cmd_val}:MCMPosition {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:XMRadio:TERRestrial:TRIGger:OUTPut<CH>:MCMPosition \n
		Snippet: value: int = driver.source.bb.xmradio.terrestrial.trigger.output.mcmPosition.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: mcm_position: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:XMRadio:TERRestrial:TRIGger:OUTPut{channel_cmd_val}:MCMPosition?')
		return Conversions.str_to_int(response)
