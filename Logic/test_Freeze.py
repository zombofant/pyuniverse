# File name: test_Freeze.py
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

from Freeze import Frozen
from Object import TradableObject

class Freeze(unittest.TestCase):
    """def test_TradableObject(self):
        t = TradableObject()
        t._minPrice = 10
        t._maxPrice = 100
        t._sizeMagnitude = 2
        t._sizeValue = 1
        d = dict()
        self.assertRaises(TypeError, hash, t)
        self.assertRaises(TypeError, d.__setitem__, t, 10)
        Frozen(t)
        self.assertRaises(RuntimeError, setattr, t, "_minPrice", 20)
        self.assertEqual(hash(t), hash(t))
        d[t] = 10
        self.assertEqual(d[t], 10)"""