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
    sw = win32com.client.Dispatch("SldWorks.Application.{}".format(SWAV))
    print(f" Solidworks API Version : {SWAV}",
          "\n", f"Solidworks Version : {SWV}")
    Model = sw.ActiveDoc
    ARG_NULL = win32com.client.VARIANT(pythoncom.VT_DISPATCH, None)
    ck = Model.Extension.SelectByID2(
        "Front", "PLANE", 0, 0, 0, False, 0, ARG_NULL, 0)
    Model.SketchManager.InsertSketch(True)
    Model.ClearSelection2(True)

# create 2 circles with a radius of 10 with the same center point
    Model.SketchManager.CreateCircleByRadius(0, 0, 0, 10)
    # put 2nd circle 10mm away from the first
    Model.SketchManager.CreateCircleByRadius(10, 0, 3, 10)
    
# extrude the the bottom circle 10mm in the Z direction
    # Model.ClearSelection2(True)
    # Model.Extension.SelectByID2("Circle1", "SKETCHSEGMENT", 0, 0, 0, False, 0, ARG_NULL, 0)
    # Model.Extension.SelectByID2("Circle2", "SKETCHSEGMENT", 0, 0, 0, True, 0, ARG_NULL, 0)
    Model.FeatureManager.FeatureExtrusion3(True, False, False, 0, 0, 10, 10, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, 0)

# create a cylinder with a radius of 10 and a height of 10 from 2 circles


    myFeature = Model.FeatureManager.FeatureExtrusion2(
        True,
        False,
        False,
        0,
        0,
        10,
        10,
        False,
        False,
        False,
        False,
        0,
        0,
        False,
        False,
        False,
        False,
        True,
        True,
        True,
        0,
        0,
        False,
    )

    Model.SelectionManager.EnableContourSelection = False
    Model.ClearSelection2(True)

try:
    if __name__ == "__main__":
        asyncio.run(main())
except KeyboardInterrupt:
    sys.exit()
