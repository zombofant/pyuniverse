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

import weakref

from Service import SyncClass, Synchronizable

class SynchronizedProperty(Synchronizable):
    def __init__(self, getter, setter=None, deleter=None, **kwargs):
        super(SynchronizedProperty, self).__init__(**kwargs)
        self._getter = getter
        self._setter = None
        self._deleter = None

    def __get__(self, instance, owner):
        return self._getter(instance) if instance is not None else self

    def __set__(self, instance, value):
        if self._setter is None:
            raise AttributeError("Can't set attribute")
        self.broadcast(instance, self._setter(instance, value))

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

    def unmapValue(self, value):
        raise NotImplementedError("Cannot lookup ID.")


class XVAProperty(object):
    def __init__(self, npManager, XVAClass, **kwargs):
        super(XVAProperty, self).__init__(**kwargs)
        # The __get__ code relies on the WeakKeyDictionary behaviour if
        # an attempt to __getitem__ with None is made. If one decides to
        # switch the type of the dict, please make sure that the None
        # check still passes.
        self._instanceDict = weakref.WeakKeyDictionary()
        self._npManager = npManager
        self._xvaClass = XVAClass

    def __get__(self, instance, owner):
        try:
            return self._instanceDict[instance]
        except KeyError:
            obj = self._xvaClass(self._npManager, prop=self)
            obj.setInstance(instance)
            self._instanceDict[instance] = obj
            return obj
        except TypeError:
            # TypeError gets raised if the WeakKeyDictionary is unable
            # to weakref a value. So we use this as a cheap check.
            if instance is None:
                return self
            else:
                raise
