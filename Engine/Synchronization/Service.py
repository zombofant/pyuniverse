# File name: Service.py
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

from IDManagement import IDManager, MasterIDManager, LocalIDManager

class Synchronization(object):
    """
    A service singleton which handles synchronization between multiple
    server segments.
    """
    
    __singleton = None
    
    def __new__(cls, *args, **kwargs):
        if cls is Synchronization:
            raise TypeError("Cannot instanciate Synchronization directly. Set a synchronization class by setting Logic.Synchronization.SyncClass")
        if Synchronization.__singleton is not None:
            return Synchronization.__singleton
        else:
            instance = super(type(Synchronization), cls).__new__(cls, *args, **kwargs)
            Synchronization.__singleton = instance
            return instance

    def __init__(self, **kwargs):
        if not hasattr(self, "_initialized"):
            super(Synchronization, self).__init__(**kwargs)
            self._initialized = True
            self._clients = set()
            self._properties = weakref.WeakKeyDictionary()
            self._idManager = self.createIDManager()

    def addClient(self, client):
        self._clients.add(client)

    def deleteClient(self, client):
        if not client in self._clients:
            return
        for prop, instance in client:
            self.removeSubscription(prop, instance, client)
        self._clients.remove(client)

    def addSubscription(self, property, instance, client):
        self._properties.setdefault(property, {}).setdefault(instance, set()).add(client)

    def removeSubscription(self, property, instance, client):
        self._properties.setdefault(property, {}).get(instance, set()).remove(client)

    def iterSubscriptions(self, property, instance):
        return iter(self._properties.setdefault(property, {}).get(instance, ()))

    def getUniqueID(self):
        return self._idManager.allocateOne()

    def createIDManager(self):
        return IDManager()


SyncClass = Synchronization

class SyncMasterServer(Synchronization):
    def __init__(self, **kwargs):
        super(SyncMasterServer, self).__init__(**kwargs)

    def createIDManager(self):
        return MasterIDManager()
