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
    def __init__(self, namespace, namespaceSize, **kwargs):
        super(IDManager, self).__init__(**kwargs)
        self._namespace = namespace
        self._currentIterable = [range(namespace, namespace+namespaceSize)]
        self._iterables = [set()]
        self._maxNamespace = namespace + namespaceSize

    def allocateOne(self):
        try:
            return next(self._currentIterable)
        except StopIteration:
            try:
                self._currentIterable = self._iterables.pop()
            except IndexError:
                # TODO: Allocate a new group of IDs here
                raise NotImplementedError("Cannot get new IDs.")
            return next(self._currentIterable)

    def releaseOne(self, id):
        if id >= self._namespace and id < self._maxNamespace:
            self._iterables.append((id,))
        
