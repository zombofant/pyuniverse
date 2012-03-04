# File name: Entity.py
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

class Entity(object):
    """
    This refers to a diplomatic (or more general, communication) entity,
    which other entities can make contact with.
    """

    def __init__(self, **kwargs):
        super(Entity, self).__init__(**kwargs)


class ControllerEntity(Entity):
    """
    These entities reflect a player directly attached to the server, be
    it an AI or a human player.
    """
    
    def __init__(self, **kwargs):
        super(ControllerEntity, self).__init__(**kwargs)


class MetaEntity(Entity):
    """
    Base class for meta entities like companies, nations, etc.
    """
    
    def __init__(self, **kwargs):
        super(MetaEntity, self).__init__(**kwargs)


class MicroEntity(Entity):
    """
    A micro management entity. This is a base class from which also
    Objects may derive to supply event handlers.
    """
    
    def __init__(self, **kwargs):
        super(MicroEntity, self).__init__(**kwargs)
