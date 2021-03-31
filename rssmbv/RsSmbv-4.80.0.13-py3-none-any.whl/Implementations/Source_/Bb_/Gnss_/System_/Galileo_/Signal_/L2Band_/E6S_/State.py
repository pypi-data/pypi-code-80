from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, signal_state: bool, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SYSTem:GALileo<ST>:SIGNal:L2Band:E6S:[STATe] \n
		Snippet: driver.source.bb.gnss.system.galileo.signal.l2Band.e6S.state.set(signal_state = False, stream = repcap.Stream.Default) \n
		Enables the corresponding signal from the GNSS system in the corresponding RF band. \n
			:param signal_state: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')"""
		param = Conversions.bool_to_str(signal_state)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SYSTem:GALileo{stream_cmd_val}:SIGNal:L2Band:E6S:STATe {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SYSTem:GALileo<ST>:SIGNal:L2Band:E6S:[STATe] \n
		Snippet: value: bool = driver.source.bb.gnss.system.galileo.signal.l2Band.e6S.state.get(stream = repcap.Stream.Default) \n
		Enables the corresponding signal from the GNSS system in the corresponding RF band. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:return: signal_state: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SYSTem:GALileo{stream_cmd_val}:SIGNal:L2Band:E6S:STATe?')
		return Conversions.str_to_bool(response)
