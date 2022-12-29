import sys
import asyncio
import pythoncom
import win32com.client
import pathlib

# Solidworks Version (write the year) :
SWV = 2022
# API Version
SWAV = SWV-1992
VARIANT_16387 = win32com.client.VARIANT(
    pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
ARG_NULL = win32com.client.VARIANT(pythoncom.VT_DISPATCH, None)


def connect():
    return win32com.client.Dispatch("SldWorks.Application.{}".format(SWAV))


def newDoc():
    swApp = connect()
    path = 'C:\\Users\\draws\\Documents\\auto-frp-tank\\test.prtdot'
    swApp.NewDocument(
        'C:\\ProgramData\\SolidWorks\\SOLIDWORKS 2022\\templates\\Part.prtdot', 0, 0, 0)
    # 2 => rebuild activated doc
    swDoc = swApp.ActivateDoc3(path, False, 2, VARIANT_16387)


def closeDoc():
    swApp = connect()
    swDoc = swApp.ActiveDoc
    swApp.CloseDoc(swDoc.GetTitle)


def createCylinder(radius, height):
    swApp = connect()
    part = swApp.ActiveDoc
    part.SketchManager.InsertSketch(True)
    part.Extension.SelectByID2(
        "Front Plane", "PLANE", 0, 0, 0, False, 0, ARG_NULL, 0)
    part.ClearSelection2(True)
    part.SketchManager.CreateCircleByRadius(0, 0, 0, radius)
    part.ClearSelection2(True)
    part.SketchManager.CreateCircleByRadius(0, 0, 0, radius*1.2)
    # first dimension is height, 2nd dimension is thickness
    part.FeatureManager.FeatureExtrusion2(True, False, False, 0, 0, height, radius*0.2, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False)
    part.SelectionManager.EnableContourSelection = False