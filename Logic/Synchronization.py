# File name: Synchronization.py
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

class Synchronization(object):
    __singleton = None
    
    def __new__(cls, *args, **kwargs):
        if cls is Synchronization:
            raise TypeError("Cannot instanciate Synchronization directly. Set a synchronization class by setting Logic.Synchronization.SyncClass")
        if cls.__singleton is not None:
            return cls.__singleton
        else:
            return super(type(Synchronization), cls).__init__(*args, **kwargs)

    def __init__(self, **kwargs):
        if not hasattr(self, "_initialized"):
            super(Synchronization, self).__init__(**kwargs)
            self._initialized = True
            self._clients = set()
            self._properties = {}

    def newClient(self):
        client = Client()
        self._clients.add(client)
        return client

    def deleteClient(self, client):
        if not client in self._clients:
            return
        for prop, instance in client:
            self.removeSubscription(prop, instance, client)
        self._clients.remove(client)

    def removeSubscription(self, property, instance, client):
        self._properties[property].get(instance, set()).remove(client)

    def iterSubscriptions(self, property, instance):
        return iter(self._properties[property].get(instance, ()))

class SynchronizedProperty(object):
    def __init__(self, getter, setter=None, deleter=None):
        super(SynchronizedProperty, self).__init__()
        self._getter = getter
        self._setter = None
        self._deleter = None
        self._sync = SyncClass()

    def __get__(self, instance, owner):
        return self._getter(instance) if instance is not None else self

    def __set__(self, instance, value):
        if self._setter is None:
            raise AttributeError("Can't set attribute")
        newValue = self._setter(instance, value)
        for client in self._sync.iterSubscriptions(self, instance):
            client.update((prop, instance), value)

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

class Client(object):
    def __init__(self, **kwargs):
        assert synchronization is Synchronization()
        super(Client, self).__init__(**kwargs)
        self.Subscriptions = set()
        self._sync = SyncClass()
        self._updates = {}

    def __iter__(self):
        return iter(self.Subscriptions)

    def subscribe(self, prop, instance):
        assert isinstance(prop, SynchronizedProperty)
        self.Subscriptions.add((prop, instance))

    def unsubscribe(self, prop, instance):
        t = (prop, instance)
        subscriptions = self.Subscriptions
        if not t in subscriptions:
            return
        subscriptions.remove(t)
        self._sync.removeSubscription(prop, instance, self)

    def update(self, prop_instance, value):
        assert prop_instance in self.Subscriptions
        self._updates[prop_instance] = value

SyncClass = Synchronization
"""
SyncClass is the class to be used for synchronization. This must,
obviously, be set really early in the initialization process. At best
right after startup.

A client may subclass Synchronization to include the server for example.
"""
