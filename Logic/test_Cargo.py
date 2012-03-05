# File name: test_Cargo.py
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

from Cargo import Cargo, QuotaCargo
from Object import TradableObject
from Errors import *

class CargoTestCase(unittest.TestCase):
    def _createWare(self, magnitude, value):
        # FIXME: replace by Ware instances
        ware = TradableObject()
        ware._sizeMagnitude = magnitude
        ware._sizeValue = value
        return ware
    
    def setUp(self):
        self.wareS = self._createWare(1, 1)
        self.wareM = self._createWare(2, 1)
        self.wareL = self._createWare(5, 1)
        self.wareXL = self._createWare(10, 1)
        self.wareST = self._createWare(100, 1)

    def tearDown(self):
        del self.wareS
        del self.wareM
        del self.wareL
        del self.wareXL
        del self.wareST

class CargoTest(CargoTestCase):
    def _setupCargo(self, maxMagnitude, capacity):
        cargo = Cargo(maxMagnitude, capacity)
        return cargo

    def test_add(self):
        cargo = self._setupCargo(5, 10)
        cargo.add(self.wareS, 10)
        self.assertEqual(cargo.UsedCapacity, 10)
        self.assertRaises(CapacityError, cargo.add, self.wareS, 1)
        self.assertIn(self.wareS, cargo)
        self.assertNotIn(self.wareM, cargo)
        self.assertSequenceEqual(list(cargo), [(self.wareS, 10)])
        self.assertEqual(cargo[self.wareS], 10)

    def test_remove(self):
        cargo = self._setupCargo(5, 10)
        cargo.add(self.wareS, 10)
        cargo.remove(self.wareS, 1)
        self.assertEqual(cargo.UsedCapacity, 9)
        self.assertEqual(cargo[self.wareS], 9)

    def test_magnitude(self):
        cargo = self._setupCargo(2, 10)
        self.assertRaises(MagnitudeError, cargo.add, self.wareL, 1)
        self.assertEqual(cargo.UsedCapacity, 0)

    def test_resize(self):
        cargo = self._setupCargo(2, 10)
        self.assertEqual(cargo.UsedCapacity, 0)
        self.assertEqual(cargo.Capacity, 10)
        cargo.add(self.wareS, 5)
        self.assertRaises(ContainerError, setattr, cargo, "Capacity", 4)
        cargo.Capacity = 5
        self.assertEqual(cargo.Capacity, 5)
        

class QuotaCargoTest(CargoTestCase):
    def setUp(self):
        super(QuotaCargoTest, self).setUp()
        self.wareL2 = self._createWare(self.wareL.SizeMagnitude, self.wareL.SizeValue)
    
    def _setupCargo(self):
        cargo = QuotaCargo(
            10,
            100,
            [
                ([self.wareS, self.wareM], 30, True),
                ([self.wareL], 20, False),
                (None, 10, False)
            ]
        )
        self.assertEqual(cargo.Capacity, 100)
        return cargo

    def test_add(self):
        cargo = self._setupCargo()
        cargo.add(self.wareS, 30)
        self.assertEqual(cargo.UsedCapacity, 30)
        self.assertRaises(QuotaCapacityError, cargo.add, self.wareS, 1)
        self.assertRaises(QuotaCapacityError, cargo.add, self.wareM, 1)
        cargo.add(self.wareL, 4)
        self.assertEqual(cargo.UsedCapacity, 50)
        self.assertRaises(QuotaCapacityError, cargo.add, self.wareL, 1)
        cargo.add(self.wareXL, 1)
        self.assertEqual(cargo.UsedCapacity, 60)
        self.assertRaises(QuotaCapacityError, cargo.add, self.wareXL, 1)
        self.assertRaises(MagnitudeError, cargo.add, self.wareST, 1)
        self.assertEqual(cargo[self.wareS], 30)
        self.assertEqual(cargo[self.wareL], 4)
        self.assertEqual(cargo[self.wareXL], 1)
        self.assertEqual(cargo[self.wareST], 0)
        self.assertEqual(cargo[self.wareL2], 0)

    def test_remove(self):
        cargo = self._setupCargo()
        cargo.add(self.wareS, 30)
        cargo.remove(self.wareS, 10)
        self.assertEqual(cargo.UsedCapacity, 20)
        self.assertEqual(cargo[self.wareS], 20)

    def test_overflow(self):
        cargo = self._setupCargo()
        cargo.add(self.wareM, 10)
        cargo.add(self.wareS, 20)
        self.assertEqual(cargo.UsedCapacity, 40)
        self.assertEqual(cargo[self.wareS], 20)
        self.assertEqual(cargo[self.wareM], 10)

    def test_resize(self):
        cargo = self._setupCargo()
        cargo.add(self.wareM, 10)
        cargo.add(self.wareS, 10)
        cargo.Capacity = 30
        self.assertEqual(cargo.Capacity, 30)
        self.assertRaises(CapacityError, cargo.add, self.wareS, 1)
        self.assertRaises(ContainerError, setattr, cargo, "Capacity", 29)

class DyanmicQuotaCargoTest(CargoTestCase):
    def _setupCargo(self):
        cargo = QuotaCargo(
            10,
            100
        )
        self.assertEqual(cargo.Capacity, 100)
        return cargo

    def test_addQuota(self):
        cargo = self._setupCargo()
        self.assertRaises(TradableNotAllowedError, cargo.add, self.wareS, 1)
        cargo.addQuota(100, [self.wareS], False)
        cargo.add(self.wareS, 10)
        self.assertEqual(cargo[self.wareS], 10)
        self.assertRaises(TradableNotAllowedError, cargo.add, self.wareM, 1)

    def test_addTradableToQuota(self):
        cargo = self._setupCargo()
        cargo.addQuota(100, [self.wareS], False)
        cargo.add(self.wareS, 10)
        cargo.addTradableToQuota(cargo.getQuotaStack(self.wareS), self.wareM)
        cargo.add(self.wareM, 10)
        self.assertEqual(cargo[self.wareM], 10)

    def test_addDefaultQuota(self):
        cargo = self._setupCargo()
        cargo.addDefaultQuota(100)
        cargo.add(self.wareS, 1)
        self.assertEqual(cargo[self.wareS], 1)

    def test_changeQuotaeWithStoredValues(self):
        cargo = self._setupCargo()
        defaultStack = cargo.addDefaultQuota(100)
        cargo.add(self.wareS, 50)
        self.assertEqual(defaultStack[self.wareS], 50)
        stack = cargo.addQuota(50, [self.wareS])
        self.assertEqual(stack[self.wareS], 50)
        self.assertEqual(defaultStack[self.wareS], 0)
        self.assertEqual(defaultStack.UsedCapacity, 0)
        self.assertEqual(stack.UsedCapacity, 50)
        self.assertRaises(QuotaCapacityError, cargo.add, self.wareS, 1)

        cargo.add(self.wareM, 10)
        cargo.addTradableToQuota(stack, self.wareM)
        self.assertEqual(defaultStack.UsedCapacity, 0)
        self.assertEqual(stack.UsedCapacity, 70)
        self.assertEqual(stack[self.wareM], 10)
        self.assertRaises(CapacityError, cargo.add, self.wareM, 30)

        cargo.removeTradableQuota(self.wareS)
        self.assertEqual(defaultStack.UsedCapacity, 50)
        self.assertEqual(stack.UsedCapacity, 20)
        self.assertEqual(stack[self.wareS], 0)
        self.assertEqual(defaultStack[self.wareS], 50)
