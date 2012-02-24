# File name: BoxModel.py
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

__all__ = ["Padding", "Margin", "Border"]

class BaseBox(object):
    def __init__(self, *args):
        if len(args) == 0:
            self._left, self._right, self._top, self._bottom = 0, 0, 0, 0
        elif len(args) == 1:
            self._left, self._right, self._top, self._bottom = (int(args[0]), )*4
        elif len(args) == 4:
            self._left, self._top, self._right, self._bottom = (int(x) for x in args)
        else:
            raise ValueError("BaseBox expects 1 or 4 arguments.")

    def assign(self, value):
        if type(value) == int:
            self._left, self._right, self._top, self._bottom = value
            return
        value = tuple((int(x) for x in value))
        if len(value) != 4:
            raise ValueError("BaseBox needs a tuple of 4 ints or 1 int")
        self._left, self._right, self._top, self._bottom = value

    def _checkValue(self, v):
        if int(v) < 0:
            raise ValueError("Box value must be non negative.")
    
    @property
    def Left(self):
        return self._left

    @Left.setter
    def Left(self, value):
        if self._left == value:
            return
        self._checkValue(value)
        self._left = value

    @property
    def Right(self):
        return self._right

    @Right.setter
    def Right(self, value):
        if self._right == value:
            return
        self._checkValue(value)
        self._right = value

    @property
    def Top(self):
        return self._top

    @Top.setter
    def Top(self, value):
        if self._top == value:
            return
        self._checkValue(value)
        self._top = value

    @property
    def Bottom(self):
        return self._bottom

    @Bottom.setter
    def Bottom(self, value):
        if self._bottom == value:
            return
        self._checkValue(value)
        self._bottom = value

class Margin(BaseBox):
    pass

class Padding(BaseBox):
    pass

class Border(object):
    pass