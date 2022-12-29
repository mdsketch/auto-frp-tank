import sys
import asyncio
import pythoncom
import win32com.client
import pathlib

# Solidworks Version (write the year) :
SWV = 2022
# API Version
SWAV = SWV-1992
variant16387 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)

def connect():
    return win32com.client.Dispatch("SldWorks.Application.{}".format(SWAV))

def newDoc():
    swApp = connect()
    path = 'C:\\Users\\draws\\Documents\\auto-frp-tank\\test.prtdot'
    swApp.NewDocument('C:\\ProgramData\\SolidWorks\\SOLIDWORKS 2022\\templates\\Part.prtdot', 0, 0, 0)
    # 2 => rebuild activated doc
    swDoc = swApp.ActivateDoc3(path, False, 2, variant16387)

def closeDoc():
    swApp = connect()
    swDoc = swApp.ActiveDoc
    swApp.CloseDoc(swDoc.GetTitle)

