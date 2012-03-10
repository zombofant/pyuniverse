# File name: IDManagement.py
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

import itertools

class IDManager(object):
    def __init__(self, **kwargs):
        if type(self) is IDManager:
            raise RuntimeError("Must not instanciate IDManager directly. Did you pick a proper Synchronization service?")
        super(IDManager, self).__init__(**kwargs)
        self._currentIterable = ()
        self._randomIDs = set()

    def _randomIterable(self):
        try:
            yield self._randomIDs.pop()
        except KeyError:
            return

    def _pickNewIterable(self):
        if len(self._randomIDs) > 0:
            self._currentIterable = self._randomIterable()
        else:
            self._getNewNamespace()

    def allocateOne(self):
        try:
            return next(self._currentIterable)
        except StopIteration:
            self._pickNewIterable()
            return next(self._currentIterable)

    def releaseOne(self, id):
        self._randomIDs.add(id)

class LocalIDManager(IDManager):
    def __init__(self, namespace=None, namespaceSize=None, masterProxy=None, **kwargs):
        super(LocalIDManager, self).__init__(**kwargs)
        if namespace is not None:
            self._currentIterable = iter(range(namespace, namespace+namespaceSize))
            self._namespaces = [(namespace, namespace + namespaceSize)]
        else:
            self._currentIterable = iter(())
            self._namespaces = []
        self._masterProxy = masterProxy

    def _getNewNamespace(self):
        if self._masterProxy is None:
            raise ValueError("Cannot get a new namespace without a master proxy on local ID manager.")
        min, size = self._masterProxy.getNewNamespace()
        self._namespaces.append((min, min + size))
        self._currentIterable = iter(range(min, min + size))

    def releaseOne(self, id):
        if id == 0:
            raise ValueError("Attempt to release NULL id.")
        for min, max in self._namespaces:
            if id >= min and id < max:
                super(LocalIDManager, self).releaseOne(id)
                return

class MasterIDManager(IDManager):
    def __init__(self, namespaceSize=4096, **kwargs):
        super(MasterIDManager, self).__init__(**kwargs)
        self._namespaceSize = namespaceSize
        self._namespaces = []
        self._returnedNamespaces = set()
        self._newNamespaceIterator = iter(itertools.count(1, self._namespaceSize))
        self._localNamespace = LocalIDManager(*self.getNewNamespace(), masterProxy=self)
        self.allocateOne = self._localNamespace.allocateOne
        self.releaseOne = self._localNamespace.releaseOne

    def getNewNamespace(self):
        if len(self._returnedNamespaces) > 0:
            namespace = self._returnedNamespaces.pop()
        else:
            namespace = next(self._newNamespaceIterator)
        self._namespaces.append(namespace)
        return (namespace, self._namespaceSize)

    @property
    def LocalNamespace(self):
        return self._localNamespace
