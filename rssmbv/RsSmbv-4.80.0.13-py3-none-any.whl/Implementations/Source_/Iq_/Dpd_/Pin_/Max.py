from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Max:
	"""Max commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("max", core, parent)

	def set(self, pep_in_max: float, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DPD<ST>:PIN:MAX \n
		Snippet: driver.source.iq.dpd.pin.max.set(pep_in_max = 1.0, stream = repcap.Stream.Default) \n
		Sets the value range of the input power. \n
			:param pep_in_max: float Range: -145 to 20
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')"""
		param = Conversions.decimal_value_to_str(pep_in_max)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:PIN:MAX {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:IQ:DPD<ST>:PIN:MAX \n
		Snippet: value: float = driver.source.iq.dpd.pin.max.get(stream = repcap.Stream.Default) \n
		Sets the value range of the input power. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')
			:return: pep_in_max: float Range: -145 to 20"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:PIN:MAX?')
		return Conversions.str_to_float(response)
