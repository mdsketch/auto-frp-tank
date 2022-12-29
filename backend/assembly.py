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

# C:\Users\draws\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\win32com\client


async def main():
    swApp = win32com.client.Dispatch("SldWorks.Application.{}".format(SWAV))
    print(f" Solidworks API Version : {SWAV}",
          "\n", f"Solidworks Version : {SWV}")
    Part = swApp.ActiveDoc
    ARG_NULL = win32com.client.VARIANT(pythoncom.VT_DISPATCH, None)
    VT_BYREF = win32com.client.VARIANT(
        pythoncom.VT_BYREF | pythoncom.VT_I4, -1)

    CWAddinCallBackObj = swApp.GetAddInObject("CosmosWorks.CosmosWorks")
    COSMOSWORKSObj = CWAddinCallBackObj.COSMOSWORKS

    AssemblyTitle = Part.GetTitle

    swInsertedComponent = Part.AddComponent5(r"C:\Users\draws\Documents\auto-frp-tank\Part5.SLDPRT",
                                             0, "", False, "", 1.39618374681716E-02, 1.80563761737247E-02, 2.65336923710037E-02)

    swInsertedComponent1 = Part.AddComponent5(r"C:\Users\draws\Documents\auto-frp-tank\Part6.SLDPRT",
                                             0, "", False, "", 1.10310856715342E-02, 3.29195746490591E-02, 5.30062776835991E-02)

    # Dim TransformData() As Double
# ReDim TransformData(0 To 15) As Double
# TransformData(0) = 1
# TransformData(1) = 0
# TransformData(2) = 0
# TransformData(3) = 0
# TransformData(4) = 1
# TransformData(5) = 0
# TransformData(6) = 0
# TransformData(7) = 0
# TransformData(8) = 1
# TransformData(9) = 0
# TransformData(10) = 0
# TransformData(11) = 0
# TransformData(12) = 1
# TransformData(13) = 0
# TransformData(14) = 0
# TransformData(15) = 0
# Dim TransformDataVariant As Variant
# TransformDataVariant = TransformData
# Dim swMathUtil As Object
# Set swMathUtil = swApp.GetMathUtility()
# Dim swTransform As Object
# Set swTransform = swMathUtil.CreateTransform((TransformDataVariant))
# boolstatus = swInsertedComponent.SetTransformAndSolve2(swTransform)
    
    TransformData = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    TransformDataVariant = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, TransformData)
    swMathUtil = swApp.IGetMathUtility()
    swTransform = swMathUtil.CreateTransform(TransformDataVariant)
    boolstatus = swInsertedComponent.SetTransformAndSolve2(swTransform)

    boolstatus = Part.Extension.SelectByRay(2.57820884413604E-02, 4.23974314305156E-02, 5.79791394834501E-02, -
                                            0.400036026779312, -0.515038074910024, -0.758094294050284, 2.38338722016596E-04, 1, False, 0, 0)
    boolstatus = Part.Extension.SelectByRay(2.57820884413604E-02, 4.23974314305156E-02, 5.79791394834501E-02, -
                                            0.400036026779312, -0.515038074910024, -0.758094294050284, 2.38338722016596E-04, 1, False, 0, 0)
    boolstatus = Part.Extension.SelectByRay(1.69052335818947E-02, 4.51818155505634E-03, 9.61527234721871E-07, -
                                            0.400036026779312, -0.515038074910024, -0.758094294050284, 2.38338722016596E-04, 1, False, 0, 0)
    boolstatus = Part.Extension.SelectByRay(1.69052335818947E-02, 4.51818155505634E-03, 9.61527234721871E-07, -
                                            0.400036026779312, -0.515038074910024, -0.758094294050284, 2.38338722016596E-04, 1, False, 0, 0)
    #Part.ClearSelection2 = True
    
    #Part.ClearSelection2 = True
    StudyManagerObj = ARG_NULL
    ActiveDocObj = ARG_NULL
    CWAddinCallBackObj = ARG_NULL
    COSMOSWORKSObj = ARG_NULL

try:
    if __name__ == "__main__":
        asyncio.run(main())
except KeyboardInterrupt:
    sys.exit()
