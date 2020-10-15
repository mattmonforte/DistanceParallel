#DistanceParallelPlanesMultipleSelect
#layers and objects get unlocked to allow selection
#r0,65
# Matt Monforte
# ClickWhirDing.com

import Rhino as rc
import rhinoscriptsyntax as rs
from scriptcontext import doc
import scriptcontext as sc
# import math

# clean up how unlock sticky works
# work on returns False, None, True
# Next make able to measure meshes
# maybe dont unlock hidden layers
# tell user when block selected so command wont work
# if cant measure blocks error check when block selected
# let user decide if can select locked objects
# add select again by reseting
# display command version for user somehow
# add allow regular distance_cmd measurements
# add allow selection of point and plane
# add allow select point and point
# hightlight bad selection with red hightlght
# Done-add message out click to copy to clipboard
# see if can improve hightlighting of block selections
# only try to relock layers/objcects if unlocked in the first place

__commandname__ = "DistanceParallel"
def RunCommand( is_interactive ):
    # print "DistanceParallel r0,65"
    # util.openUrl("https://github.com/mattmonforte")

    # DOC_TOLERANCE = rs.UnitAbsoluteTolerance()
    ZERO_TOLERANCE = 1.0e-5
    myDebug = True
    unlockLayersDefault = False
    global isUnlocked
    isUnlocked = False
    global layersToRelock
    layersToRelock = []
    global objectsToRelock
    objectsToRelock = []
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
        layersToRelock = unlock_layers()
        objectsToRelock = unlock_objects()
        isUnlocked = True

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
                clean_up_success()
                break
            # loop until second surface selected or cancel
            continue
        # Locking and Unlocking Objects and Layers
        elif getResult == rc.Input.GetResult.Option:
            if unlockLayers.CurrentValue == 1:
                isUnlocked = True
                sc.sticky["distance_parallel_unlock"] = True
                layersToRelock = unlock_layers()
                objectsToRelock = unlock_objects()
            else:
                isUnlocked = False
                sc.sticky["distance_parallel_unlock"] = False
                lock_objects(objectsToRelock)
                lock_layers(layersToRelock)
    	    # go.EnablePreSelect(False, True)
            continue
        elif getResult == Rhino.Input.GetResult.Nothing:
            # Why is this needed?
            msgOut("Got nothing.")
            clean_up_fail()
            return rc.Commands.Result.Failure
			# break
        # end While


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
    if isUnlocked:
        lock_objects(objectsToRelock)
        lock_layers(layersToRelock)
    return

def clean_up_success():
    if isUnlocked:
        lock_objects(objectsToRelock)
        lock_layers(layersToRelock)
    return

def clean_up_cancel():
    if isUnlocked:
        lock_objects(objectsToRelock)
        lock_layers(layersToRelock)
    return

def unlock_layers():
    # Unlock any locked layers so objects on layers can be selected.
    # Return list of layers unlocked with peristent locking setting of sub layers
    # stored as list of (layerobject, GetPersistentLocking)
    locked_layers = [layer for layer in doc.Layers if layer.IsLocked == True]
    previously_locked = []
    for layer in locked_layers:
        previously_locked.append(tuple((layer, layer.GetPersistentLocking())))
        layer.IsLocked = False
    return previously_locked

def lock_layers(_layers):
    for layer in _layers:
        layer_obj = layer[0]
        layer_persistent_locking_bool = layer[1]
        layer_obj.IsLocked = True
        layer_obj.SetPersistentLocking(layer_persistent_locking_bool)
    return

def unlock_objects():
    # maybe get by type (surface)
    allIds = rs.LockedObjects()
    lockedIds = []
    for id in allIds:
        if rs.IsObjectLocked(id):
            if not rs.IsObjectHidden(id):
                lockedIds.append(id)
                rs.UnlockObject(id)
    return lockedIds

def lock_objects(_objects):
    for obj_to_lock in _objects:
        rs.LockObject(obj_to_lock)
    return

if( __name__ == "__main__" ):
    RunCommand(True)
