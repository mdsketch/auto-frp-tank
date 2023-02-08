import sys
import asyncio
import pythoncom
import win32com.client
import pathlib

# Solidworks Version (write the year) :
SWV = 2022
# API Version
SWAV = SWV-1992
VARIANT_16387 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
ARG_NULL = win32com.client.VARIANT(pythoncom.VT_DISPATCH, None)
DESIGN_TABLE_PREFERENCE = win32com.client.VARIANT(pythoncom.VT_I4, 214)
VARIANT_I4_1 = win32com.client.VARIANT(pythoncom.VT_I4, 1)
OPENDOC_ARG5 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 2)
OPENDOC_ARG6 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 128)


def connect():
    return win32com.client.Dispatch("SldWorks.Application.{}".format(SWAV))


def newDoc():
    """
    Create a new document
    """
    swApp = connect()
    path = 'C:\\autofrp\\doc1.prtdot'
    swApp.NewDocument('C:\\ProgramData\\SolidWorks\\SOLIDWORKS 2022\\templates\\Part.prtdot', 0, 0, 0)
    # 2 => rebuild activated doc
    swDoc = swApp.ActivateDoc3(path, False, 2, VARIANT_16387)

def saveImage():
    """
    Save active document as PNG image
    """
    swApp = connect()
    swDoc = swApp.ActiveDoc
    swDoc.SaveAs3('C:\\autofrp\\doc1.png', 0, 2)

def openDoc(path):
    """
    Open document located at path
        path (str) : full path of the part to open
    Returns:
        none
    """
    swApp = connect()
    arg1 = win32com.client.VARIANT(pythoncom.VT_BSTR, path)
    swApp.OpenDoc6(arg1, VARIANT_I4_1, VARIANT_I4_1, "", OPENDOC_ARG5, OPENDOC_ARG6)


def closeDoc():
    """
    Close active document
    """
    swApp = connect()
    swDoc = swApp.ActiveDoc
    swApp.CloseDoc(swDoc.GetTitle)


def createCylinder(radius, height):
    """
    Create a cylinder

    Args:
        radius (float) : radius of the cylinder
        height (float) : height of the cylinder
    """
    swApp = connect()
    part = swApp.ActiveDoc
    part.SketchManager.InsertSketch(True)
    part.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, ARG_NULL, 0)
    part.ClearSelection2(True)
    part.SketchManager.CreateCircleByRadius(0, 0, 0, radius)
    part.ClearSelection2(True)
    part.SketchManager.CreateCircleByRadius(0, 0, 0, radius*1.2)
    # first dimension is height, 2nd dimension is thickness
    part.FeatureManager.FeatureExtrusion2(True, False, False, 0, 0, height, radius*0.2, False,
                                          False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False)
    part.SelectionManager.EnableContourSelection = False


def setPreferences(type):
    """
    Set preferences to allow design table to automatically update part
        type (int) : 0 => prompt, 1 => model, 2 => excelfile

    Returns:
        Current preference
    """
    swApp = connect()
    previous = swApp.GetUserPreferenceIntegerValue(DESIGN_TABLE_PREFERENCE)
    swApp.SetUserPreferenceIntegerValue(DESIGN_TABLE_PREFERENCE, 2)
    return previous
