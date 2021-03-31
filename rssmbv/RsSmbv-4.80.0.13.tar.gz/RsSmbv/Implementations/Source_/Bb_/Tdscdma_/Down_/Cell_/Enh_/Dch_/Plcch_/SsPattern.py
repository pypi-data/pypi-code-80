from typing import List

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SsPattern:
	"""SsPattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ssPattern", core, parent)

	# noinspection PyTypeChecker
	class SsPatternStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Ss_Pattern: List[str]: numeric
			- Bit_Count: int: integer Range: 1 to 21"""
		__meta_args_list = [
			ArgStruct('Ss_Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ss_Pattern: List[str] = None
			self.Bit_Count: int = None

	def set(self, structure: SsPatternStruct, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:PLCCh:SSPattern \n
		Snippet: driver.source.bb.tdscdma.down.cell.enh.dch.plcch.ssPattern.set(value = [PROPERTY_STRUCT_NAME](), stream = repcap.Stream.Default) \n
		Sets the sync shift pattern and the pattern length. \n
			:param structure: for set value, see the help for SsPatternStruct structure arguments.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:PLCCh:SSPattern', structure)

	def get(self, stream=repcap.Stream.Default) -> SsPatternStruct:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:PLCCh:SSPattern \n
		Snippet: value: SsPatternStruct = driver.source.bb.tdscdma.down.cell.enh.dch.plcch.ssPattern.get(stream = repcap.Stream.Default) \n
		Sets the sync shift pattern and the pattern length. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: structure: for return value, see the help for SsPatternStruct structure arguments."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:PLCCh:SSPattern?', self.__class__.SsPatternStruct())
