# File name: Tuples.py
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
import functools
import iterutils

from Service import Synchronizable

class XVAObject(Synchronizable):
    def __init__(self, npManager, prop=None, **kwargs):
        super(XVAObject, self).__init__(**kwargs)
        self._npManager = npManager
        self._prop = prop
        self._token = None

    def setInstance(self, instance):
        self._token = (self._prop, instance)

    def broadcast(self, value):
        token = self._token
        if token is None:
            return
        update = functools.partial(self.update, token, value)
        iterutils.consume(map(update, self._sync.iterSubscriptions(*token)), None)

class XVAValue(XVAObject):
    """
    Makes a row in the NPManager accessible as a Tuple or individual
    values.
    """
    
    def __init__(self, npManager, prop=None, **kwargs):
        super(XVAValue, self).__init__(npManager, prop, **kwargs)
        self._rowIndex = npManager.allocateXVAValue()
        self._prop = prop

    def __del__(self):
        self._npManager.deallocateXVAValue(self._rowIndex)

    @property
    def Tuple(self):
        return tuple(self._npManager.Data[self._rowIndex])

    @Tuple.setter
    def Tuple(self, value):
        assert len(value) == 3
        self._npManager.Data[self._rowIndex] = value
        self.broadcast(self.Tuple)

    @property
    def Position(self):
        return self._npManager.Data[self._rowIndex,0]

    @Position.setter
    def Position(self, value):
        self._npManager.Data[self._rowIndex,0] = value
        self.broadcast(self.Tuple)

    @property
    def Velocity(self):
        return self._npManager.Data[self._rowIndex,1]

    @Velocity.setter
    def Velocity(self, value):
        self._npManager.Data[self._rowIndex,1] = value
        self.broadcast(self.Tuple)
        
    @property
    def Acceleration(self):
        return self._npManager.Data[self._rowIndex,2]

    @Acceleration.setter
    def Acceleration(self, value):
        self._npManager.Data[self._rowIndex,2] = value
        self.broadcast(self.Tuple)


class XVAVector(XVAObject):
    """
    Makes a vector in the NPManager accessible as individual vectors for
    position, velocity and acceleration.
    """
    
    def __init__(self, npManager, prop=None, **kwargs):
        super(XVAVector, self).__init__(npManager, prop, **kwargs)
        self._rowIndicies = npManager.allocateXVAVector()

    def __del__(self):
        self._npManager.deallocateXVAVector(self._rowIndicies)

    @property
    def Tuple(self):
        return (self.Position, self.Velocity, self.Acceleration)

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
        self.broadcast(self.Tuple)

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
        self.broadcast(self.Tuple)
        
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
        self.broadcast(self.Tuple)
