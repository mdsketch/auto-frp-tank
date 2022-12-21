import sys
import time
import asyncio

import pythoncom

import win32com.client

# Solidworks Version (write the year) :
SWV = 2022
# API Version
SWAV = SWV-1992
# Elapsed time
elapsed = 0


async def main():
    swApp = win32com.client.Dispatch("SldWorks.Application.{}".format(SWAV))
    print(f" Solidworks API Version : {SWAV}",
          "\n", f"Solidworks Version : {SWV}")
    Part = swApp.ActiveDoc
    ARG_NULL = win32com.client.VARIANT(pythoncom.VT_DISPATCH, None)
    VT_BYREF = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, -1)
    
    CWAddinCallBackObj = swApp.GetAddInObject("CosmosWorks.CosmosWorks")
    COSMOSWORKSObj = CWAddinCallBackObj.COSMOSWORKS
  
    AssemblyTitle = Part.GetTitle
    tmpObj, errors, longwarnings = swApp.OpenDoc6(r"C:\Users\draws\Documents\auto-frp-tank\Part5.SLDPRT", 1, 32, "", VT_BYREF, VT_BYREF)
    Part = swApp.ActivateDoc3(AssemblyTitle, True, 0, VT_BYREF)
    swInsertedComponent = Part.AddComponent5(r"C:\Users\draws\Documents\auto-frp-tank\Part5.SLDPRT", 0, "", False, "", 1.39618374681716E-02, 1.80563761737247E-02, 2.65336923710037E-02)
    swApp.CloseDoc(r"C:\Users\draws\Documents\auto-frp-tank\Part5.SLDPRT")

try:
    if __name__ == "__main__":
        asyncio.run(main())
except KeyboardInterrupt:
    sys.exit()
