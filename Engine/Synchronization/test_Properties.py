from __future__ import unicode_literals, print_function, division
from our_future import *

import unittest

import TestLocal

import Properties

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

class SynchronizedProperty(TestLocal.SyncTestCase):
    def setUp(self):
        super(SynchronizedProperty, self).setUp()
        self.obj = TestClass()

    def tearDown(self):
        del self.obj
    
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
