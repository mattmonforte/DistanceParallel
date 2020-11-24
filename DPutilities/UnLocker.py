# import Rhino
import rhinoscriptsyntax as rs
from scriptcontext import doc
# import scriptcontext as sc

class UnLocker:
    # Class Variables
    # The init method or constructor
    def __init__(self):
        # print('**Create UnLocker**')
        # Instance Variables
        # if class unlocked the layers status is true
        self.unlocked = False
        self.layersUnLocked = False # not used yet
        self.objectUnLocked = False # not used yet
        self.prevLockedLayers = []
        self.prevLockedObjects = []

	#Deleting (Calling destructor)
	# def __del__(self):
	# 	class_name = self.__class__.__name__
	# 	if self.unlocked:
	# 		print("clean up")
	# 		self.relockLayersAndObjects()
	# 	print(class_name, "destroyed")
	# 	return

    def isUnLocked(self):
        if self.unlocked:
            # print("status: True unlocked")
        else:
            # print("status: False locked")
        return self.unlocked

    def areObjectsUnLocked(self):
        if self.objectUnLocked:
            # print("status: True unlocked")
        else:
            # print("status: False locked")
        return self.objectUnLocked

    def areLayersUnLocked(self):
        if self.layersUnLocked:
            # print("status: True unlocked")
        else:
            # print("status: False locked")
        return self.layersUnLocked

    def __unlockObjects(self):
        # print("Objects unlocked")
        # maybe get by type (surface)
        self.prevLockedObjects = []
        allIds = rs.LockedObjects()
        for id in allIds:
            if rs.IsObjectLocked(id):
                if not rs.IsObjectHidden(id):
                    self.prevLockedObjects.append(id)
                    rs.UnlockObject(id)
        self.objectUnLocked = True
        return

    def __unlockLayers(self):
        # print("Layers unlocked")
        self.previouslyLockedLayers = []
        locked_layers = [layer for layer in doc.Layers if layer.IsLocked == True]
        for layer in locked_layers:
            self.previouslyLockedLayers.append(tuple((layer, layer.GetPersistentLocking())))
            layer.IsLocked = False
        self.layersUnLocked = True
        return

    def __relockObjects(self):
        # print("Objects relocked")
        for obj_to_lock in self.prevLockedObjects:
            rs.LockObject(obj_to_lock)
        self.objectUnLocked = False
        return

    def __relockLayers(self):
        # print("Layers relocked")
        for layer in self.previouslyLockedLayers:
            layer_obj = layer[0]
            layer_persistent_locking_bool = layer[1]
            layer_obj.IsLocked = True
            layer_obj.SetPersistentLocking(layer_persistent_locking_bool)
        self.layersUnLocked = False
        return

    def unlockLayersAndObjects(self):
        self.unlocked = True
        self.__unlockLayers()
        self.__unlockObjects()
        return

    def relockLayersAndObjects(self):
        self.unlocked = False
        self.__relockObjects()
        self.__relockLayers()
        return
