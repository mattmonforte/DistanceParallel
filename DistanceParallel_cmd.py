#DistanceParallelPlanesMultipleSelect
#layers and objects get unlocked to allow selection
#r0,70
# Matt Monforte
# ClickWhirDing.com

import Rhino as rc
import rhinoscriptsyntax as rs
from scriptcontext import doc
import scriptcontext as sc
from DPutilities.UnLocker import UnLocker
# import math

# clean up how unlock sticky works
# work on returns False, None, True
# Next make able to measure meshes
# maybe dont unlock hidden layers
# tell user when block selected so command wont work
# if cant measure blocks error check when block selected
# add select again by reseting
# display command version for user somehow
# hightlight bad selection with red hightlght
# Done-add message out click to copy to clipboard
# see if can improve hightlighting of block selections
# only try to relock layers/objcects if unlocked in the first place

ul = UnLocker()
__commandname__ = "DistanceParallel"
# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"

def RunCommand( is_interactive ):

    print __commandname__

    # DOC_TOLERANCE = rs.UnitAbsoluteTolerance()
    ZERO_TOLERANCE = 1.0e-5
    myDebug = True
    unlockLayersDefault = False
    global plane
    plane = []
    selectedObjects = []
    selectedCounter = 0

    if sc.sticky.has_key("distance_parallel_unlock"):
        unlockLayersDefault = sc.sticky["distance_parallel_unlock"]
    # if sc.sticky.has_key("distance_parallel_modalmsg"):
        # unlockLayersDefault = sc.sticky["distance_parallel_modalmsg"]

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

    ## Filter object type
    geometryType = rc.DocObjects.ObjectType.Surface
    go.GeometryFilter = geometryType

    unlockLayers = rc.Input.Custom.OptionToggle(unlockLayersDefault, "Off", "On")
    go.AddOptionToggle("UnlockLayersAndObjects", unlockLayers)

    if unlockLayers.CurrentValue == 1:
        ul.unlockLayersAndObjects()

    while True:
        getResult = go.GetMultiple(selectedCounter+1,selectedCounter+1)
        # go.EnableClearObjectsOnEntry(False)
        # go.DeselectAllBeforePostSelect = False
        if getResult == rc.Input.GetResult.Cancel:
            clean_up_cancel()
            return rc.Commands.Result.Cancel
        # if go.CommandResult() != rc.Commands.Result.Success:
        #     # why is this triggering?
        #     clean_up_success()
        #     return go.CommandResult()
        if getResult == rc.Input.GetResult.Object:
            selectedObjects = go.Objects()
            selectedCounter = len(selectedObjects)
            # get objects from selections
            objref = go.Object(selectedCounter-1)
            # get selected surface object
            obj = objref.Object()
            if not obj:
                # Why is this needed?
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
                msgOut("Surfaces is not planar.")
                # maybe continue or allow select of first surface again
                clean_up_fail()
                return rc.Commands.Result.Failure
            plane.append(getPlane)
            if selectedCounter == 2:
                break
            # loop until second surface selected or cancel
            continue
        # Locking and Unlocking Objects and Layers
        elif getResult == rc.Input.GetResult.Option:
            if unlockLayers.CurrentValue == 1:
                sc.sticky["distance_parallel_unlock"] = True
                ul.unlockLayersAndObjects()
            else:
                sc.sticky["distance_parallel_unlock"] = False
                ul.relockLayersAndObjects()
    	    # go.EnablePreSelect(False, True)
            continue
        elif getResult == Rhino.Input.GetResult.Nothing:
            # Why is this needed?
            msgOut("Got nothing.")
            clean_up_fail()
            return rc.Commands.Result.Failure
			# break
        # end While

    clean_up_success()
    # Are planes parallel
    # if ArePlanesParallel(plane[0], plane[1], ZERO_TOLERANCE) == True:
    if ArePlanesParallel(plane[0], plane[1], ZERO_TOLERANCE) == False:
        msgOut("Surfaces are not parallel to each other.")
        clean_up_fail()
        return rc.Commands.Result.Failure
    # measure distance between planes
    # acually distance between plane[0] and point on plan[1]
    ParallelDistance = abs(rs.DistanceToPlane(plane[0], plane[1][0]))
    # output results
    unitsName = doc.GetUnitSystemName(True, True, True, False)
    ## fromating output decimal places not working
    # decimalPlaces = doc.DistanceDisplayPrecision
    # textOut = "Parallel Distance = {:." + str(decimalPlaces) +"f} " + unitsName
    rs.ClipboardText(ParallelDistance)
    textOut = "Parallel Distance = {:.4f} " + unitsName
    # msgOut(textOut.format(ParallelDistance))
    rs.MessageBox("the value is saved in your clipboard", 64, textOut.format(ParallelDistance))
    print(textOut.format(ParallelDistance))
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

# print "DistanceParallel r0,70"
# util.openUrl("https://github.com/mattmonforte")

#This allows you to test the script from the editor, debug etc.
#RunCommand(True)
if( __name__ == "__main__" ):
    RunCommand(True)
