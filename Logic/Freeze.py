# File name: Freeze.py
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

def __frozensetattr__(self, attr, value):
    raise RuntimeError("Attempt to do {1}={2} on frozen {0}.".format(self, attr, repr(value)))

def Frozen(instance):
    if hasattr(instance.__class__, "__frozenhash__"):
        class Frozen(instance.__class__):
            __setattr__ = __frozensetattr__
            __hash__ = instance.__class__.__frozenhash__
            __eq__ = instance.__class__.__eq__

            def __repr__(self):
                return "Frozen({0})".format(super(Frozen, self).__repr__())
        instance.Frozen = True
        instance.__class__ = Frozen
        return instance
    else:
        raise RuntimeError("Cannot freeze {0} instances.".format(type(instance)))
