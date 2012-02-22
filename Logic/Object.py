"""
Base for all game objects and the default object types
"""

from __future__ import unicode_literals, print_function, division
from our_future import *

class Object(object):
    """
    Base for all game objects
    """

    def __init__(self, **kwargs):
        super(Object, self).__init__(self, **kwargs)

class PositionedObject(Object):
    """
    Base for all objects
    """

    def __init__(self, sector, pos, **kwargs):
        super(PositionedObject, self).__init__(self, **kwargs)
        self.sector = sector
        self.pos = pos

    @property
    def Sector(self):
        return self.sector

class WareObject(Object):
    """
    Base object for wares
    A ware object just specifies the type of a ware,
    the actual instance just references the ware type class
    """

    def __init__(self, **kwargs):
        super(WareObject, self).__init__(self, **kwargs)
