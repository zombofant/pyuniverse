# File name: Rect.py
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

__all__ = ["NotARect", "Rect"]

class _NotARect(object):
    def __eq__(self, other):
        if isinstance(other, _NotARect):
            return True
        elif isinstance(other, Rect):
            return False
        else:
            return NotImplemented

    def __contains__(self, other):
        if isinstance(other, (_NotARect, Rect)):
            return False
        else:
            return NotImplemented

    def __and__(self, other):
        if isinstance(other, (_NotARect, Rect)):
            return self
        else:
            return NotImplemented

    def __repr__(self):
        return "NotARect"
NotARect = _NotARect()

class Rect(object):
    @staticmethod
    def _checkDimension(value):
        if value < 0:
            raise ValueError("Rect dimensions must be non negative.")
        return value
        
    _onChange = None
        
    def __init__(self, *args):
        """
        Takes zero, two or four integer (castable) arguments.

        If none are passed, the Rect gets initialized with all
        components set to zero.

        If two are passed, these are interpreted as X and Y coordinates.
        Width and Height of the rect are still set to zero.

        If four are passed, the first two are X and Y, while the other
        two are interpreted as Right and Bottom.
        """
        self._x, self._y = 0, 0
        self._right, self._bottom = 0, 0
        self._width, self._height = 0, 0
        if len(args) == 2:
            self._x, self._y = (int(x) for x in args)
            self._right, self._bottom = 0, 0
            self._width, self._height = 0, 0
        elif len(args) == 4:
            # Lets do the checks inside the property setters
            self.X, self.Y, self.Right, self.Bottom = args
        elif len(args) != 0:
            raise ValueError("Rect takes 0, 2 or 4 int arguments.")

    @property
    def X(self):
        return self._x

    @X.setter
    def X(self, value):
        value = int(value)
        if self._x == value:
            return
        self._x = value
        self._right = self._x + self._width
        if self._onChange is not None:
            self._onChange()

    @property
    def Y(self):
        return self._y

    @Y.setter
    def Y(self, value):
        value = int(value)
        if self._y == value:
            return
        self._y = value
        self._bottom = self._y + self._height
        if self._onChange is not None:
            self._onChange()

    @property
    def Left(self):
        return self._x

    @Left.setter
    def Left(self, value):
        value = int(value)
        if self._x == value:
            return
        if value > self._right:
            raise ValueError("Left must be smaller than or equal to right.")
        self._x = value
        self._width = self._right - self._x
        if self._onChange is not None:
            self._onChange()

    @property
    def Top(self):
        return self._y

    @Top.setter
    def Top(self, value):
        value = int(value)
        if self._y == value:
            return
        if value > self._bottom:
            raise ValueError("Top must be smaller than or equal to bottom.")
        self._y = value
        self._height = self._bottom - self._y
        if self._onChange is not None:
            self._onChange()

    @property
    def Width(self):
        return self._width

    @Width.setter
    def Width(self, value):
        value = int(value)
        if self._width == value:
            return
        self._width = self._checkDimension(value)
        self._right = self._x + self._width
        if self._onChange is not None:
            self._onChange()

    @property
    def Height(self):
        return self._height

    @Height.setter
    def Height(self, value):
        value = int(value)
        if self._height == value:
            return
        self._height = self._checkDimension(value)
        self._bottom = self._y + self._height
        if self._onChange is not None:
            self._onChange()

    @property
    def Right(self):
        return self._right

    @Right.setter
    def Right(self, value):
        value = int(value)
        if self._right == value:
            return
        if value < self._x:
            raise ValueError("Right must be larger than or equal to left.")
        self._right = value
        self._width = self._right - self._x
        if self._onChange is not None:
            self._onChange()

    @property
    def Bottom(self):
        return self._bottom

    @Bottom.setter
    def Bottom(self, value):
        value = int(value)
        if self._bottom == value:
            return
        if value < self._y:
            raise ValueError("Bottom must be larger than or equal to top.")
        self._bottom = value
        self._height = self._bottom - self._y
        if self._onChange is not None:
            self._onChange()

    def transpose(self, byX, byY):
        self.X = self._x + byX
        self.Y = sefl._y + byY

    def assign(self, other):
        if not isinstance(other, Rect):
            raise TypeError("Expected Rect, got {0}".format(type(other)))
        self._x, self._y, self._width, self._height = other._x, other._y, other._width, other._height
        self._right, self._bottom = other._right, other._bottom
        if self._onChange is not None:
            self._onChange()

    @property
    def XYWH(self):
        return self._x, self._y, self._width, self._height

    @XYWH.setter
    def XYWH(self, t):
        x, y, w, h = t
        self._x = int(x)
        self._y = int(y)
        self._width = self._checkDimension(w)
        self._height = self._checkDimension(h)
        self._right = self._x + self._width
        self._bottom = self._y + self._height
        if self._onChange is not None:
            self._onChange()

    def __eq__(self, other):
        if isinstance(other, _NotARect):
            return False
        elif isinstance(other, Rect):
            return self._x == other._x and self._y == other._y and self._width == other._width and self._height == other._height
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, _NotARect):
            return True
        elif isinstance(other, Rect):
            return self._x != other._x or self._y != other._y or self._width != other._width or self._height != other._height
        else:
            return NotImplemented

    def __and__(self, other):
        if isinstance(other, _NotARect):
            return NotARect
        if not isinstance(other, Rect):
            return NotImplemented
        x, y = max(self._x, other._x), max(self._y, other._y)
        r, b = min(self._right, other._right), min(self._bottom, other._bottom)
        if r < x or b < y:
            return NotARect
        return Rect(x, y, r, b)

    def __contains__(self, other):
        if isinstance(other, _NotARect):
            return True
        if isinstance(other, Rect):
            return self._x <= other._x and self._y <= other._y and self._right >= other._right and self._bottom >= other._bottom
        try:
            x, y = other
        except (ValueError, TypeError):
            return NotImplemented
        return x >= self._x and x < self._right and y >= self._y and y < self._bottom

    def __repr__(self):
        return "Rect({0}, {1}, {2}, {3})".format(self._x, self._y, self._right, self._bottom)