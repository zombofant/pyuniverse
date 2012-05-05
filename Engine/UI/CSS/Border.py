# File name: Border.py
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

import iterutils
import copy

from Fill import Fill, Colour, Transparent, isPlainFill
from Box import BaseBox
from Rect import Rect, NotARect

class BorderComponent(object):
    def assign(self, other):
        if not isinstance(other, BorderComponent):
            raise TypeError("Can only assign BorderComponents to BorderComponents. Got {0} {1}".format(type(other), other))
        self.Width = other.Width
        self.Fill = other.Fill

class BorderEdge(BorderComponent):
    __hash__ = None
    
    def __init__(self, width=0, fill=Transparent, **kwargs):
        self._width = None
        self._fill = None
        super(BorderEdge, self).__init__(**kwargs)
        self.Width = width
        self.Fill = fill

    def __deepcopy__(self, memo):
        return BorderEdge(self._width, copy.deepcopy(self._fill, memo)) 

    @property
    def Width(self):
        return self._width

    @Width.setter
    def Width(self, value):
        if value == self._width:
            return
        if value < 0:
            raise ValueError("Border width must be non-negative")
        self._width = value
    
    @property
    def Fill(self):
        return self._fill

    @Fill.setter
    def Fill(self, value):
        if self._fill == value:
            return
        if not isPlainFill(value):
            raise TypeError("Border needs plain fill instances as fillers (e.g. colour or transparent). Got {0} {1}".format(type(value), value))
        self._fill = value

    def __eq__(self, other):
        if not isinstance(other, BorderEdge):
            return NotImplemented
        return (self._width == other._width and
                self._fill == other._fill)

    def __ne__(self, other):
        r = self.__eq__(other)
        if r is NotImplemented:
            return r
        else:
            return not r

    def __repr__(self):
        return "BorderEdge(width={0!r}, fill={1!r})".format(self._width, self._fill)

class Border(BorderComponent):
    __hash__ = None
    
    def __init__(self, width=0, fill=None, **kwargs):
        self._edges = [BorderEdge() for i in range(4)]
        self._corners = [0] * 4
        super(Border, self).__init__(**kwargs)
        self.Width = width
        if fill is not None:
            self.Fill = fill
    
    def assign(self, other):
        if isinstance(other, Border):
            for edgeA, edgeB in zip(self._edges, other._edges):
                edgeA.Width = edgeB.Width
                edgeA.Fill = edgeB.Fill
            self._corners = list(other._corners)
        elif isinstance(other, BorderComponent): 
            for edgeA in self._edges:
                edgeA.Width = other.Width
                edgeA.Fill = other.Fill
            self._corners = [0] * 4
        else:    
            raise TypeError("Can only assign BorderComponents to Border")

    def __deepcopy__(self, memo):
        new = Border()
        for i, edge in enumerate(self._edges):
            new._edges[i] = copy.deepcopy(edge, memo)
        new._corners = list(self._corners)
        return new

    @property
    def Width(self):
        raise NotImplementedError("Cannot read global border width.")

    @Width.setter
    def Width(self, value):
        for edge in self._edges:
            edge.Width = value
    
    @property
    def Fill(self):
        raise NotImplementedError("Cannot read global border colour.")

    @Fill.setter
    def Fill(self, value):
        for edge in self._edges:
            edge.Fill = value

    @property
    def Left(self):
        return self._edges[0]

    @Left.setter
    def Left(self, value):
        self._edges[0].assign(value)

    @property
    def Top(self):
        return self._edges[1]

    @Top.setter
    def Top(self, value):
        self._edges[1].assign(value)

    @property
    def Right(self):
        return self._edges[2]

    @Right.setter
    def Right(self, value):
        self._edges[2].assign(value)

    @property
    def Bottom(self):
        return self._edges[3]

    @Bottom.setter
    def Bottom(self, value):
        self._edges[3].assign(value)


    def setRadius(self, value):
        self._corners = [value] * 4
    
    @property
    def TopLeftRadius(self):
        return self._corners[0]

    @TopLeftRadius.setter
    def TopLeftRadius(self, value):
        self._corners[0] = value

    @property
    def TopRightRadius(self):
        return self._corners[1]

    @TopRightRadius.setter
    def TopRightRadius(self, value):
        self._corners[1] = value

    @property
    def BottomRightRadius(self):
        return self._corners[2]

    @BottomRightRadius.setter
    def BottomRightRadius(self, value):
        self._corners[2] = value

    @property
    def BottomLeftRadius(self):
        return self._corners[3]

    @BottomLeftRadius.setter
    def BottomLeftRadius(self, value):
        self._corners[3] = value

    def __eq__(self, other):
        if not isinstance(other, Border):
            return NotImplemented
        for edgeA, edgeB in zip(self._edges, other._edges):
            if not edgeA == edgeB:
                return False
        return self._corners == other._corners

    def __ne__(self, other):
        r = self.__eq__(other)
        if r is NotImplemented:
            return r
        else:
            return not r

    def __repr__(self):
        return """<Border
    Left={0!r},
    Top={1!r},
    Right={2!r},
    Bottom={3!r},
    TopLeft={4!r},
    TopRight={5!r},
    BottomRight={6!r},
    BottomLeft={7!r}>""".format(self.Left, self.Top, self.Right, self.Bottom,
            self.TopLeft, self.TopRight, self.BottomRight, self.BottomLeft)

    def getBox(self):
        return BaseBox(self.Left.Width, self.Top.Width,
            self.Right.Width, self.Bottom.Width)

    def geometryForRect(self, rect, faceBuffer):
        """
        Adds geometry for this border as inner border in *rect* in
        *faceBuffer*.

        Returns the BaseBox representing this border.
        """
        box = self.getBox()
        rectsAndEdges = zip(
            rect.cut(box),
            iterutils.interleave((edge.Fill for edge in self._edges), self._corners)
        )
        prevFill = None
        for rect, fill in rectsAndEdges:
            if rect is NotARect:
                continue
            if fill is None:
                fill = prevFill
            else:
                prevFill = fill
            fill.geometryForRect(rect, faceBuffer)
        return box

    def inCairo(self, rect, cr):
        """
        Execute all instructions neccessary to draw this border as the
        inner border in *rect* on cairo context *cr*.
        """

        box = self.getBox()
        rectsAndEdges = zip(
            rect.cut(box),
            iterutils.interleave((edge.Fill for edge in self._edges), self._corners)
        )
        prevFill = None
        for rect, fill in rectsAndEdges:
            if rect is NotARect:
                continue
            if fill is None:
                fill = prevFill
            else:
                prevFill = fill
            fill.inCairo(rect, cr)

    def cairoGroupForRect(self, rect, cr):
        """
        Create and return a cairo group for this border as inner border
        in *rect*, using *cr* as cairo context.
        """
        cr.push_group()
        self.inCairo(rect, cr)
        return cr.pop_group()
