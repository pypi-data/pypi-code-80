from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Min:
	"""Min commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("min", core, parent)

	def set(self, pep_in_min: float, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty<ST>:PIN:MIN \n
		Snippet: driver.source.iq.doherty.pin.min.set(pep_in_min = 1.0, stream = repcap.Stream.Default) \n
		No command help available \n
			:param pep_in_min: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')"""
		param = Conversions.decimal_value_to_str(pep_in_min)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:PIN:MIN {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty<ST>:PIN:MIN \n
		Snippet: value: float = driver.source.iq.doherty.pin.min.get(stream = repcap.Stream.Default) \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')
			:return: pep_in_min: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:PIN:MIN?')
		return Conversions.str_to_float(response)
