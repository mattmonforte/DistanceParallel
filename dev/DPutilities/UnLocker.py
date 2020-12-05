# UnLocker
# Unlock layers and Objects in Rhinoceros 3d CAD modeling software
# created 11/20/2020
#
# Copyright (c)2020 Matt Monforte
# mattmonforte@gmail.com
# ClickWhirDing.com
# MonSalon.org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see https://www.gnu.org/licenses.


import rhinoscriptsyntax as rs
from scriptcontext import doc

class UnLocker:

    def __init__(self):
        # if the UnLocker class unlocked the layers unlocked status shoudl be true
        self.unlocked = False
        self.layersUnLocked = False # not used yet
        self.objectUnLocked = False # not used yet
        self.prevLockedLayers = []
        self.prevLockedObjects = []

    def isUnLocked(self):
        if self.unlocked:
            print("status: True unlocked")
        else:
            print("status: False locked")
        return self.unlocked

    def areObjectsUnLocked(self):
        if self.objectUnLocked:
            print("status: True unlocked")
        else:
            print("status: False locked")
        return self.objectUnLocked

    def areLayersUnLocked(self):
        if self.layersUnLocked:
            print("status: True unlocked")
        else:
            print("status: False locked")
        return self.layersUnLocked

    def __unlockObjects(self):
        # print("Objects unlocked")
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
        self.previouslyLockedLayers = []
        locked_layers = [layer for layer in doc.Layers if layer.IsLocked == True]
        for layer in locked_layers:
            self.previouslyLockedLayers.append(tuple((layer, layer.GetPersistentLocking())))
            layer.IsLocked = False
        self.layersUnLocked = True
        return

    def __relockObjects(self):
        for obj_to_lock in self.prevLockedObjects:
            rs.LockObject(obj_to_lock)
        self.objectUnLocked = False
        return

    def __relockLayers(self):
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
