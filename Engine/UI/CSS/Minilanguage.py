# File name: Minilanguage.py
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

from Properties import *
from Properties import BaseBox
from Selectors import *
from Selectors import AttributeClass, AttributeExists, AttributeValue
from Values import *
from Rules import Rule
from Literals import *

class StylesheetNamespace(object):
    image = Image
    gradient = Gradient
    step = GradientStep
    rgba = RGBA
    hsva = HSVA
    hsla = HSLA
    stretch = Stretch
    repeat = Repeat
    rect = Rect
    url = URLLiteral

    _tokenBlacklist = ["evaluateCall", "get"]

    def evaluateCall(self, call, *args):
        call = self.get(call)
        return call(*args)

    def get(self, token):
        token.lower()
        if token.startswith("_") or token in self._tokenBlacklist or not hasattr(self, token):
            raise ValueError("Function {0} not defined in css".format(token))
        return getattr(self, token)

namespace = StylesheetNamespace()