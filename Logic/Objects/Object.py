# File name: Object.py
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
"""
Base for all game objects and the default object types
"""

from __future__ import unicode_literals, print_function, division
from our_future import *

from Logic.Synchronization.Service import SyncClass

class Object(object):
    """
    Base class for all game objects.
    """
    
    def __init__(self, id=None, **kwargs):
        super(Object, self).__init__(**kwargs)
        self._id = id or SyncClass().getUniqueID()

    def iterEntities(self):
        """
        Returns an iterable which yields all directly associated
        entities of the given object. The actual meaning depends on the
        Object itself, but iterate over all entities of these entities
        should yield all entities one can concact using this Object.
        """
        return ()

    @property
    def ID(self):
        return self._id


class Entity(Object):
    """
    This refers to a diplomatic (or more general, communication) entity,
    which other entities can make contact with.
    """

    def __init__(self, **kwargs):
        super(Entity, self).__init__(**kwargs)


class PositionableObject(Object):
    """
    Base class for any object which is positionable in a sector.
    """
    
    def __init__(self, **kwargs):
        super(PositionableObject, self).__init__(**kwargs)
        self._sector = None
        self._position = None


class TradableObject(Object):
    """
    Base class for any tradable object; that is an object which can be
    carried in a cargo bay and traded in a station.
    """
    
    def __init__(self, **kwargs):
        super(TradableObject, self).__init__(**kwargs)
        self._minPrice = None
        self._maxPrice = None
        self._sizeValue = None
        self._sizeMagnitude = None

    @property
    def Size(self):
        return self._sizeMagnitude * self._sizeValue

    @property
    def SizeMagnitude(self):
        return self._sizeMagnitude

    @property
    def SizeValue(self):
        return self._sizeValue


class OwnableObject(Object):
    """
    Any object which can have one or more owner entities assigned 
    """
    
    def __init__(self, **kwargs):
        super(OwnableObject, self).__init__(**kwargs)
        self._owner = None

    @property
    def Owner(self):
        return self._owner

    @Owner.setter
    def Owner(self, value):
        if not isinstance(value, Entity):
            raise TypeError("OwnableObject Owner must be an Entity. Got {0} {1}".format(type(value), value))
        self._owner = value


