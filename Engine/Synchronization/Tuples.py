from __future__ import unicode_literals, print_function, division
from our_future import *

import numpy as np

class NPManager(object):
    """
    Manages a numpy storage for XVA values.

    Uses a large numpy array to enable any logic to update all XVA
    (Position, Velocity, Acceleration) values at once.
    """
    
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
        """
        Allocates one row of the numpy storage for an XVA value. This
        may expand the array, so is potentially a costly operation.
        """
        index = self._getFreeRow()
        self.Data[index] = (0, 0, 0)
        return index

    def deallocateXVAValue(self, index):
        assert not index in self._freeRows
        self._freeRows.add(index)

    def allocateXVAVector(self):
        """
        Allocates three rows of numpy storage for a XVA vector. This may
        expand the array, so is potentially a costly operation.
        """
        indicies = [self._getFreeRow(), self._getFreeRow(), self._getFreeRow()]
        for index in indicies:
            self.Data[index] = (0, 0, 0)
        return indicies

    def deallocateXVAVector(self, vecIndicies):
        assert len(vecIndicies) == 3
        self._freeRows.update(vecIndicies)

    def update(self):
        """
        Advances the simulation by a step of length *UpdateFrameSize*.
        """
        self._rawData = np.dot(self._updateMatrix, self._rawData)
        self.Data = self._rawData.T

    @property
    def FreeTuples(self):
        return len(self._freeRows)

class XVAValue(object):
    """
    Makes a row in the NPManager accessible as a Tuple or individual
    values.
    """
    
    def __init__(self, npManager, **kwargs):
        self._npManager = npManager
        self._rowIndex = npManager.allocateXVAValue()

    def __del__(self):
        self._npManager.deallocateXVAValue(self._rowIndex)

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
    """
    Makes a vector in the NPManager accessible as individual vectors for
    position, velocity and acceleration.
    """
    
    def __init__(self, npManager, **kwargs):
        self._npManager = npManager
        self._rowIndicies = npManager.allocateXVAVector()

    def __del__(self):
        self._npManager.deallocateXVAVector(self._rowIndicies)

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
