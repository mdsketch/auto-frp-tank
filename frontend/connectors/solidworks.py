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
DESIGN_TABLE_PREFERENCE = win32com.client.VARIANT(pythoncom.VT_I4, 214)
VARIANT_I4_1 = win32com.client.VARIANT(pythoncom.VT_I4, 1)
OPENDOC_ARG5 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 2)
OPENDOC_ARG6 = win32com.client.VARIANT(
    pythoncom.VT_BYREF | pythoncom.VT_I4, 128)


def connect():
    return win32com.client.Dispatch("SldWorks.Application.{}".format(SWAV))


def getStudy(t, p1, p2):
    """
    modify the study parameters
        Parameters:
            t (float) : thickness of the shell
            p1 (float) : internal pressure
            p2 (float) : external pressure            
    """
    swApp = connect()
    CWObject = swApp.GetAddInObject("SldWorks.Simulation")
    COSMOSWORKS = CWObject.COSMOSWORKS
    ActDoc = COSMOSWORKS.ActiveDoc
    # Get the study manager
    StudyMngr = ActDoc.StudyManager
    # https://help.solidworks.com/2022/english/api/swsimulationapi/solidworks.interop.cosworks~solidworks.interop.cosworks.icwstudy_members.html
    Study = StudyMngr.GetStudy(0)

    # Modify the shell thickness
    # https://help.solidworks.com/2022/english/api/swsimulationapi/SolidWorks.Interop.cosworks~SolidWorks.Interop.cosworks.ICWShellManager_members.html
    ShellMgr = Study.ShellManager
    if (ShellMgr.ShellCount > 0):
        Shell = ShellMgr.GetShellAt(0, VARIANT_16387)
    # https://help.solidworks.com/2022/english/api/swsimulationapi/SolidWorks.Interop.cosworks~SolidWorks.Interop.cosworks.ICWShell_members.html
    Shell.ShellBeginEdit()
    Shell.ShellThickness = t
    error = Shell.ShellEndEdit

    pressure = [p1, p2]
    # Modify the pressure
    # https://help.solidworks.com/2022/english/api/swsimulationapi/SolidWorks.Interop.cosworks~SolidWorks.Interop.cosworks.ICWLoadsAndRestraintsManager_members.html
    landRMgr = Study.LoadsAndRestraintsManager
    # https://help.solidworks.com/2022/english/api/swsimulationapi/SolidWorks.Interop.cosworks~SolidWorks.Interop.cosworks.ICWLoadsAndRestraints_members.html
    for x in range(0, landRMgr.Count):
        y = landRMgr.GetLoadsAndRestraints(x, VARIANT_16387)
        # https://help.solidworks.com/2022/english/api/swsimulationapi/SOLIDWORKS.Interop.cosworks~SOLIDWORKS.Interop.cosworks.swsLoadsAndRestraintsType_e.html
        if y.Type == 1:
            # https://help.solidworks.com/2022/english/api/swsimulationapi/SolidWorks.Interop.cosworks~SolidWorks.Interop.cosworks.ICWPressure_members.html
            y.PressureBeginEdit()
            y.Value = pressure.pop(0)
            y.PressureEndEdit

def newDoc():
    """
    Create a new document
    """
    swApp = connect()
    path = 'C:\\autofrp\\doc1.prtdot'
    swApp.NewDocument(
        'C:\\ProgramData\\SolidWorks\\SOLIDWORKS 2022\\templates\\Part.prtdot', 0, 0, 0)
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
    swApp.OpenDoc6(arg1, VARIANT_I4_1, VARIANT_I4_1,
                   "", OPENDOC_ARG5, OPENDOC_ARG6)


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
    part.Extension.SelectByID2(
        "Front Plane", "PLANE", 0, 0, 0, False, 0, ARG_NULL, 0)
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
