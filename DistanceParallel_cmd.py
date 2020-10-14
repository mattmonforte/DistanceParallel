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
# remember unlock settings
# Next make able to measure meshes
# tell user when block selected so command wont work
# Next make able to measure objects in blocks
# if cant measure blocks error check when block selected
# let user decide if can select locked objects
# add select again by reseting
# display command version for user somehow
# add allow regular distance_cmd measurements
# add allow selection of point and plane
# add allow selection of point and line closest point
# hightlight bad selection with red hightlght
# Done-add message out click to copy to clipboard
# see if can improve hightlighting of block selections

__commandname__ = "DistanceParallel"
def RunCommand( is_interactive ):
    # print "DistanceParallel r0,65"
    # util.openUrl("https://github.com/mattmonforte")

    # DOC_TOLERANCE = rs.UnitAbsoluteTolerance()
    ZERO_TOLERANCE = 1.0e-5
    myDebug = True
    unlockLayersDefault = False
    global UnlockLayersUsed
    UnlockLayersUsed = False
    global layersToRelock
    layersToRelock = []
    global objectsToRelock
    objectsToRelock = []
    global plane
    plane = []

    if sc.sticky.has_key("distance_parallel_unlock"):
        unlockLayersDefault = sc.sticky["distance_parallel_unlock"]

    s1 = rc.Input.Custom.GetObject()
    s1.SetCommandPrompt("Select Two Parallel Planar Surfaces")
    s1.AlreadySelectedObjectSelect = False
    s1.DeselectAllBeforePostSelect = False
    # s1.EnableClearObjectsOnEntry(False)
    # s1.EnableUnselectObjectsOnExit(False)
    s1.OneByOnePostSelect = True
    s1.SubObjectSelect = True
    s1.EnablePreSelect(False, True)
    # s1.EnableClearObjectsOnEntry(False)

    ## Filter object type
    geometryType = rc.DocObjects.ObjectType.Surface
    s1.GeometryFilter = geometryType

    unlockLayers = rc.Input.Custom.OptionToggle(unlockLayersDefault, "Off", "On")
    s1.AddOptionToggle("UnlockLayersAndObjects", unlockLayers)

    if unlockLayers.CurrentValue == 1:
        UnlockLayersUsed = True
        layersToRelock = unlock_layers()
        objectsToRelock = unlock_objects()

    while True:
    	getResult = s1.GetMultiple(1,2)
    	if getResult == rc.Input.GetResult.Cancel:
            clean_up_cancel()
            return rc.Commands.Result.Cancel
    	elif getResult == rc.Input.GetResult.Option:
            if unlockLayers.CurrentValue == 1:
                UnlockLayersUsed = True
                sc.sticky["distance_parallel_unlock"] = True
                layersToRelock = unlock_layers()
                objectsToRelock = unlock_objects()
            else:
                sc.sticky["distance_parallel_unlock"] = False
                lock_objects(objectsToRelock)
                lock_layers(layersToRelock)
    	    # s1.EnablePreSelect(False, True)
            continue
        elif getResult == rc.Input.GetResult.Object:
            # ids = [s1.Object(i).ObjectId for i in range(s1.ObjectCount)]
            for i in range(2):
                # get objects from selections
                objref = s1.Object(i)
                # get selected surface object
                obj = objref.Object()
                if not obj:
                    if myDebug :
                        msgOut("Object not selected")
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
                    if myDebug :
                        msgOut("No surface selected.")
                    clean_up_fail()
                    return rc.Commands.Result.Failure
                # Unselect surface
                test, getPlane = surface.TryGetPlane(ZERO_TOLERANCE)
                if not test:
                    msgOut("One of the selected surfaces is not planar.")
                    # maybe continue or allow select of first surface again
                    clean_up_fail()
                    return rc.Commands.Result.Failure
                plane.append(getPlane)
                # obj.Select(False)

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
            msgOut(textOut.format(ParallelDistance))

        clean_up_success()
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
    if UnlockLayersUsed:
        lock_objects(objectsToRelock)
        lock_layers(layersToRelock)
    return

def clean_up_success():
    if UnlockLayersUsed:
        lock_objects(objectsToRelock)
        lock_layers(layersToRelock)
    return

def clean_up_cancel():
    if UnlockLayersUsed:
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
