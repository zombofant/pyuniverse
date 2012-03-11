from __future__ import unicode_literals, print_function, division
from our_future import *

import numpy as np

class NPManager(object):
    def __init__(self, initialArraySize, updateFrameSize, **kwargs):
        super(NPManager, self).__init__(**kwargs)
        self._rawData = np.zeros((3, initialArraySize))
        self.Data = self._rawData.T
        self._freeRows = set(range(0, initialArraySize))
        self.UpdateFrameSize = updateFrameSize

    @property
    def UpdateFrameSize(self):
        return self._updateFrameSize

    @UpdateFrameSize.setter
    def UpdateFrameSize(self, value):
        self._updateFrameSize = float(value)
        self._updateMatrix = np.array([
            [1, value, 0.5*value*value],
            [0,     1,           value],
            [0,     0,               1]
        ])

    def _expand(self):
        oldData = self.Data
        oldLen = len(oldData)
        self.Data = np.zeros((oldLen*2,3))
        self.Data[0:oldLen,:] = oldData

    def _getFreeRow(self):
        try:
            return self._freeRows.pop()
        except KeyError:
            self._expand()
            return self.allocateXVAValue()

    def allocateXVAValue(self):
        index = self._getFreeRow()
        self.Data[index] = (0, 0, 0)
        return index

    def deallocateXVAValue(self, index):
        assert not index in self._freeRows
        self._freeRows.add(index)

    def allocateXVAVector(self):
        indicies = [self._getFreeRow(), self._getFreeRow(), self._getFreeRow()]
        for index in indicies:
            self.Data[index] = (0, 0, 0)
        return indicies

    def deallocateXVAVector(self, vecIndicies):
        assert len(vecIndicies) != 3
        self._freeRows.update(vecIndicies)

    def update(self):
        self._rawData = np.dot(self._updateMatrix, self._rawData)
        self.Data = self._rawData.T

class XVAValue(object):
    def __init__(self, npManager, **kwargs):
        self._npManager = npManager
        self._rowIndex = npManager.allocateXVAValue()

    @property
    def Tuple(self):
        return tuple(self._npManager.Data[self._rowIndex])

    @Tuple.setter
    def Tuple(self, value):
        assert len(value) == 3
        self._npManager.Data[self._rowIndex] = value

    @property
    def Position(self):
        return self._npManager.Data[self._rowIndex,0]

    @Position.setter
    def Position(self, value):
        self._npManager.Data[self._rowIndex,0] = value

    @property
    def Velocity(self):
        return self._npManager.Data[self._rowIndex,1]

    @Velocity.setter
    def Velocity(self, value):
        self._npManager.Data[self._rowIndex,1] = value
        
    @property
    def Acceleration(self):
        return self._npManager.Data[self._rowIndex,2]

    @Acceleration.setter
    def Acceleration(self, value):
        self._npManager.Data[self._rowIndex,2] = value


class XVAVector(object):
    def __init__(self, npManager, **kwargs):
        self._npManager = npManager
        self._rowIndicies = npManager.allocateXVAVector()

    @property
    def Position(self):
        data = self._npManager.Data
        indicies = self._rowIndicies
        return (data[indicies[0],0], data[indicies[1],0], data[indicies[2],0])

    @Position.setter
    def Position(self, value):
        data = self._npManager.Data
        indicies = self._rowIndicies
        data[indicies[0],0] = value[0]
        data[indicies[1],0] = value[1]
        data[indicies[2],0] = value[2]

    @property
    def Velocity(self):
        data = self._npManager.Data
        indicies = self._rowIndicies
        return (data[indicies[0],1], data[indicies[1],1], data[indicies[2],1])

    @Velocity.setter
    def Velocity(self, value):
        data = self._npManager.Data
        indicies = self._rowIndicies
        data[indicies[0],1] = value[0]
        data[indicies[1],1] = value[1]
        data[indicies[2],1] = value[2]
        
    @property
    def Acceleration(self):
        data = self._npManager.Data
        indicies = self._rowIndicies
        return (data[indicies[0],2], data[indicies[1],2], data[indicies[2],2])

    @Acceleration.setter
    def Acceleration(self, value):
        data = self._npManager.Data
        indicies = self._rowIndicies
        data[indicies[0],2] = value[0]
        data[indicies[1],2] = value[1]
        data[indicies[2],2] = value[2]
