'''
DistanceParallel
created 9/4/2020

A python command for Rhinoceros 3d CAD modeling software that measures
the distance between two parallel planar surfaces.

Copyright (c)2020 Matt Monforte
mattmonforte@gmail.com
ClickWhirDing.com
MonSalon.org

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see https://www.gnu.org/licenses.
'''

import Rhino as rc
import rhinoscriptsyntax as rs
from scriptcontext import doc
import scriptcontext as sc
from DPutilities.UnLocker import UnLocker

ul = UnLocker()
__commandname__ = "DistanceParallel"

def RunCommand( is_interactive ):
    print __commandname__

    # ZERO_TOLERANCE = 1.0e-2
    ZERO_TOLERANCE = rs.UnitAbsoluteTolerance()
    myDebug = True
    unlockLayersDefault = False
    global plane
    plane = []
    selectedObjects = []
    selectedCounter = 0

    go = rc.Input.Custom.GetObject()
    go.SetCommandPrompt("Select Two Parallel Planar Surfaces")
    go.AlreadySelectedObjectSelect = False
    go.DeselectAllBeforePostSelect = False
    go.EnableClearObjectsOnEntry(False)
    # go.EnableUnselectObjectsOnExit(False)
    go.OneByOnePostSelect = True
    go.SubObjectSelect = True
    go.EnablePreSelect(False, True)
    # go.EnableClearObjectsOnEntry(False)

    # Filter object type
    geometryType = rc.DocObjects.ObjectType.Surface
    go.GeometryFilter = geometryType


    # Set up command option persistance memory
    if sc.sticky.has_key("distance_parallel_unlock"):
        unlockLayersDefault = sc.sticky["distance_parallel_unlock"]
    else:
        sc.sticky["distance_parallel_unlock"] = False
        unlockLayersDefault = sc.sticky["distance_parallel_unlock"]

    if sc.sticky.has_key("distance_parallel_msg_box"):
        messageBoxDefault = sc.sticky["distance_parallel_msg_box"]
    else:
        sc.sticky["distance_parallel_msg_box"] = False
        messageBoxDefault = sc.sticky["distance_parallel_msg_box"]

    # set up command options
    unlockLayers = rc.Input.Custom.OptionToggle(unlockLayersDefault, "Off", "On")
    go.AddOptionToggle("UnlockLayersAndObjects", unlockLayers)

    messageBox = rc.Input.Custom.OptionToggle(messageBoxDefault, "Off", "On")
    go.AddOptionToggle("ResultsInMessageBox", messageBox)

    unlockLayersPrevState = unlockLayers.CurrentValue
    messageBoxPrevState = messageBox.CurrentValue

    if unlockLayers.CurrentValue == 1:
        ul.unlockLayersAndObjects()


    while True:

        getResult = go.GetMultiple(selectedCounter+1,selectedCounter+1)
        # go.EnableClearObjectsOnEntry(False)
        # go.DeselectAllBeforePostSelect = False
        if getResult == rc.Input.GetResult.Cancel:
            clean_up_cancel()
            return rc.Commands.Result.Cancel
        #     clean_up_success()
        #     return go.CommandResult()
        if getResult == rc.Input.GetResult.Object:
            # Get the view that the point was picked in.
            view = go.View()
            selectedObjects = go.Objects()
            selectedCounter = len(selectedObjects)
            # get objects from selections
            objref = go.Object(selectedCounter-1)
            # get selected surface object
            obj = objref.Object()
            if not obj:
                # Why do?
                if myDebug :
                    msgOut("Object not selected.")
                clean_up_fail()
                return rc.Commands.Result.Failure
            try:
                surface = objref.Surface()
            except:
                msgOut("Surfaces within blocks are not always selectable. Polysurfaces can be selected, Extrusion cannot. Explode block for more selectability.")
                # try to continue and reselect
                clean_up_fail()
                return rc.Commands.Result.Failure
            if not surface:
                # why is this needed?
                if myDebug :
                    msgOut("No surface selected.")
                clean_up_fail()
                return rc.Commands.Result.Failure

            test, getPlane = surface.TryGetPlane(ZERO_TOLERANCE)
            if not test:
                msgOut("Surface is not planar.")
                # maybe continue or allow select of first surface again
                clean_up_fail()
                return rc.Commands.Result.Failure
            plane.append(getPlane)
            if selectedCounter == 2:
                # view.Redraw()
                break
            # loop until second surface selected or cancel
            continue
        # Command Options
        elif getResult == rc.Input.GetResult.Option:
            if unlockLayers.CurrentValue != unlockLayersPrevState:
                if unlockLayers.CurrentValue == 1:
                    sc.sticky["distance_parallel_unlock"] = True
                    unlockLayersPrevState = True
                    ul.unlockLayersAndObjects()
                else:
                    sc.sticky["distance_parallel_unlock"] = False
                    unlockLayersPrevState = False
                    ul.relockLayersAndObjects()
            elif messageBox.CurrentValue != messageBoxPrevState:
                if messageBox.CurrentValue == 1:
                    sc.sticky["distance_parallel_msg_box"] = True
                    messageBoxPrevState = True
                else:
                    sc.sticky["distance_parallel_msg_box"] = False
                    messageBoxPrevState = False
    	    go.EnablePreSelect(False, True)
            continue
        elif getResult == rc.Input.GetResult.Nothing:
            # needed?
            msgOut("Got nothing.")
            clean_up_fail()
            return rc.Commands.Result.Failure
            # break
        # end While

    clean_up_success()
    # Are planes parallel
    if ArePlanesParallel(plane[0], plane[1], ZERO_TOLERANCE) == False:
        msgOut("Surfaces are not parallel to each other.")
        clean_up_fail()
        return rc.Commands.Result.Failure
    # measure distance between planes
    # acually distance between plane[0] and point on plan[1]
    ParallelDistance = abs(rs.DistanceToPlane(plane[0], plane[1][0]))
    # output results
    unitsName = doc.GetUnitSystemName(True, True, True, False)
    ## fromating output decimal places not working for me
    # decimalPlaces = doc.DistanceDisplayPrecision
    # textOut = "Parallel Distance = {:." + str(decimalPlaces) +"f} " + unitsName
    rs.ClipboardText(ParallelDistance)
    textOut = "Parallel Distance = {:.4f} " + unitsName
    # msgOut(textOut.format(ParallelDistance))
    print(textOut.format(ParallelDistance))
    if sc.sticky["distance_parallel_msg_box"]:
        # view.Redraw()
        rs.MessageBox("the value is saved to your clipboard", 64, textOut.format(ParallelDistance))
    else:
        pass
        #delay enough to see last selected highlighting before commend ends
        #Doesn't always work. look for better way to do this
        # rs.Sleep(400)
    return rc.Commands.Result.Success

def msgOut(_msg):
    print(_msg)
    rs.MessageBox(_msg)
    return

def ArePlanesParallel(_plane1, _plane2, tol):
    cpvec = rs.VectorCrossProduct(_plane1.Normal, _plane2.Normal)
    if abs(cpvec.X) < tol and abs(cpvec.Y) < tol and abs(cpvec.Z) < tol:
        return True
    return False

def clean_up_fail():
    if ul.unlocked:
        ul.relockLayersAndObjects()
    return

def clean_up_success():
    if ul.unlocked:
        ul.relockLayersAndObjects()
    return

def clean_up_cancel():
    if ul.unlocked:
        ul.relockLayersAndObjects()
    return

if( __name__ == "__main__" ):
    RunCommand(True)
