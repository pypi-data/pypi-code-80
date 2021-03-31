from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NumSfi:
	"""NumSfi commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("numSfi", core, parent)

	def set(self, num_sfi_in_dci_20: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:NUMSfi \n
		Snippet: driver.source.bb.nr5G.ubwp.user.numSfi.set(num_sfi_in_dci_20 = 1, channel = repcap.Channel.Default) \n
		Sets how many slot format indicator (SFI) fields are transmitted in the DCI format 2_0. \n
			:param num_sfi_in_dci_20: integer Range: 1 to 16
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.decimal_value_to_str(num_sfi_in_dci_20)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:NUMSfi {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:NUMSfi \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.user.numSfi.get(channel = repcap.Channel.Default) \n
		Sets how many slot format indicator (SFI) fields are transmitted in the DCI format 2_0. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: num_sfi_in_dci_20: integer Range: 1 to 16"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:NUMSfi?')
		return Conversions.str_to_int(response)
