from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Step:
	"""Step commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("step", core, parent)

	def set(self, step: float, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PRACh:PPOWer:STEP \n
		Snippet: driver.source.bb.w3Gpp.mstation.prach.ppower.step.set(step = 1.0, stream = repcap.Stream.Default) \n
		The command defines the step width of the power increase, by which the preamble component of the PRACH is increased from
		repetition to repetition. The power defined during the last repetition corresponds to the power defined by the command
		method RsSmbv.Source.Bb.W3Gpp.Mstation.Prach.Ppower.set. \n
			:param step: float Range: 0 dB to 10 dB
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(step)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PRACh:PPOWer:STEP {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PRACh:PPOWer:STEP \n
		Snippet: value: float = driver.source.bb.w3Gpp.mstation.prach.ppower.step.get(stream = repcap.Stream.Default) \n
		The command defines the step width of the power increase, by which the preamble component of the PRACH is increased from
		repetition to repetition. The power defined during the last repetition corresponds to the power defined by the command
		method RsSmbv.Source.Bb.W3Gpp.Mstation.Prach.Ppower.set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: step: float Range: 0 dB to 10 dB"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PRACh:PPOWer:STEP?')
		return Conversions.str_to_float(response)
