from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pconfiguration:
	"""Pconfiguration commands group definition. 121 total commands, 13 Sub-groups, 84 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pconfiguration", core, parent)

	@property
	def acad(self):
		"""acad commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_acad'):
			from .Pconfiguration_.Acad import Acad
			self._acad = Acad(self._core, self._base)
		return self._acad

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_data'):
			from .Pconfiguration_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def dcmTable(self):
		"""dcmTable commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dcmTable'):
			from .Pconfiguration_.DcmTable import DcmTable
			self._dcmTable = DcmTable(self._core, self._base)
		return self._dcmTable

	@property
	def eheader(self):
		"""eheader commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eheader'):
			from .Pconfiguration_.Eheader import Eheader
			self._eheader = Eheader(self._core, self._base)
		return self._eheader

	@property
	def ehFlags(self):
		"""ehFlags commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_ehFlags'):
			from .Pconfiguration_.EhFlags import EhFlags
			self._ehFlags = EhFlags(self._core, self._base)
		return self._ehFlags

	@property
	def fsbit(self):
		"""fsbit commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fsbit'):
			from .Pconfiguration_.Fsbit import Fsbit
			self._fsbit = Fsbit(self._core, self._base)
		return self._fsbit

	@property
	def mtsphy(self):
		"""mtsphy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_mtsphy'):
			from .Pconfiguration_.Mtsphy import Mtsphy
			self._mtsphy = Mtsphy(self._core, self._base)
		return self._mtsphy

	@property
	def offset(self):
		"""offset commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_offset'):
			from .Pconfiguration_.Offset import Offset
			self._offset = Offset(self._core, self._base)
		return self._offset

	@property
	def phy(self):
		"""phy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_phy'):
			from .Pconfiguration_.Phy import Phy
			self._phy = Phy(self._core, self._base)
		return self._phy

	@property
	def phys(self):
		"""phys commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_phys'):
			from .Pconfiguration_.Phys import Phys
			self._phys = Phys(self._core, self._base)
		return self._phys

	@property
	def rphys(self):
		"""rphys commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_rphys'):
			from .Pconfiguration_.Rphys import Rphys
			self._rphys = Rphys(self._core, self._base)
		return self._rphys

	@property
	def stmPhy(self):
		"""stmPhy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_stmPhy'):
			from .Pconfiguration_.StmPhy import StmPhy
			self._stmPhy = StmPhy(self._core, self._base)
		return self._stmPhy

	@property
	def tphys(self):
		"""tphys commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_tphys'):
			from .Pconfiguration_.Tphys import Tphys
			self._tphys = Tphys(self._core, self._base)
		return self._tphys

	# noinspection PyTypeChecker
	class AaddressStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Aaddress: List[str]: numeric
			- Bit_Count: int: integer Range: 32 to 32"""
		__meta_args_list = [
			ArgStruct('Aaddress', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Aaddress: List[str] = None
			self.Bit_Count: int = None

	def get_aaddress(self) -> AaddressStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AADDress \n
		Snippet: value: AaddressStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_aaddress() \n
		Sets the access address of the link layer connection (32-bit string) . \n
			:return: structure: for return value, see the help for AaddressStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AADDress?', self.__class__.AaddressStruct())

	def set_aaddress(self, value: AaddressStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AADDress \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_aaddress(value = AaddressStruct()) \n
		Sets the access address of the link layer connection (32-bit string) . \n
			:param value: see the help for AaddressStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AADDress', value)

	# noinspection PyTypeChecker
	class AcAssignedStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ac_Assigned: List[str]: No parameter help available
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Ac_Assigned', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ac_Assigned: List[str] = None
			self.Bit_Count: int = None

	def get_ac_assigned(self) -> AcAssignedStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACASsigned \n
		Snippet: value: AcAssignedStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_ac_assigned() \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:return: structure: for return value, see the help for AcAssignedStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACASsigned?', self.__class__.AcAssignedStruct())

	def set_ac_assigned(self, value: AcAssignedStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACASsigned \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_ac_assigned(value = AcAssignedStruct()) \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:param value: see the help for AcAssignedStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACASsigned', value)

	# noinspection PyTypeChecker
	class AcidStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Acid: List[str]: No parameter help available
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Acid', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Acid: List[str] = None
			self.Bit_Count: int = None

	def get_acid(self) -> AcidStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACID \n
		Snippet: value: AcidStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_acid() \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:return: structure: for return value, see the help for AcidStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACID?', self.__class__.AcidStruct())

	def set_acid(self, value: AcidStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACID \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_acid(value = AcidStruct()) \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:param value: see the help for AcidStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACID', value)

	# noinspection PyTypeChecker
	class AdidStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Adid: List[str]: numeric
			- Bit_Count: int: integer Range: 12 to 12"""
		__meta_args_list = [
			ArgStruct('Adid', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Adid: List[str] = None
			self.Bit_Count: int = None

	def get_adid(self) -> AdidStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ADID \n
		Snippet: value: AdidStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_adid() \n
		Specifies 'Advertising Data ID' in hexadecimal format to be signaled within an extended header. \n
			:return: structure: for return value, see the help for AdidStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ADID?', self.__class__.AdidStruct())

	def set_adid(self, value: AdidStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ADID \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_adid(value = AdidStruct()) \n
		Specifies 'Advertising Data ID' in hexadecimal format to be signaled within an extended header. \n
			:param value: see the help for AdidStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ADID', value)

	# noinspection PyTypeChecker
	class AlapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Lap: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Lap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lap: List[str] = None
			self.Bit_Count: int = None

	def get_alap(self) -> AlapStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ALAP \n
		Snippet: value: AlapStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_alap() \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner’s or
		initiator’s target device address to which the advertisement is directed ..:TLAP. \n
			:return: structure: for return value, see the help for AlapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ALAP?', self.__class__.AlapStruct())

	def set_alap(self, value: AlapStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ALAP \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_alap(value = AlapStruct()) \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner’s or
		initiator’s target device address to which the advertisement is directed ..:TLAP. \n
			:param value: see the help for AlapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ALAP', value)

	def get_alength(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ALENgth \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_alength() \n
		Specifies the length of ACAD data pattern. \n
			:return: length: integer Range: 0 to 62
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ALENgth?')
		return Conversions.str_to_int(response)

	def set_alength(self, length: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ALENgth \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_alength(length = 1) \n
		Specifies the length of ACAD data pattern. \n
			:param length: integer Range: 0 to 62
		"""
		param = Conversions.decimal_value_to_str(length)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ALENgth {param}')

	# noinspection PyTypeChecker
	def get_amode(self) -> enums.BtoAdvMode:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AMODe \n
		Snippet: value: enums.BtoAdvMode = driver.source.bb.btooth.econfiguration.pconfiguration.get_amode() \n
		Indicates the mode of the advertisement. \n
			:return: am_ode: NCNS| CNS| NCS NCNS: Non-connectable, non-scannable CNS: Connectable, non-scannable NCS: Non-connectable, non-scannable
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AMODe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoAdvMode)

	def set_amode(self, am_ode: enums.BtoAdvMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AMODe \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_amode(am_ode = enums.BtoAdvMode.CNS) \n
		Indicates the mode of the advertisement. \n
			:param am_ode: NCNS| CNS| NCS NCNS: Non-connectable, non-scannable CNS: Connectable, non-scannable NCS: Non-connectable, non-scannable
		"""
		param = Conversions.enum_scalar_to_str(am_ode, enums.BtoAdvMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AMODe {param}')

	# noinspection PyTypeChecker
	class AnuapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Nap_Uap: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Nap_Uap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Nap_Uap: List[str] = None
			self.Bit_Count: int = None

	def get_anuap(self) -> AnuapStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ANUap \n
		Snippet: value: AnuapStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_anuap() \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner’s or initiator’s target device address to which the advertisement is
		directed ..:TNUap. \n
			:return: structure: for return value, see the help for AnuapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ANUap?', self.__class__.AnuapStruct())

	def set_anuap(self, value: AnuapStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ANUap \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_anuap(value = AnuapStruct()) \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner’s or initiator’s target device address to which the advertisement is
		directed ..:TNUap. \n
			:param value: see the help for AnuapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ANUap', value)

	def get_aoffset(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AOFFset \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_aoffset() \n
		Specifies the time from the start of the packet containing the AuxPtr field to the approximate start of the auxiliary
		packet. The offset is determined by multiplying the value by the unit, see method RsSmbv.Source.Bb.Btooth.Econfiguration.
		Pconfiguration.aoUnits \n
			:return: ao_ffset: float Range: 0 to 245.7 or 246 to 2457 depending on offset unit
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AOFFset?')
		return Conversions.str_to_float(response)

	def set_aoffset(self, ao_ffset: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AOFFset \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_aoffset(ao_ffset = 1.0) \n
		Specifies the time from the start of the packet containing the AuxPtr field to the approximate start of the auxiliary
		packet. The offset is determined by multiplying the value by the unit, see method RsSmbv.Source.Bb.Btooth.Econfiguration.
		Pconfiguration.aoUnits \n
			:param ao_ffset: float Range: 0 to 245.7 or 246 to 2457 depending on offset unit
		"""
		param = Conversions.decimal_value_to_str(ao_ffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AOFFset {param}')

	# noinspection PyTypeChecker
	def get_ao_units(self) -> enums.BtoOffsUnit:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AOUNits \n
		Snippet: value: enums.BtoOffsUnit = driver.source.bb.btooth.econfiguration.pconfiguration.get_ao_units() \n
		Indicates the units used by the 'Aux Offset' parameter, see method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.
		aoffset \n
			:return: unit: U30| U300 U30: 30 µs U300: 300 µs
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AOUNits?')
		return Conversions.str_to_scalar_enum(response, enums.BtoOffsUnit)

	def set_ao_units(self, unit: enums.BtoOffsUnit) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AOUNits \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_ao_units(unit = enums.BtoOffsUnit.U30) \n
		Indicates the units used by the 'Aux Offset' parameter, see method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.
		aoffset \n
			:param unit: U30| U300 U30: 30 µs U300: 300 µs
		"""
		param = Conversions.enum_scalar_to_str(unit, enums.BtoOffsUnit)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AOUNits {param}')

	# noinspection PyTypeChecker
	def get_aphy(self) -> enums.PackFormat:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:APHY \n
		Snippet: value: enums.PackFormat = driver.source.bb.btooth.econfiguration.pconfiguration.get_aphy() \n
		Specifies the physical layer used to transmit the auxiliary packet. \n
			:return: aphy: L1M| L2M| LCOD LE 1M, LE 2M, LE coded PHY
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:APHY?')
		return Conversions.str_to_scalar_enum(response, enums.PackFormat)

	def set_aphy(self, aphy: enums.PackFormat) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:APHY \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_aphy(aphy = enums.PackFormat.L1M) \n
		Specifies the physical layer used to transmit the auxiliary packet. \n
			:param aphy: L1M| L2M| LCOD LE 1M, LE 2M, LE coded PHY
		"""
		param = Conversions.enum_scalar_to_str(aphy, enums.PackFormat)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:APHY {param}')

	# noinspection PyTypeChecker
	class AsidStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Asid: List[str]: numeric
			- Bit_Count: int: integer Range: 4 to 4"""
		__meta_args_list = [
			ArgStruct('Asid', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Asid: List[str] = None
			self.Bit_Count: int = None

	def get_asid(self) -> AsidStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ASID \n
		Snippet: value: AsidStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_asid() \n
		Specifies the 'Advertising Set ID' in hexadecimal format to be signaled within an extended header. \n
			:return: structure: for return value, see the help for AsidStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ASID?', self.__class__.AsidStruct())

	def set_asid(self, value: AsidStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ASID \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_asid(value = AsidStruct()) \n
		Specifies the 'Advertising Set ID' in hexadecimal format to be signaled within an extended header. \n
			:param value: see the help for AsidStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ASID', value)

	# noinspection PyTypeChecker
	def get_atype(self) -> enums.BtoUlpAddrType:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ATYPe \n
		Snippet: value: enums.BtoUlpAddrType = driver.source.bb.btooth.econfiguration.pconfiguration.get_atype() \n
		Sets the address type in the payload of Bluetooth LE LL_PERIODIC_SYNC_IND packets. \n
			:return: atype: PUBLic| RANDom
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ATYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoUlpAddrType)

	def set_atype(self, atype: enums.BtoUlpAddrType) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ATYPe \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_atype(atype = enums.BtoUlpAddrType.PUBLic) \n
		Sets the address type in the payload of Bluetooth LE LL_PERIODIC_SYNC_IND packets. \n
			:param atype: PUBLic| RANDom
		"""
		param = Conversions.enum_scalar_to_str(atype, enums.BtoUlpAddrType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ATYPe {param}')

	# noinspection PyTypeChecker
	def get_caccuracy(self) -> enums.BtoClkAcc:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CACCuracy \n
		Snippet: value: enums.BtoClkAcc = driver.source.bb.btooth.econfiguration.pconfiguration.get_caccuracy() \n
		Specifies the clock accuracy of the advertiser used between the packet containing this data and the auxiliary packet. \n
			:return: caccuracy: T500| T50 T500: 51 ppm to 500 ppm T50: 0 ppm to 50 ppm
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CACCuracy?')
		return Conversions.str_to_scalar_enum(response, enums.BtoClkAcc)

	def set_caccuracy(self, caccuracy: enums.BtoClkAcc) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CACCuracy \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_caccuracy(caccuracy = enums.BtoClkAcc.T50) \n
		Specifies the clock accuracy of the advertiser used between the packet containing this data and the auxiliary packet. \n
			:param caccuracy: T500| T50 T500: 51 ppm to 500 ppm T50: 0 ppm to 50 ppm
		"""
		param = Conversions.enum_scalar_to_str(caccuracy, enums.BtoClkAcc)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CACCuracy {param}')

	def get_cecount(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CECount \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_cecount() \n
		Specifies the connection event count in the CtrData field of the LL_PERIODIC_SYNC_IND control data PDU. \n
			:return: ce_count: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CECount?')
		return Conversions.str_to_int(response)

	def set_cecount(self, ce_count: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CECount \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_cecount(ce_count = 1) \n
		Specifies the connection event count in the CtrData field of the LL_PERIODIC_SYNC_IND control data PDU. \n
			:param ce_count: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(ce_count)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CECount {param}')

	# noinspection PyTypeChecker
	class CidStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Cid: List[str]: numeric
			- Bit_Count: int: integer Range: 16 to 16"""
		__meta_args_list = [
			ArgStruct('Cid', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cid: List[str] = None
			self.Bit_Count: int = None

	def get_cid(self) -> CidStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CID \n
		Snippet: value: CidStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_cid() \n
		Sets the company identifier of the manufacturer of the Bluetooth Controller. A 16 bit value is set. Note: This parameter
		is relevant for data frame configuration and for the packet type LL_VERSION_IND. \n
			:return: structure: for return value, see the help for CidStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CID?', self.__class__.CidStruct())

	def set_cid(self, value: CidStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CID \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_cid(value = CidStruct()) \n
		Sets the company identifier of the manufacturer of the Bluetooth Controller. A 16 bit value is set. Note: This parameter
		is relevant for data frame configuration and for the packet type LL_VERSION_IND. \n
			:param value: see the help for CidStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CID', value)

	def get_cinstant(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CINStant \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_cinstant() \n
		Sets a connection instant for indicating the connection event at which the new connection parameters are taken in use. \n
			:return: cinstant: integer Range: 1 to depends on sequence length
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CINStant?')
		return Conversions.str_to_int(response)

	def set_cinstant(self, cinstant: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CINStant \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_cinstant(cinstant = 1) \n
		Sets a connection instant for indicating the connection event at which the new connection parameters are taken in use. \n
			:param cinstant: integer Range: 1 to depends on sequence length
		"""
		param = Conversions.decimal_value_to_str(cinstant)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CINStant {param}')

	def get_cinterval(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CINTerval \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_cinterval() \n
		Sets the time interval between the start points of two consecutive connection events for the packet type DATA and all
		CONTROL_DATA packet types. Command sets the values in ms. Query returns values in s. \n
			:return: cinterval: float Range: 7.5E-3 s to depends on oversampling , Unit: ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CINTerval?')
		return Conversions.str_to_float(response)

	def set_cinterval(self, cinterval: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CINTerval \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_cinterval(cinterval = 1.0) \n
		Sets the time interval between the start points of two consecutive connection events for the packet type DATA and all
		CONTROL_DATA packet types. Command sets the values in ms. Query returns values in s. \n
			:param cinterval: float Range: 7.5E-3 s to depends on oversampling , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(cinterval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CINTerval {param}')

	# noinspection PyTypeChecker
	class CivalueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ci_Value: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Ci_Value', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ci_Value: List[str] = None
			self.Bit_Count: int = None

	def get_civalue(self) -> CivalueStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CIValue \n
		Snippet: value: CivalueStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_civalue() \n
		Sets the initialization value for the CRC (Cyclic Redundancy Check, 24 bits) calculation. A packet has been received
		correctly, when it has passed the CRC check. \n
			:return: structure: for return value, see the help for CivalueStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CIValue?', self.__class__.CivalueStruct())

	def set_civalue(self, value: CivalueStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CIValue \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_civalue(value = CivalueStruct()) \n
		Sets the initialization value for the CRC (Cyclic Redundancy Check, 24 bits) calculation. A packet has been received
		correctly, when it has passed the CRC check. \n
			:param value: see the help for CivalueStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CIValue', value)

	def get_cpresent(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CPResent \n
		Snippet: value: bool = driver.source.bb.btooth.econfiguration.pconfiguration.get_cpresent() \n
		Activates the CTEInfo field in the header of Bluetooth LE data packets in the LE uncoded PHY. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CPResent?')
		return Conversions.str_to_bool(response)

	def set_cpresent(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CPResent \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_cpresent(state = False) \n
		Activates the CTEInfo field in the header of Bluetooth LE data packets in the LE uncoded PHY. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CPResent {param}')

	# noinspection PyTypeChecker
	def get_cselection(self) -> enums.BtoChSel:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CSELection \n
		Snippet: value: enums.BtoChSel = driver.source.bb.btooth.econfiguration.pconfiguration.get_cselection() \n
		Specifies the algorithm of channel selection. \n
			:return: csrlection: CS1| CS2 Algorithm #1 or algorithm #2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CSELection?')
		return Conversions.str_to_scalar_enum(response, enums.BtoChSel)

	def set_cselection(self, csrlection: enums.BtoChSel) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CSELection \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_cselection(csrlection = enums.BtoChSel.CS1) \n
		Specifies the algorithm of channel selection. \n
			:param csrlection: CS1| CS2 Algorithm #1 or algorithm #2
		"""
		param = Conversions.enum_scalar_to_str(csrlection, enums.BtoChSel)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CSELection {param}')

	def get_ctime(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CTIMe \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_ctime() \n
		Sets the CTETime comprising the length of constant tone extension field of the Bluetooth LE PDU. \n
			:return: ctime: float Range: 16E-6 to 160E-6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CTIMe?')
		return Conversions.str_to_float(response)

	def set_ctime(self, ctime: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CTIMe \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_ctime(ctime = 1.0) \n
		Sets the CTETime comprising the length of constant tone extension field of the Bluetooth LE PDU. \n
			:param ctime: float Range: 16E-6 to 160E-6
		"""
		param = Conversions.decimal_value_to_str(ctime)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CTIMe {param}')

	# noinspection PyTypeChecker
	def get_ct_req(self) -> enums.BtoCteType:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CTReq \n
		Snippet: value: enums.BtoCteType = driver.source.bb.btooth.econfiguration.pconfiguration.get_ct_req() \n
		Sets the CTE type in the CTETypeReq field of the CtrData field of the LL_CTE_REQ PDU. \n
			:return: ct_req: AOD1| AOA| AOD2 AOA AoA Constant Tone Extension AOD1 AoD Constant Tone Extension with 1 µs time slots AOD2 AoD Constant Tone Extension with 2 µs time slots
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CTReq?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCteType)

	def set_ct_req(self, ct_req: enums.BtoCteType) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CTReq \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_ct_req(ct_req = enums.BtoCteType.AOA) \n
		Sets the CTE type in the CTETypeReq field of the CtrData field of the LL_CTE_REQ PDU. \n
			:param ct_req: AOD1| AOA| AOD2 AOA AoA Constant Tone Extension AOD1 AoD Constant Tone Extension with 1 µs time slots AOD2 AoD Constant Tone Extension with 2 µs time slots
		"""
		param = Conversions.enum_scalar_to_str(ct_req, enums.BtoCteType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CTReq {param}')

	# noinspection PyTypeChecker
	def get_ctype(self) -> enums.BtoCteType:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CTYPe \n
		Snippet: value: enums.BtoCteType = driver.source.bb.btooth.econfiguration.pconfiguration.get_ctype() \n
		Sets the type of constant tone extension. The type specifies the CTE AoA/AoD method and for AoD the length of the
		switching and I/Q sampling slots. \n
			:return: ctype: AOD1| AOA| AOD2 AOA AoA Constant Tone Extension AOD1 AoD Constant Tone Extension with 1 µs time slots AOD2 AoD Constant Tone Extension with 2 µs time slots
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCteType)

	def set_ctype(self, ctype: enums.BtoCteType) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CTYPe \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_ctype(ctype = enums.BtoCteType.AOA) \n
		Sets the type of constant tone extension. The type specifies the CTE AoA/AoD method and for AoD the length of the
		switching and I/Q sampling slots. \n
			:param ctype: AOD1| AOA| AOD2 AOA AoA Constant Tone Extension AOD1 AoD Constant Tone Extension with 1 µs time slots AOD2 AoD Constant Tone Extension with 2 µs time slots
		"""
		param = Conversions.enum_scalar_to_str(ctype, enums.BtoCteType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CTYPe {param}')

	def get_dlength(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:DLENgth \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_dlength() \n
		Sets the payload data length in bytes. \n
			:return: dlength: integer Range: 0 to 255 (advertiser) or 251 (data)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:DLENgth?')
		return Conversions.str_to_int(response)

	def set_dlength(self, dlength: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:DLENgth \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_dlength(dlength = 1) \n
		Sets the payload data length in bytes. \n
			:param dlength: integer Range: 0 to 255 (advertiser) or 251 (data)
		"""
		param = Conversions.decimal_value_to_str(dlength)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:DLENgth {param}')

	def get_dwhitening(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:DWHitening \n
		Snippet: value: bool = driver.source.bb.btooth.econfiguration.pconfiguration.get_dwhitening() \n
		Activates or deactivates the Data Whitening. Evenly distributed white noise is ideal for the transmission and real data
		can be forced to look similar to white noise with different methods called Data Whitening. Applied to the PDU and CRC
		fields of all packet types, whitening is used to avoid long equal seqeunces in the data bit stream. \n
			:return: dwhitening: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:DWHitening?')
		return Conversions.str_to_bool(response)

	def set_dwhitening(self, dwhitening: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:DWHitening \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_dwhitening(dwhitening = False) \n
		Activates or deactivates the Data Whitening. Evenly distributed white noise is ideal for the transmission and real data
		can be forced to look similar to white noise with different methods called Data Whitening. Applied to the PDU and CRC
		fields of all packet types, whitening is used to avoid long equal seqeunces in the data bit stream. \n
			:param dwhitening: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(dwhitening)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:DWHitening {param}')

	# noinspection PyTypeChecker
	class EcodeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ecode: List[str]: numeric
			- Bit_Count: int: integer Range: 8 to 8"""
		__meta_args_list = [
			ArgStruct('Ecode', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ecode: List[str] = None
			self.Bit_Count: int = None

	def get_ecode(self) -> EcodeStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ECODe \n
		Snippet: value: EcodeStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_ecode() \n
		Sets the error code value to inform the remote device why the connection is about to be terminated in case of
		LL_TERMINATE_IND packet. On the other hand, this parameter for LL_REJECT_IND packet is used for the reason a request was
		rejected. A 8 bit value is set. Note: This parameter is relevant for data frame configuration and the packet type:
			INTRO_CMD_HELP: Selects the clock source: \n
			- LL_TERMINATE_IND
			- LL_REJECT_IND \n
			:return: structure: for return value, see the help for EcodeStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ECODe?', self.__class__.EcodeStruct())

	def set_ecode(self, value: EcodeStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ECODe \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_ecode(value = EcodeStruct()) \n
		Sets the error code value to inform the remote device why the connection is about to be terminated in case of
		LL_TERMINATE_IND packet. On the other hand, this parameter for LL_REJECT_IND packet is used for the reason a request was
		rejected. A 8 bit value is set. Note: This parameter is relevant for data frame configuration and the packet type:
			INTRO_CMD_HELP: Selects the clock source: \n
			- LL_TERMINATE_IND
			- LL_REJECT_IND \n
			:param value: see the help for EcodeStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ECODe', value)

	def get_ecounter(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ECOunter \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_ecounter() \n
		Counts the AUX_SYNC_IND packets that the SyncInfo field describes. \n
			:return: ecounter: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ECOunter?')
		return Conversions.str_to_int(response)

	def set_ecounter(self, ecounter: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ECOunter \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_ecounter(ecounter = 1) \n
		Counts the AUX_SYNC_IND packets that the SyncInfo field describes. \n
			:param ecounter: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(ecounter)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ECOunter {param}')

	# noinspection PyTypeChecker
	class EdiversifierStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ediversifier: List[str]: numeric
			- Bit_Count: int: integer Range: 16 to 16"""
		__meta_args_list = [
			ArgStruct('Ediversifier', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ediversifier: List[str] = None
			self.Bit_Count: int = None

	def get_ediversifier(self) -> EdiversifierStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:EDIVersifier \n
		Snippet: value: EdiversifierStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_ediversifier() \n
		Sets the encrypted diversifier of the master for device identification. The parameter is an initialization vector
		provided by the host in the HCI_ULP_Start_Encryption command. \n
			:return: structure: for return value, see the help for EdiversifierStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:EDIVersifier?', self.__class__.EdiversifierStruct())

	def set_ediversifier(self, value: EdiversifierStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:EDIVersifier \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_ediversifier(value = EdiversifierStruct()) \n
		Sets the encrypted diversifier of the master for device identification. The parameter is an initialization vector
		provided by the host in the HCI_ULP_Start_Encryption command. \n
			:param value: see the help for EdiversifierStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:EDIVersifier', value)

	def get_fs_length(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:FSLength \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_fs_length() \n
		Enables that the feature set length is indicated. \n
			:return: fs_length: integer Range: 1 to 26
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:FSLength?')
		return Conversions.str_to_int(response)

	def set_fs_length(self, fs_length: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:FSLength \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_fs_length(fs_length = 1) \n
		Enables that the feature set length is indicated. \n
			:param fs_length: integer Range: 1 to 26
		"""
		param = Conversions.decimal_value_to_str(fs_length)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:FSLength {param}')

	def get_hlength(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:HLENgth \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_hlength() \n
		(for data event and advertising frame configuration with the packet type CONNECT_IND) Sets the difference from the
		current channel to the next channel. The master and slave devices determine the data channel in use for every connection
		event from the channel map. Hop_length is set for the LL connection and communicated in the CONNECT_IND and
		LL_CHANNEL_MAP_IND packets. \n
			:return: hlength: integer Range: 5 to 16
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:HLENgth?')
		return Conversions.str_to_int(response)

	def set_hlength(self, hlength: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:HLENgth \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_hlength(hlength = 1) \n
		(for data event and advertising frame configuration with the packet type CONNECT_IND) Sets the difference from the
		current channel to the next channel. The master and slave devices determine the data channel in use for every connection
		event from the channel map. Hop_length is set for the LL connection and communicated in the CONNECT_IND and
		LL_CHANNEL_MAP_IND packets. \n
			:param hlength: integer Range: 5 to 16
		"""
		param = Conversions.decimal_value_to_str(hlength)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:HLENgth {param}')

	# noinspection PyTypeChecker
	class IcAssignedStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ic_Assigned: List[str]: No parameter help available
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Ic_Assigned', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ic_Assigned: List[str] = None
			self.Bit_Count: int = None

	def get_ic_assigned(self) -> IcAssignedStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ICASsigned \n
		Snippet: value: IcAssignedStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_ic_assigned() \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:return: structure: for return value, see the help for IcAssignedStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ICASsigned?', self.__class__.IcAssignedStruct())

	def set_ic_assigned(self, value: IcAssignedStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ICASsigned \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_ic_assigned(value = IcAssignedStruct()) \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:param value: see the help for IcAssignedStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ICASsigned', value)

	# noinspection PyTypeChecker
	class IcidStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Icid: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Icid', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Icid: List[str] = None
			self.Bit_Count: int = None

	def get_icid(self) -> IcidStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ICID \n
		Snippet: value: IcidStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_icid() \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:return: structure: for return value, see the help for IcidStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ICID?', self.__class__.IcidStruct())

	def set_icid(self, value: IcidStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ICID \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_icid(value = IcidStruct()) \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:param value: see the help for IcidStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ICID', value)

	# noinspection PyTypeChecker
	class IdStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Idn: List[str]: numeric
			- Bit_Count: int: integer Range: 16 to 16"""
		__meta_args_list = [
			ArgStruct('Idn', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Idn: List[str] = None
			self.Bit_Count: int = None

	def get_id(self) -> IdStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ID \n
		Snippet: value: IdStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_id() \n
		Specifies the ID in the CtrData field of the LL_PERIODIC_SYNC_IND PDU. \n
			:return: structure: for return value, see the help for IdStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ID?', self.__class__.IdStruct())

	def set_id(self, value: IdStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ID \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_id(value = IdStruct()) \n
		Specifies the ID in the CtrData field of the LL_PERIODIC_SYNC_IND PDU. \n
			:param value: see the help for IdStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ID', value)

	# noinspection PyTypeChecker
	class IlapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Lap: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Lap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lap: List[str] = None
			self.Bit_Count: int = None

	def get_ilap(self) -> IlapStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ILAP \n
		Snippet: value: IlapStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_ilap() \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner’s or
		initiator’s target device address to which the advertisement is directed ..:TLAP. \n
			:return: structure: for return value, see the help for IlapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ILAP?', self.__class__.IlapStruct())

	def set_ilap(self, value: IlapStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ILAP \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_ilap(value = IlapStruct()) \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner’s or
		initiator’s target device address to which the advertisement is directed ..:TLAP. \n
			:param value: see the help for IlapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ILAP', value)

	# noinspection PyTypeChecker
	class InuapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Nap_Uap: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Nap_Uap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Nap_Uap: List[str] = None
			self.Bit_Count: int = None

	def get_inuap(self) -> InuapStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:INUap \n
		Snippet: value: InuapStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_inuap() \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner’s or initiator’s target device address to which the advertisement is
		directed ..:TNUap. \n
			:return: structure: for return value, see the help for InuapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:INUap?', self.__class__.InuapStruct())

	def set_inuap(self, value: InuapStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:INUap \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_inuap(value = InuapStruct()) \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner’s or initiator’s target device address to which the advertisement is
		directed ..:TNUap. \n
			:param value: see the help for InuapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:INUap', value)

	def get_lc_timeout(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:LCTimeout \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_lc_timeout() \n
		Defines the maximum time between two correctly received Bluetooth LE packets in the LL connection before the connection
		is considered lost for the packet type CONNECT_IND. Command sets the values in ms. Query returns values in s. \n
			:return: lc_timeout: float Range: 100E-3 s to 32000E-3 s , Unit: ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:LCTimeout?')
		return Conversions.str_to_float(response)

	def set_lc_timeout(self, lc_timeout: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:LCTimeout \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_lc_timeout(lc_timeout = 1.0) \n
		Defines the maximum time between two correctly received Bluetooth LE packets in the LL connection before the connection
		is considered lost for the packet type CONNECT_IND. Command sets the values in ms. Query returns values in s. \n
			:param lc_timeout: float Range: 100E-3 s to 32000E-3 s , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(lc_timeout)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:LCTimeout {param}')

	def get_lpe_counter(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:LPECounter \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_lpe_counter() \n
		Specifies the lastPaEventCounter field in the CtrData field of the LL_PERIODIC_SYNC_IND PDU. \n
			:return: lpecounter: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:LPECounter?')
		return Conversions.str_to_int(response)

	def set_lpe_counter(self, lpecounter: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:LPECounter \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_lpe_counter(lpecounter = 1) \n
		Specifies the lastPaEventCounter field in the CtrData field of the LL_PERIODIC_SYNC_IND PDU. \n
			:param lpecounter: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(lpecounter)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:LPECounter {param}')

	def get_mcl_req(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MCLReq \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_mcl_req() \n
		Specifies the minimum CTE length in the CtrData field of the LL_CTE_Req PDU. \n
			:return: mcl_req: float Range: 16E-6 to 160E-6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MCLReq?')
		return Conversions.str_to_float(response)

	def set_mcl_req(self, mcl_req: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MCLReq \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_mcl_req(mcl_req = 1.0) \n
		Specifies the minimum CTE length in the CtrData field of the LL_CTE_Req PDU. \n
			:param mcl_req: float Range: 16E-6 to 160E-6
		"""
		param = Conversions.decimal_value_to_str(mcl_req)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MCLReq {param}')

	# noinspection PyTypeChecker
	class MiVectorStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Mi_Vector: List[str]: No parameter help available
			- Bit_Count: int: integer Range: 32 to 32"""
		__meta_args_list = [
			ArgStruct('Mi_Vector', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mi_Vector: List[str] = None
			self.Bit_Count: int = None

	def get_mi_vector(self) -> MiVectorStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MIVector \n
		Snippet: value: MiVectorStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_mi_vector() \n
		Sets the master's or the slave's portion of the initialization vector (IVm/IVs) . \n
			:return: structure: for return value, see the help for MiVectorStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MIVector?', self.__class__.MiVectorStruct())

	def set_mi_vector(self, value: MiVectorStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MIVector \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_mi_vector(value = MiVectorStruct()) \n
		Sets the master's or the slave's portion of the initialization vector (IVm/IVs) . \n
			:param value: see the help for MiVectorStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MIVector', value)

	def get_mn_interval(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MNINterval \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_mn_interval() \n
		Specifies the minimum allowed connection interval. Command sets the values in ms. Query returns values in s. \n
			:return: mn_interval: float Range: 7.5E-3 s to depending on Max. Interval
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MNINterval?')
		return Conversions.str_to_float(response)

	def set_mn_interval(self, mn_interval: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MNINterval \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_mn_interval(mn_interval = 1.0) \n
		Specifies the minimum allowed connection interval. Command sets the values in ms. Query returns values in s. \n
			:param mn_interval: float Range: 7.5E-3 s to depending on Max. Interval
		"""
		param = Conversions.decimal_value_to_str(mn_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MNINterval {param}')

	def get_mr_octets(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MROCtets \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_mr_octets() \n
		Specifies the maximum allowed payload length of a packet to be received (..:MROCtets) or transmitted (..:MTOCtets) .
		Information is signaled via LL_LENGTH_REQ and LL_LENGTH_RSP. \n
			:return: mr_octets: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MROCtets?')
		return Conversions.str_to_int(response)

	def set_mr_octets(self, mr_octets: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MROCtets \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_mr_octets(mr_octets = 1) \n
		Specifies the maximum allowed payload length of a packet to be received (..:MROCtets) or transmitted (..:MTOCtets) .
		Information is signaled via LL_LENGTH_REQ and LL_LENGTH_RSP. \n
			:param mr_octets: integer Range: 27 to 251
		"""
		param = Conversions.decimal_value_to_str(mr_octets)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MROCtets {param}')

	def get_mr_time(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MRTime \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_mr_time() \n
		Specifies the maximum allowed time to receive (..:MRTime) or transmit (..:MTTime) a packet. Information is signaled via
		LL_LENGTH_REQ and LL_LENGTH_RSP. \n
			:return: mrtime: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MRTime?')
		return Conversions.str_to_float(response)

	def set_mr_time(self, mrtime: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MRTime \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_mr_time(mrtime = 1.0) \n
		Specifies the maximum allowed time to receive (..:MRTime) or transmit (..:MTTime) a packet. Information is signaled via
		LL_LENGTH_REQ and LL_LENGTH_RSP. \n
			:param mrtime: float Range: 0.328E-3 to 17.04E-3
		"""
		param = Conversions.decimal_value_to_str(mrtime)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MRTime {param}')

	# noinspection PyTypeChecker
	class MskdStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Mskd: List[str]: No parameter help available
			- Bit_Count: int: integer Range: 64 to 64"""
		__meta_args_list = [
			ArgStruct('Mskd', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mskd: List[str] = None
			self.Bit_Count: int = None

	def get_mskd(self) -> MskdStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MSKD \n
		Snippet: value: MskdStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_mskd() \n
		Sets the master's or the slave's portion of the session key diversifier (SKDm/SKDs) . \n
			:return: structure: for return value, see the help for MskdStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MSKD?', self.__class__.MskdStruct())

	def set_mskd(self, value: MskdStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MSKD \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_mskd(value = MskdStruct()) \n
		Sets the master's or the slave's portion of the session key diversifier (SKDm/SKDs) . \n
			:param value: see the help for MskdStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MSKD', value)

	def get_mt_octets(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MTOCtets \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_mt_octets() \n
		Specifies the maximum allowed payload length of a packet to be received (..:MROCtets) or transmitted (..:MTOCtets) .
		Information is signaled via LL_LENGTH_REQ and LL_LENGTH_RSP. \n
			:return: mt_octets: integer Range: 27 to 251
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MTOCtets?')
		return Conversions.str_to_int(response)

	def set_mt_octets(self, mt_octets: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MTOCtets \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_mt_octets(mt_octets = 1) \n
		Specifies the maximum allowed payload length of a packet to be received (..:MROCtets) or transmitted (..:MTOCtets) .
		Information is signaled via LL_LENGTH_REQ and LL_LENGTH_RSP. \n
			:param mt_octets: integer Range: 27 to 251
		"""
		param = Conversions.decimal_value_to_str(mt_octets)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MTOCtets {param}')

	def get_mt_time(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MTTime \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_mt_time() \n
		Specifies the maximum allowed time to receive (..:MRTime) or transmit (..:MTTime) a packet. Information is signaled via
		LL_LENGTH_REQ and LL_LENGTH_RSP. \n
			:return: mttime: float Range: 0.328E-3 to 17.04E-3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MTTime?')
		return Conversions.str_to_float(response)

	def set_mt_time(self, mttime: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MTTime \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_mt_time(mttime = 1.0) \n
		Specifies the maximum allowed time to receive (..:MRTime) or transmit (..:MTTime) a packet. Information is signaled via
		LL_LENGTH_REQ and LL_LENGTH_RSP. \n
			:param mttime: float Range: 0.328E-3 to 17.04E-3
		"""
		param = Conversions.decimal_value_to_str(mttime)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MTTime {param}')

	def get_mu_channels(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MUCHannels \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_mu_channels() \n
		Specifies the minimum number of channels to be used on the specified PHYs, see method RsSmbv.Source.Bb.Btooth.
		Econfiguration.Pconfiguration.Phys.L1M.State.set etc. \n
			:return: muchannels: integer Range: 2 to 37
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MUCHannels?')
		return Conversions.str_to_int(response)

	def set_mu_channels(self, muchannels: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MUCHannels \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_mu_channels(muchannels = 1) \n
		Specifies the minimum number of channels to be used on the specified PHYs, see method RsSmbv.Source.Bb.Btooth.
		Econfiguration.Pconfiguration.Phys.L1M.State.set etc. \n
			:param muchannels: integer Range: 2 to 37
		"""
		param = Conversions.decimal_value_to_str(muchannels)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MUCHannels {param}')

	def get_mx_interval(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MXINterval \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_mx_interval() \n
		Specifies the maximum allowed connection interval. Command sets the values in ms. Query returns values in s. \n
			:return: minterval: float Range: 7.5E-3 s to 4000E-3 s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MXINterval?')
		return Conversions.str_to_float(response)

	def set_mx_interval(self, minterval: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MXINterval \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_mx_interval(minterval = 1.0) \n
		Specifies the maximum allowed connection interval. Command sets the values in ms. Query returns values in s. \n
			:param minterval: float Range: 7.5E-3 s to 4000E-3 s
		"""
		param = Conversions.decimal_value_to_str(minterval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MXINterval {param}')

	def get_nc_interval(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NCINterval \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_nc_interval() \n
		Sets the time interval new connection events for the packet types CONNECT_IND and LL_CONNECTION_UPDATE_IND. Command sets
		the values in ms. Query returns values in s. \n
			:return: nc_interval: float Range: 7.5E-3 s to depends on oversampling , Unit: ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NCINterval?')
		return Conversions.str_to_float(response)

	def set_nc_interval(self, nc_interval: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NCINterval \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_nc_interval(nc_interval = 1.0) \n
		Sets the time interval new connection events for the packet types CONNECT_IND and LL_CONNECTION_UPDATE_IND. Command sets
		the values in ms. Query returns values in s. \n
			:param nc_interval: float Range: 7.5E-3 s to depends on oversampling , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(nc_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NCINterval {param}')

	def get_nlc_timeout(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NLCTimeout \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_nlc_timeout() \n
		Defines the maximum time between two correctly received Bluetooth LE packets in the LL connection before the connection
		is considered lost only for the packet type LL_CONNECTION_UPDATE_IND. Command sets the values in ms. Query returns values
		in s. \n
			:return: nlc_timeout: float Range: 100E-3 s to 32000E-3 s , Unit: ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NLCTimeout?')
		return Conversions.str_to_float(response)

	def set_nlc_timeout(self, nlc_timeout: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NLCTimeout \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_nlc_timeout(nlc_timeout = 1.0) \n
		Defines the maximum time between two correctly received Bluetooth LE packets in the LL connection before the connection
		is considered lost only for the packet type LL_CONNECTION_UPDATE_IND. Command sets the values in ms. Query returns values
		in s. \n
			:param nlc_timeout: float Range: 100E-3 s to 32000E-3 s , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(nlc_timeout)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NLCTimeout {param}')

	def get_ns_latency(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NSLatency \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_ns_latency() \n
		(for data event and advertising frame configuration with the packet type LL_CONNECTION_UPDATE_IND) Sets the number of
		consecutive connection events the slave can ignore for asymmetric link layer connections. \n
			:return: ns_latency: integer Range: 0 to depends on LL connection timeout and connection event interval
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NSLatency?')
		return Conversions.str_to_int(response)

	def set_ns_latency(self, ns_latency: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NSLatency \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_ns_latency(ns_latency = 1) \n
		(for data event and advertising frame configuration with the packet type LL_CONNECTION_UPDATE_IND) Sets the number of
		consecutive connection events the slave can ignore for asymmetric link layer connections. \n
			:param ns_latency: integer Range: 0 to depends on LL connection timeout and connection event interval
		"""
		param = Conversions.decimal_value_to_str(ns_latency)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NSLatency {param}')

	def get_nsvalue(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NSValue \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_nsvalue() \n
		Sets the start value of the next expected packet from the same device in the LL connection ('N'ext'E'xpected
		'S'equence'N'umber) . This parameter can be set in the first event. From the second event this field is not indicated. \n
			:return: ns_value: integer Range: 0 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NSValue?')
		return Conversions.str_to_int(response)

	def set_nsvalue(self, ns_value: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NSValue \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_nsvalue(ns_value = 1) \n
		Sets the start value of the next expected packet from the same device in the LL connection ('N'ext'E'xpected
		'S'equence'N'umber) . This parameter can be set in the first event. From the second event this field is not indicated. \n
			:param ns_value: integer Range: 0 to 1
		"""
		param = Conversions.decimal_value_to_str(ns_value)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NSValue {param}')

	def get_nw_offset(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NWOFfset \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_nw_offset() \n
		Sets the start point of the transmit window for data event and advertising frame configuration with the packet type
		LL_CONNECTION_UPDATE_IND. Command sets the values in ms. Query returns values in s. \n
			:return: nw_offset: float Range: 0 s to depends on connection event interval , Unit: ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NWOFfset?')
		return Conversions.str_to_float(response)

	def set_nw_offset(self, nw_offset: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NWOFfset \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_nw_offset(nw_offset = 1.0) \n
		Sets the start point of the transmit window for data event and advertising frame configuration with the packet type
		LL_CONNECTION_UPDATE_IND. Command sets the values in ms. Query returns values in s. \n
			:param nw_offset: float Range: 0 s to depends on connection event interval , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(nw_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NWOFfset {param}')

	def get_nw_size(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NWSize \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_nw_size() \n
		Sets the size of the transmit window, regarding to the start point for data event and advertising frame configuration
		with the packet type LL_CONNECTION_UPDATE_IND. \n
			:return: nw_size: float Range: 1.25E-3 to depends on connection event interval
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NWSize?')
		return Conversions.str_to_float(response)

	def set_nw_size(self, nw_size: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NWSize \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_nw_size(nw_size = 1.0) \n
		Sets the size of the transmit window, regarding to the start point for data event and advertising frame configuration
		with the packet type LL_CONNECTION_UPDATE_IND. \n
			:param nw_size: float Range: 1.25E-3 to depends on connection event interval
		"""
		param = Conversions.decimal_value_to_str(nw_size)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NWSize {param}')

	def get_oadjust(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:OADJust \n
		Snippet: value: bool = driver.source.bb.btooth.econfiguration.pconfiguration.get_oadjust() \n
		Adjusts the 'Sync Packet Offset' automatically to the next value, which is a multiple of the ''Offset Units'. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:OADJust?')
		return Conversions.str_to_bool(response)

	def set_oadjust(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:OADJust \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_oadjust(state = False) \n
		Adjusts the 'Sync Packet Offset' automatically to the next value, which is a multiple of the ''Offset Units'. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:OADJust {param}')

	def get_pa_interval(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:PAINterval \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_pa_interval() \n
		Sets the time interval between the start of two AUX_SYNC_IND PDUs from the same advertising set. Command sets the values
		in ms. Query returns values in s. \n
			:return: interval: float Range: 7.5E-3 s to depending on oversampling , Unit: ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:PAINterval?')
		return Conversions.str_to_float(response)

	def set_pa_interval(self, interval: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:PAINterval \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_pa_interval(interval = 1.0) \n
		Sets the time interval between the start of two AUX_SYNC_IND PDUs from the same advertising set. Command sets the values
		in ms. Query returns values in s. \n
			:param interval: float Range: 7.5E-3 s to depending on oversampling , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:PAINterval {param}')

	def get_pperiodicity(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:PPERiodicity \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_pperiodicity() \n
		Specifies a value the connection interval is preferred to be a multiple of. \n
			:return: pp_eriodicity: float Range: 0 to depends on Max. Interval
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:PPERiodicity?')
		return Conversions.str_to_float(response)

	def set_pperiodicity(self, pp_eriodicity: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:PPERiodicity \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_pperiodicity(pp_eriodicity = 1.0) \n
		Specifies a value the connection interval is preferred to be a multiple of. \n
			:param pp_eriodicity: float Range: 0 to depends on Max. Interval
		"""
		param = Conversions.decimal_value_to_str(pp_eriodicity)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:PPERiodicity {param}')

	# noinspection PyTypeChecker
	def get_ratype(self) -> enums.BtoUlpAddrType:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:RATYpe \n
		Snippet: value: enums.BtoUlpAddrType = driver.source.bb.btooth.econfiguration.pconfiguration.get_ratype() \n
		Selects the address type of the controller device. Depending on the Bluetooth controller role either Tx or Rx or both
		address types are assigned. Subdivided into private and random, a Bluetooth LE device address consits of 48 bits.
		The format of the device address differs depending on the selected address type. \n
			:return: ra_type: PUBLic| RANDom PUBlic Allocates a unique 48 bit address to each Bluetooth LE device. The public address is given from the registration authority IEEE. RANDom Allocates a 48-bit address to each Bluetooth LE device. A random address is optional.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:RATYpe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoUlpAddrType)

	def set_ratype(self, ra_type: enums.BtoUlpAddrType) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:RATYpe \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_ratype(ra_type = enums.BtoUlpAddrType.PUBLic) \n
		Selects the address type of the controller device. Depending on the Bluetooth controller role either Tx or Rx or both
		address types are assigned. Subdivided into private and random, a Bluetooth LE device address consits of 48 bits.
		The format of the device address differs depending on the selected address type. \n
			:param ra_type: PUBLic| RANDom PUBlic Allocates a unique 48 bit address to each Bluetooth LE device. The public address is given from the registration authority IEEE. RANDom Allocates a 48-bit address to each Bluetooth LE device. A random address is optional.
		"""
		param = Conversions.enum_scalar_to_str(ra_type, enums.BtoUlpAddrType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:RATYpe {param}')

	def get_rce_count(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:RCECount \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_rce_count() \n
		Specifies the ReferenceConnEventCount field of LL_CONNECTION_PARAM_REQ. \n
			:return: rce_count: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:RCECount?')
		return Conversions.str_to_int(response)

	def set_rce_count(self, rce_count: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:RCECount \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_rce_count(rce_count = 1) \n
		Specifies the ReferenceConnEventCount field of LL_CONNECTION_PARAM_REQ. \n
			:param rce_count: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(rce_count)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:RCECount {param}')

	# noinspection PyTypeChecker
	class RopcodeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Rop_Code: List[str]: numeric
			- Bit_Count: int: integer Range: 8 to 8"""
		__meta_args_list = [
			ArgStruct('Rop_Code', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rop_Code: List[str] = None
			self.Bit_Count: int = None

	def get_ropcode(self) -> RopcodeStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ROPCode \n
		Snippet: value: RopcodeStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_ropcode() \n
		Specifies the Opcode of rejected LL control PDU. information is signaled via LL_REJECT_EXT_IND. \n
			:return: structure: for return value, see the help for RopcodeStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ROPCode?', self.__class__.RopcodeStruct())

	def set_ropcode(self, value: RopcodeStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ROPCode \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_ropcode(value = RopcodeStruct()) \n
		Specifies the Opcode of rejected LL control PDU. information is signaled via LL_REJECT_EXT_IND. \n
			:param value: see the help for RopcodeStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ROPCode', value)

	# noinspection PyTypeChecker
	class RvectorStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Rvector: List[str]: numeric
			- Bit_Count: int: integer Range: 64 to 64"""
		__meta_args_list = [
			ArgStruct('Rvector', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rvector: List[str] = None
			self.Bit_Count: int = None

	def get_rvector(self) -> RvectorStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:RVECtor \n
		Snippet: value: RvectorStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_rvector() \n
		Sets the random vector of the master for device identification.The parameter is an initialization vector provided by the
		Host in the HCI_ULP_Start_Encryption command. \n
			:return: structure: for return value, see the help for RvectorStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:RVECtor?', self.__class__.RvectorStruct())

	def set_rvector(self, value: RvectorStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:RVECtor \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_rvector(value = RvectorStruct()) \n
		Sets the random vector of the master for device identification.The parameter is an initialization vector provided by the
		Host in the HCI_ULP_Start_Encryption command. \n
			:param value: see the help for RvectorStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:RVECtor', value)

	# noinspection PyTypeChecker
	def get_sc_accuracy(self) -> enums.BtoSlpClckAccrcy:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SCACcuracy \n
		Snippet: value: enums.BtoSlpClckAccrcy = driver.source.bb.btooth.econfiguration.pconfiguration.get_sc_accuracy() \n
		Defines the master´s clock accuracy with specified encoding. This parameter is used by the slave to determine required
		listening windows in the LL connection. It is a controller design parameter known by the Controller. \n
			:return: sc_accuracy: SCA0| SCA1| SCA2| SCA3| SCA4| SCA5| SCA6| SCA7
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SCACcuracy?')
		return Conversions.str_to_scalar_enum(response, enums.BtoSlpClckAccrcy)

	def set_sc_accuracy(self, sc_accuracy: enums.BtoSlpClckAccrcy) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SCACcuracy \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_sc_accuracy(sc_accuracy = enums.BtoSlpClckAccrcy.SCA0) \n
		Defines the master´s clock accuracy with specified encoding. This parameter is used by the slave to determine required
		listening windows in the LL connection. It is a controller design parameter known by the Controller. \n
			:param sc_accuracy: SCA0| SCA1| SCA2| SCA3| SCA4| SCA5| SCA6| SCA7
		"""
		param = Conversions.enum_scalar_to_str(sc_accuracy, enums.BtoSlpClckAccrcy)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SCACcuracy {param}')

	# noinspection PyTypeChecker
	class ScAssignedStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Sc_Assigned: List[str]: No parameter help available
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Sc_Assigned', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sc_Assigned: List[str] = None
			self.Bit_Count: int = None

	def get_sc_assigned(self) -> ScAssignedStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SCASsigned \n
		Snippet: value: ScAssignedStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_sc_assigned() \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:return: structure: for return value, see the help for ScAssignedStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SCASsigned?', self.__class__.ScAssignedStruct())

	def set_sc_assigned(self, value: ScAssignedStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SCASsigned \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_sc_assigned(value = ScAssignedStruct()) \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:param value: see the help for ScAssignedStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SCASsigned', value)

	def get_sce_counter(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SCECounter \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_sce_counter() \n
		No command help available \n
			:return: sce_counter: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SCECounter?')
		return Conversions.str_to_int(response)

	def set_sce_counter(self, sce_counter: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SCECounter \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_sce_counter(sce_counter = 1) \n
		No command help available \n
			:param sce_counter: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(sce_counter)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SCECounter {param}')

	# noinspection PyTypeChecker
	class ScidStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Scid: List[str]: No parameter help available
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Scid', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Scid: List[str] = None
			self.Bit_Count: int = None

	def get_scid(self) -> ScidStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SCID \n
		Snippet: value: ScidStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_scid() \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:return: structure: for return value, see the help for ScidStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SCID?', self.__class__.ScidStruct())

	def set_scid(self, value: ScidStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SCID \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_scid(value = ScidStruct()) \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:param value: see the help for ScidStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SCID', value)

	# noinspection PyTypeChecker
	class SidStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Sid: List[str]: numeric
			- Bit_Count: int: integer Range: 4 to 4"""
		__meta_args_list = [
			ArgStruct('Sid', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sid: List[str] = None
			self.Bit_Count: int = None

	def get_sid(self) -> SidStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SID \n
		Snippet: value: SidStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_sid() \n
		Specifies the SID in the CtrData field of the LL_PERIODIC_SYNC_IND. \n
			:return: structure: for return value, see the help for SidStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SID?', self.__class__.SidStruct())

	def set_sid(self, value: SidStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SID \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_sid(value = SidStruct()) \n
		Specifies the SID in the CtrData field of the LL_PERIODIC_SYNC_IND. \n
			:param value: see the help for SidStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SID', value)

	# noinspection PyTypeChecker
	class SivectorStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Si_Vector: List[str]: numeric
			- Bit_Count: int: integer Range: 32 to 32"""
		__meta_args_list = [
			ArgStruct('Si_Vector', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Si_Vector: List[str] = None
			self.Bit_Count: int = None

	def get_sivector(self) -> SivectorStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SIVector \n
		Snippet: value: SivectorStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_sivector() \n
		Sets the master's or the slave's portion of the initialization vector (IVm/IVs) . \n
			:return: structure: for return value, see the help for SivectorStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SIVector?', self.__class__.SivectorStruct())

	def set_sivector(self, value: SivectorStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SIVector \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_sivector(value = SivectorStruct()) \n
		Sets the master's or the slave's portion of the initialization vector (IVm/IVs) . \n
			:param value: see the help for SivectorStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SIVector', value)

	# noinspection PyTypeChecker
	class SlapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Lap: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Lap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lap: List[str] = None
			self.Bit_Count: int = None

	def get_slap(self) -> SlapStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SLAP \n
		Snippet: value: SlapStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_slap() \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner’s or
		initiator’s target device address to which the advertisement is directed ..:TLAP. \n
			:return: structure: for return value, see the help for SlapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SLAP?', self.__class__.SlapStruct())

	def set_slap(self, value: SlapStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SLAP \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_slap(value = SlapStruct()) \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner’s or
		initiator’s target device address to which the advertisement is directed ..:TLAP. \n
			:param value: see the help for SlapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SLAP', value)

	def get_slatency(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SLATency \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_slatency() \n
		(For data event and advertising frame configuration with the packet type CONNECT_IND) Sets the number of consecutive
		connection events the slave can ignore for asymmetric link layer connections. \n
			:return: slatency: integer Range: 0 to depends on LL connection timeout and connection event interval
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SLATency?')
		return Conversions.str_to_int(response)

	def set_slatency(self, slatency: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SLATency \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_slatency(slatency = 1) \n
		(For data event and advertising frame configuration with the packet type CONNECT_IND) Sets the number of consecutive
		connection events the slave can ignore for asymmetric link layer connections. \n
			:param slatency: integer Range: 0 to depends on LL connection timeout and connection event interval
		"""
		param = Conversions.decimal_value_to_str(slatency)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SLATency {param}')

	# noinspection PyTypeChecker
	class SnuapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Nap_Uap: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Nap_Uap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Nap_Uap: List[str] = None
			self.Bit_Count: int = None

	def get_snuap(self) -> SnuapStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SNUap \n
		Snippet: value: SnuapStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_snuap() \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner’s or initiator’s target device address to which the advertisement is
		directed ..:TNUap. \n
			:return: structure: for return value, see the help for SnuapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SNUap?', self.__class__.SnuapStruct())

	def set_snuap(self, value: SnuapStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SNUap \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_snuap(value = SnuapStruct()) \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner’s or initiator’s target device address to which the advertisement is
		directed ..:TNUap. \n
			:param value: see the help for SnuapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SNUap', value)

	# noinspection PyTypeChecker
	def get_sounits(self) -> enums.BtoOffsUnit:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SOUNits \n
		Snippet: value: enums.BtoOffsUnit = driver.source.bb.btooth.econfiguration.pconfiguration.get_sounits() \n
		Indicates the units used by the 'Sync Packet Offset' parameter, see method RsSmbv.Source.Bb.Btooth.Econfiguration.
		Pconfiguration.spOffset \n
			:return: unit: U30| U300 U30 30 µs U300 300 µs
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SOUNits?')
		return Conversions.str_to_scalar_enum(response, enums.BtoOffsUnit)

	def set_sounits(self, unit: enums.BtoOffsUnit) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SOUNits \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_sounits(unit = enums.BtoOffsUnit.U30) \n
		Indicates the units used by the 'Sync Packet Offset' parameter, see method RsSmbv.Source.Bb.Btooth.Econfiguration.
		Pconfiguration.spOffset \n
			:param unit: U30| U300 U30 30 µs U300 300 µs
		"""
		param = Conversions.enum_scalar_to_str(unit, enums.BtoOffsUnit)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SOUNits {param}')

	# noinspection PyTypeChecker
	def get_spbit(self) -> enums.BtoSymPerBit:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SPBit \n
		Snippet: value: enums.BtoSymPerBit = driver.source.bb.btooth.econfiguration.pconfiguration.get_spbit() \n
		Specifies a coding for LE coded packets. The specification for Bluetooth wireless technology defines two values S for
		forward error correction: S = 2 symbol/bit and S = 8 symbol/bit. \n
			:return: spb: TWO| EIGHt
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SPBit?')
		return Conversions.str_to_scalar_enum(response, enums.BtoSymPerBit)

	def set_spbit(self, spb: enums.BtoSymPerBit) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SPBit \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_spbit(spb = enums.BtoSymPerBit.EIGHt) \n
		Specifies a coding for LE coded packets. The specification for Bluetooth wireless technology defines two values S for
		forward error correction: S = 2 symbol/bit and S = 8 symbol/bit. \n
			:param spb: TWO| EIGHt
		"""
		param = Conversions.enum_scalar_to_str(spb, enums.BtoSymPerBit)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SPBit {param}')

	def get_sp_offset(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SPOFfset \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_sp_offset() \n
		Specifies the time from the start of the AUX_ADV_IND packet containing the SyncInfo field to the start of the
		AUX_SYNC_IND packet. The offset is determined by multiplying the value by the unit, see method RsSmbv.Source.Bb.Btooth.
		Econfiguration.Pconfiguration.sounits \n
			:return: sp_offset: float Range: 0 to 245.7 or 246 to 2457 depending on offset unit
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SPOFfset?')
		return Conversions.str_to_float(response)

	def set_sp_offset(self, sp_offset: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SPOFfset \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_sp_offset(sp_offset = 1.0) \n
		Specifies the time from the start of the AUX_ADV_IND packet containing the SyncInfo field to the start of the
		AUX_SYNC_IND packet. The offset is determined by multiplying the value by the unit, see method RsSmbv.Source.Bb.Btooth.
		Econfiguration.Pconfiguration.sounits \n
			:param sp_offset: float Range: 0 to 245.7 or 246 to 2457 depending on offset unit
		"""
		param = Conversions.decimal_value_to_str(sp_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SPOFfset {param}')

	# noinspection PyTypeChecker
	class SskdStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Sskd: List[str]: numeric
			- Bit_Count: int: integer Range: 64 to 64"""
		__meta_args_list = [
			ArgStruct('Sskd', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sskd: List[str] = None
			self.Bit_Count: int = None

	def get_sskd(self) -> SskdStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SSKD \n
		Snippet: value: SskdStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_sskd() \n
		Sets the master's or the slave's portion of the session key diversifier (SKDm/SKDs) . \n
			:return: structure: for return value, see the help for SskdStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SSKD?', self.__class__.SskdStruct())

	def set_sskd(self, value: SskdStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SSKD \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_sskd(value = SskdStruct()) \n
		Sets the master's or the slave's portion of the session key diversifier (SKDm/SKDs) . \n
			:param value: see the help for SskdStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SSKD', value)

	def get_ss_value(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SSValue \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_ss_value() \n
		Sets the sequence number of the packet. This parameter can be set in the first event. From the second event, this field
		is not indicated. \n
			:return: ss_value: integer Range: 0 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SSValue?')
		return Conversions.str_to_int(response)

	def set_ss_value(self, ss_value: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SSValue \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_ss_value(ss_value = 1) \n
		Sets the sequence number of the packet. This parameter can be set in the first event. From the second event, this field
		is not indicated. \n
			:param ss_value: integer Range: 0 to 1
		"""
		param = Conversions.decimal_value_to_str(ss_value)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SSValue {param}')

	# noinspection PyTypeChecker
	class SvnumberStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Sv_Number: List[str]: numeric
			- Bit_Count: int: integer Range: 16 to 16"""
		__meta_args_list = [
			ArgStruct('Sv_Number', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sv_Number: List[str] = None
			self.Bit_Count: int = None

	def get_svnumber(self) -> SvnumberStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SVNumber \n
		Snippet: value: SvnumberStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_svnumber() \n
		Sets a unique value for each implementation or revision of an implementation of the Bluetooth Controller. A 16 bit value
		is set. Note: This parameter is relevant for data frame configuration and for the packet type: LL_VERSION_IND. \n
			:return: structure: for return value, see the help for SvnumberStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SVNumber?', self.__class__.SvnumberStruct())

	def set_svnumber(self, value: SvnumberStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SVNumber \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_svnumber(value = SvnumberStruct()) \n
		Sets a unique value for each implementation or revision of an implementation of the Bluetooth Controller. A 16 bit value
		is set. Note: This parameter is relevant for data frame configuration and for the packet type: LL_VERSION_IND. \n
			:param value: see the help for SvnumberStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SVNumber', value)

	# noinspection PyTypeChecker
	def get_ta_type(self) -> enums.BtoUlpAddrType:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:TATYpe \n
		Snippet: value: enums.BtoUlpAddrType = driver.source.bb.btooth.econfiguration.pconfiguration.get_ta_type() \n
		Selects the address type of the controller device. Depending on the Bluetooth controller role either Tx or Rx or both
		address types are assigned. Subdivided into private and random, a Bluetooth LE device address consits of 48 bits.
		The format of the device address differs depending on the selected address type. \n
			:return: ta_type: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:TATYpe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoUlpAddrType)

	def set_ta_type(self, ta_type: enums.BtoUlpAddrType) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:TATYpe \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_ta_type(ta_type = enums.BtoUlpAddrType.PUBLic) \n
		Selects the address type of the controller device. Depending on the Bluetooth controller role either Tx or Rx or both
		address types are assigned. Subdivided into private and random, a Bluetooth LE device address consits of 48 bits.
		The format of the device address differs depending on the selected address type. \n
			:param ta_type: PUBLic| RANDom PUBlic Allocates a unique 48 bit address to each Bluetooth LE device. The public address is given from the registration authority IEEE. RANDom Allocates a 48-bit address to each Bluetooth LE device. A random address is optional.
		"""
		param = Conversions.enum_scalar_to_str(ta_type, enums.BtoUlpAddrType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:TATYpe {param}')

	# noinspection PyTypeChecker
	class TlapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Lap: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Lap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lap: List[str] = None
			self.Bit_Count: int = None

	def get_tlap(self) -> TlapStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:TLAP \n
		Snippet: value: TlapStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_tlap() \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner’s or
		initiator’s target device address to which the advertisement is directed ..:TLAP. \n
			:return: structure: for return value, see the help for TlapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:TLAP?', self.__class__.TlapStruct())

	def set_tlap(self, value: TlapStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:TLAP \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_tlap(value = TlapStruct()) \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner’s or
		initiator’s target device address to which the advertisement is directed ..:TLAP. \n
			:param value: see the help for TlapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:TLAP', value)

	# noinspection PyTypeChecker
	class TnuapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Nap_Uap: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Nap_Uap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Nap_Uap: List[str] = None
			self.Bit_Count: int = None

	def get_tnuap(self) -> TnuapStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:TNUap \n
		Snippet: value: TnuapStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_tnuap() \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner’s or initiator’s target device address to which the advertisement is
		directed ..:TNUap. \n
			:return: structure: for return value, see the help for TnuapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:TNUap?', self.__class__.TnuapStruct())

	def set_tnuap(self, value: TnuapStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:TNUap \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_tnuap(value = TnuapStruct()) \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner’s or initiator’s target device address to which the advertisement is
		directed ..:TNUap. \n
			:param value: see the help for TnuapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:TNUap', value)

	def get_tpower(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:TPOWer \n
		Snippet: value: int = driver.source.bb.btooth.econfiguration.pconfiguration.get_tpower() \n
		Sets the required transmit power to be signaled within an extended header. \n
			:return: tpower: integer Range: -127 to 126
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:TPOWer?')
		return Conversions.str_to_int(response)

	def set_tpower(self, tpower: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:TPOWer \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_tpower(tpower = 1) \n
		Sets the required transmit power to be signaled within an extended header. \n
			:param tpower: integer Range: -127 to 126
		"""
		param = Conversions.decimal_value_to_str(tpower)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:TPOWer {param}')

	# noinspection PyTypeChecker
	class UtypeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Utype: List[str]: numeric
			- Bit_Count: int: integer Range: 8 to 8"""
		__meta_args_list = [
			ArgStruct('Utype', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Utype: List[str] = None
			self.Bit_Count: int = None

	def get_utype(self) -> UtypeStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:UTYPe \n
		Snippet: value: UtypeStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_utype() \n
		Enables that an invalid control packet is indicated. The CtrType field indicates the value of the LL control packet that
		caused the transmission of this packet. \n
			:return: structure: for return value, see the help for UtypeStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:UTYPe?', self.__class__.UtypeStruct())

	def set_utype(self, value: UtypeStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:UTYPe \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_utype(value = UtypeStruct()) \n
		Enables that an invalid control packet is indicated. The CtrType field indicates the value of the LL control packet that
		caused the transmission of this packet. \n
			:param value: see the help for UtypeStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:UTYPe', value)

	# noinspection PyTypeChecker
	class VnumberStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Vnumber: List[str]: numeric
			- Bit_Count: int: integer Range: 8 to 8"""
		__meta_args_list = [
			ArgStruct('Vnumber', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Vnumber: List[str] = None
			self.Bit_Count: int = None

	def get_vnumber(self) -> VnumberStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:VNUMber \n
		Snippet: value: VnumberStruct = driver.source.bb.btooth.econfiguration.pconfiguration.get_vnumber() \n
		Sets the company identifier of the manufacturer of the Bluetooth Controller. A 8 bit value is set. Note: This parameter
		is relevant for data frame configuration and for the packet type LL_VERSION_IND. \n
			:return: structure: for return value, see the help for VnumberStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:VNUMber?', self.__class__.VnumberStruct())

	def set_vnumber(self, value: VnumberStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:VNUMber \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_vnumber(value = VnumberStruct()) \n
		Sets the company identifier of the manufacturer of the Bluetooth Controller. A 8 bit value is set. Note: This parameter
		is relevant for data frame configuration and for the packet type LL_VERSION_IND. \n
			:param value: see the help for VnumberStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:VNUMber', value)

	def get_woffset(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:WOFFset \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_woffset() \n
		Sets the start point of the window transmit for data event and advertising frame configuration with the packet type
		CONNECT_IND. Command sets the values in ms. Query returns values in s. \n
			:return: wo_ffset: float Range: 0 s to depending on connection event interval , Unit: ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:WOFFset?')
		return Conversions.str_to_float(response)

	def set_woffset(self, wo_ffset: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:WOFFset \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_woffset(wo_ffset = 1.0) \n
		Sets the start point of the window transmit for data event and advertising frame configuration with the packet type
		CONNECT_IND. Command sets the values in ms. Query returns values in s. \n
			:param wo_ffset: float Range: 0 s to depending on connection event interval , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(wo_ffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:WOFFset {param}')

	def get_wsize(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:WSIZe \n
		Snippet: value: float = driver.source.bb.btooth.econfiguration.pconfiguration.get_wsize() \n
		Sets the size of the transmit window, regarding to the start point for data event and advertising frame configuration
		with the packet type CONNECT_IND. \n
			:return: wsize: float Range: 1.25E-3 to depends on connection event interval
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:WSIZe?')
		return Conversions.str_to_float(response)

	def set_wsize(self, wsize: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:WSIZe \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.set_wsize(wsize = 1.0) \n
		Sets the size of the transmit window, regarding to the start point for data event and advertising frame configuration
		with the packet type CONNECT_IND. \n
			:param wsize: float Range: 1.25E-3 to depends on connection event interval
		"""
		param = Conversions.decimal_value_to_str(wsize)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:WSIZe {param}')

	def clone(self) -> 'Pconfiguration':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pconfiguration(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
