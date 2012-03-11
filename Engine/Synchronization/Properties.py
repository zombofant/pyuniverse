# File name: Properties.py
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

from Synchronization import SyncClass

import functools

class SynchronizedProperty(object):
    def __init__(self, getter, setter=None, deleter=None):
        super(SynchronizedProperty, self).__init__()
        self._getter = getter
        self._setter = None
        self._deleter = None
        self._sync = SyncClass()

    def __get__(self, instance, owner):
        return self._getter(instance) if instance is not None else self

    def update(self, prop_instance, newValue, client):
        client.update(prop_instance, newValue)

    def mapValue(self, value):
        return value

    def __set__(self, instance, value):
        if self._setter is None:
            raise AttributeError("Can't set attribute")
        newValue = self.mapValue(self._setter(instance, value))
        update = functools.partial(self.update, (prop, instance), newValue)
        map(update, self._sync.iterSubscriptions(self, instance))

    def __delete__(self, instance):
        # deletion should do a setting to a default value
        if self._deleter is None:
            raise AttributeError("Can't delete attribute")

    def setter(self, setter):
        self._setter = setter
        return self

    def deleter(self, deleter):
        self._deleter = deleter
        return self

class ObjectProperty(SynchronizedProperty):
    def mapValue(self, value):
        return value.ID
