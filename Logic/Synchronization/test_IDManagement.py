# File name: test_IDManagement.py
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

import unittest

import IDManagement as ID

class LocalIDManager(unittest.TestCase):
    def setUp(self):
        self.manager = ID.LocalIDManager(1, 10)

    def tearDown(self):
        del self.manager
    
    def test_allocation(self):
        ids = [self.manager.allocateOne() for x in range(10)]
        self.assertSequenceEqual(ids, list(range(1, 11)))
    
    def test_outofIDs(self):
        ids = [self.manager.allocateOne() for x in range(10)]
        self.assertRaises(ValueError, self.manager.allocateOne)

    def test_reallocation(self):
        ids = [self.manager.allocateOne() for x in range(10)]
        id = ids.pop()
        self.manager.releaseOne(id)
        self.assertEqual(self.manager.allocateOne(), id)

    def test_null(self):
        self.assertRaises(ValueError, self.manager.releaseOne, 0)

class MasterIDManager(unittest.TestCase):
    def setUp(self):
        self.manager = ID.MasterIDManager(10)
        self.local = self.manager.LocalNamespace

    def tearDown(self):
        del self.manager
        del self.local
    
    def test_local(self):
        ids = [self.manager.allocateOne() for x in range(10)]
        self.assertSequenceEqual(ids, list(range(1,11)))

    def test_null(self):
        self.assertRaises(ValueError, self.manager.releaseOne, 0)

    def test_newLocal(self):
        newLocal = ID.LocalIDManager(masterProxy=self.manager)
        ids = [newLocal.allocateOne() for x in range(10)]
        self.assertSequenceEqual(ids, list(range(11,21)))
        
        
