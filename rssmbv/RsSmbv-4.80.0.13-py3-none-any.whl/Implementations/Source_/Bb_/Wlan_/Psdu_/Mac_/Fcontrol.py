from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fcontrol:
	"""Fcontrol commands group definition. 12 total commands, 0 Sub-groups, 12 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fcontrol", core, parent)

	def get_fds(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:FDS \n
		Snippet: value: List[str] = driver.source.bb.wlan.psdu.mac.fcontrol.get_fds() \n
		No command help available \n
			:return: fds: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:FDS?')
		return Conversions.str_to_str_list(response)

	def set_fds(self, fds: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:FDS \n
		Snippet: driver.source.bb.wlan.psdu.mac.fcontrol.set_fds(fds = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param fds: No help available
		"""
		param = Conversions.list_to_csv_str(fds)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:FDS {param}')

	def get_mdata(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:MDATa \n
		Snippet: value: List[str] = driver.source.bb.wlan.psdu.mac.fcontrol.get_mdata() \n
		No command help available \n
			:return: mdata: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:MDATa?')
		return Conversions.str_to_str_list(response)

	def set_mdata(self, mdata: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:MDATa \n
		Snippet: driver.source.bb.wlan.psdu.mac.fcontrol.set_mdata(mdata = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param mdata: No help available
		"""
		param = Conversions.list_to_csv_str(mdata)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:MDATa {param}')

	def get_mfragments(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:MFRagments \n
		Snippet: value: List[str] = driver.source.bb.wlan.psdu.mac.fcontrol.get_mfragments() \n
		No command help available \n
			:return: mfragments: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:MFRagments?')
		return Conversions.str_to_str_list(response)

	def set_mfragments(self, mfragments: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:MFRagments \n
		Snippet: driver.source.bb.wlan.psdu.mac.fcontrol.set_mfragments(mfragments = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param mfragments: No help available
		"""
		param = Conversions.list_to_csv_str(mfragments)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:MFRagments {param}')

	def get_order(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:ORDer \n
		Snippet: value: List[str] = driver.source.bb.wlan.psdu.mac.fcontrol.get_order() \n
		No command help available \n
			:return: order: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:ORDer?')
		return Conversions.str_to_str_list(response)

	def set_order(self, order: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:ORDer \n
		Snippet: driver.source.bb.wlan.psdu.mac.fcontrol.set_order(order = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param order: No help available
		"""
		param = Conversions.list_to_csv_str(order)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:ORDer {param}')

	def get_pmanagement(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:PMANagement \n
		Snippet: value: List[str] = driver.source.bb.wlan.psdu.mac.fcontrol.get_pmanagement() \n
		No command help available \n
			:return: pmanagement: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:PMANagement?')
		return Conversions.str_to_str_list(response)

	def set_pmanagement(self, pmanagement: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:PMANagement \n
		Snippet: driver.source.bb.wlan.psdu.mac.fcontrol.set_pmanagement(pmanagement = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param pmanagement: No help available
		"""
		param = Conversions.list_to_csv_str(pmanagement)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:PMANagement {param}')

	def get_pversion(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:PVERsion \n
		Snippet: value: List[str] = driver.source.bb.wlan.psdu.mac.fcontrol.get_pversion() \n
		No command help available \n
			:return: pversion: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:PVERsion?')
		return Conversions.str_to_str_list(response)

	def set_pversion(self, pversion: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:PVERsion \n
		Snippet: driver.source.bb.wlan.psdu.mac.fcontrol.set_pversion(pversion = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param pversion: No help available
		"""
		param = Conversions.list_to_csv_str(pversion)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:PVERsion {param}')

	def get_retry(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:RETRy \n
		Snippet: value: List[str] = driver.source.bb.wlan.psdu.mac.fcontrol.get_retry() \n
		No command help available \n
			:return: retry: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:RETRy?')
		return Conversions.str_to_str_list(response)

	def set_retry(self, retry: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:RETRy \n
		Snippet: driver.source.bb.wlan.psdu.mac.fcontrol.set_retry(retry = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param retry: No help available
		"""
		param = Conversions.list_to_csv_str(retry)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:RETRy {param}')

	def get_sub_type(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:SUBType \n
		Snippet: value: List[str] = driver.source.bb.wlan.psdu.mac.fcontrol.get_sub_type() \n
		No command help available \n
			:return: subtype: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:SUBType?')
		return Conversions.str_to_str_list(response)

	def set_sub_type(self, subtype: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:SUBType \n
		Snippet: driver.source.bb.wlan.psdu.mac.fcontrol.set_sub_type(subtype = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param subtype: No help available
		"""
		param = Conversions.list_to_csv_str(subtype)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:SUBType {param}')

	def get_tds(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:TDS \n
		Snippet: value: List[str] = driver.source.bb.wlan.psdu.mac.fcontrol.get_tds() \n
		No command help available \n
			:return: tds: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:TDS?')
		return Conversions.str_to_str_list(response)

	def set_tds(self, tds: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:TDS \n
		Snippet: driver.source.bb.wlan.psdu.mac.fcontrol.set_tds(tds = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param tds: No help available
		"""
		param = Conversions.list_to_csv_str(tds)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:TDS {param}')

	def get_type_py(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:TYPE \n
		Snippet: value: List[str] = driver.source.bb.wlan.psdu.mac.fcontrol.get_type_py() \n
		No command help available \n
			:return: type_py: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:TYPE?')
		return Conversions.str_to_str_list(response)

	def set_type_py(self, type_py: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:TYPE \n
		Snippet: driver.source.bb.wlan.psdu.mac.fcontrol.set_type_py(type_py = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param type_py: No help available
		"""
		param = Conversions.list_to_csv_str(type_py)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:TYPE {param}')

	def get_wep(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:WEP \n
		Snippet: value: List[str] = driver.source.bb.wlan.psdu.mac.fcontrol.get_wep() \n
		No command help available \n
			:return: wep: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:WEP?')
		return Conversions.str_to_str_list(response)

	def set_wep(self, wep: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol:WEP \n
		Snippet: driver.source.bb.wlan.psdu.mac.fcontrol.set_wep(wep = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param wep: No help available
		"""
		param = Conversions.list_to_csv_str(wep)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol:WEP {param}')

	def get_value(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol \n
		Snippet: value: List[str] = driver.source.bb.wlan.psdu.mac.fcontrol.get_value() \n
		No command help available \n
			:return: fcontrol: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol?')
		return Conversions.str_to_str_list(response)

	def set_value(self, fcontrol: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:FCONtrol \n
		Snippet: driver.source.bb.wlan.psdu.mac.fcontrol.set_value(fcontrol = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param fcontrol: No help available
		"""
		param = Conversions.list_to_csv_str(fcontrol)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:FCONtrol {param}')
