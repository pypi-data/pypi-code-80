from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Resolution:
	"""Resolution commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("resolution", core, parent)

	def set(self, resolution: float, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GALileo<ST>:TOAData:RESolution \n
		Snippet: driver.source.bb.gnss.adGeneration.galileo.toaData.resolution.set(resolution = 1.0, stream = repcap.Stream.Default) \n
		Sets the resolution of the assistance data. \n
			:param resolution: float Range: 1E-3 to 5
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')"""
		param = Conversions.decimal_value_to_str(resolution)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GALileo{stream_cmd_val}:TOAData:RESolution {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GALileo<ST>:TOAData:RESolution \n
		Snippet: value: float = driver.source.bb.gnss.adGeneration.galileo.toaData.resolution.get(stream = repcap.Stream.Default) \n
		Sets the resolution of the assistance data. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:return: resolution: float Range: 1E-3 to 5"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GALileo{stream_cmd_val}:TOAData:RESolution?')
		return Conversions.str_to_float(response)
