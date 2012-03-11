# File name: NPManager.py
# This file is part of: pyuni
#
# LICENSE
#
# The contents of this file are subject to the Mozilla Public License
# Version 1.1 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See
# the License for the specific language governing rights and limitations
# under the License.
#
# Alternatively, the contents of this file may be used under the terms
# of the GNU General Public license (the  "GPL License"), in which case
# the provisions of GPL License are applicable instead of those above.
#
# FEEDBACK & QUESTIONS
#
# For feedback and questions about pyuni please e-mail one of the
# authors named in the AUTHORS file.
########################################################################
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
