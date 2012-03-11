# File name: test_Tuples.py
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

import gc
import unittest

import NPManager
import Tuples

class NPManagerTest(unittest.TestCase):
    def setUp(self):
        self.manager = NPManager.NPManager(32, 1.0)

    def tearDown(self):
        del self.manager

    def test_XVAValue(self):
        value = Tuples.XVAValue(self.manager)
        self.assertEqual(value.Position, 0)
        self.assertEqual(value.Velocity, 0)
        self.assertEqual(value.Acceleration, 0)
        value.Acceleration = 1.0
        self.manager.update()
        self.assertEqual(value.Acceleration, 1.0)
        self.assertEqual(value.Velocity, 1.0)
        self.assertEqual(value.Position, 0.5)

    def test_XVAVector(self):
        vec = Tuples.XVAVector(self.manager)
        vec.Acceleration = (0.5, 1.0, 2.0)
        self.manager.update()
        self.assertSequenceEqual(vec.Position, (0.25, 0.5, 1.0))
        self.assertSequenceEqual(vec.Velocity, (0.5, 1.0, 2.0))
        self.assertSequenceEqual(vec.Acceleration, (0.5, 1.0, 2.0))

    def test_delValue(self):
        value = Tuples.XVAValue(self.manager)
        self.assertEqual(self.manager.FreeTuples, 31)
        del value
        # XXX: This test will most likely fail if pypy changes a bit.
        gc.enable()
        gc.collect()
        self.assertEqual(self.manager.FreeTuples, 32)

    def test_delVector(self):
        value = Tuples.XVAVector(self.manager)
        self.assertEqual(self.manager.FreeTuples, 29)
        del value
        # XXX: This test will most likely fail if pypy changes a bit.
        gc.enable()
        gc.collect()
        self.assertEqual(self.manager.FreeTuples, 32)
        
