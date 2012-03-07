# File name: Sector.py
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

from Object import OwnableObject, PositionableObject

class Sector(OwnableObject):
    def __init__(self, **kwargs):
        super(Sector, self).__init__(**kwargs)
        # XXX: is a set actually okay? We do not need sorting. This may
        # yield problems though if we change __hash__ functions for any
        # positionable object (which should not happen indeed)
        self._objects = set()
        self._globalPosition = None

    def add(self, obj):
        if not isinstance(obj, PositionableObject):
            raise TypeError("Sector objects must be PositionableObjects. Got {0} {1}".format(type(obj), obj))
        self._objects.add(obj)

    def remove(self, obj):
        self._objects.remove(obj)

    def __iter__(self):
        return iter(self._objects)

    def __len__(self):
        return len(self._objects)

    def __contains__(self, obj):
        return obj in self._objects
