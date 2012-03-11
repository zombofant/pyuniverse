# File name: test_Properties.py
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

import Service
import TestLocal

import Properties
import Tuples

class TestClass(object):
    def __init__(self, value=0):
        self._value = value
    
    @Properties.SynchronizedProperty
    def TestProp(self):
        return self._value

    @TestProp.setter
    def TestProp(self, value):
        self._value = value
        return value

    TestTuple = Properties.XVAProperty(Service.SyncClass().NPManager, Tuples.XVAValue)


class TestClassTest(TestLocal.SyncTestCase):
    def setUp(self):
        super(TestClassTest, self).setUp()
        self.obj = TestClass()

    def tearDown(self):
        del self.obj


class SynchronizedProperty(TestClassTest):
    def test_getFromClass(self):
        self.assertIsInstance(TestClass.TestProp, Properties.SynchronizedProperty)
    
    def test_assign(self):
        self.client.subscribe(TestClass.TestProp, self.obj)
        self.obj.TestProp = 10
        self.obj.TestProp = 20
        self.assertEqual(
            self.client.flushFrame(),
            {
                (TestClass.TestProp, self.obj): 20
            }
        )


class SynchronizedTuple(TestClassTest):
    def test_getFromClass(self):
        self.assertIsInstance(TestClass.TestTuple, Properties.XVAProperty)

    def test_tuple(self):
        self.client.subscribe(TestClass.TestTuple, self.obj)
        self.obj.TestTuple.Position = 1.0
        self.assertEqual(
            self.client.flushFrame(),
            {
                (TestClass.TestTuple, self.obj): (1.0, 0.0, 0.0)
            }
        )
