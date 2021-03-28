# pip install win32wifi

from win32wifi.Win32NativeWifiApi import *

def WlanSetProfile(hClientHandle, pInterfaceGuid, xml_profile):
    """
    DWORD WlanSetProfile(
        HANDLE     hClientHandle,
        const GUID *pInterfaceGuid,
        DWORD      dwFlags,
        LPCWSTR    strProfileXml,
        LPCWSTR    strAllUserProfileSecurity,
        BOOL       bOverwrite,
        PVOID      pReserved,
        DWORD      *pdwReasonCode
        );
    """
    func_ref = wlanapi.WlanSetProfile
    func_ref.argtypes = [HANDLE,
                         POINTER(GUID),
                         DWORD,
                         LPCWSTR,
                         LPCWSTR,
                         BOOL,
                         c_void_p,
                         POINTER(DWORD)]
    func_ref.restype = DWORD

    dwFlags = DWORD(0)
    pdwReasonCode = DWORD()
    result = func_ref(hClientHandle,
                      byref(pInterfaceGuid),
                      dwFlags,
                      xml_profile,
                      None,
                      False,
                      None,
                      byref(pdwReasonCode))
    if result != 0:
        raise Exception("WlanSetProfile failed. error %d" % result, result)
    return result