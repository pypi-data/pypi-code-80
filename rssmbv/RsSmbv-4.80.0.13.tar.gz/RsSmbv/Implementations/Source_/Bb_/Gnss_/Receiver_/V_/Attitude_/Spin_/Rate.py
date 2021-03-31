from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rate:
	"""Rate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rate", core, parent)

	def set(self, rate: float, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ATTitude:SPIN:RATE \n
		Snippet: driver.source.bb.gnss.receiver.v.attitude.spin.rate.set(rate = 1.0, stream = repcap.Stream.Default) \n
		Sets the constant rate of change of the roll. \n
			:param rate: float Range: -400 to 400
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.decimal_value_to_str(rate)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ATTitude:SPIN:RATE {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ATTitude:SPIN:RATE \n
		Snippet: value: float = driver.source.bb.gnss.receiver.v.attitude.spin.rate.get(stream = repcap.Stream.Default) \n
		Sets the constant rate of change of the roll. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: rate: float Range: -400 to 400"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ATTitude:SPIN:RATE?')
		return Conversions.str_to_float(response)
