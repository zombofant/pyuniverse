# File name: PythonicUniverse.py
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
from Engine.Application import Window, Application
from Engine.UI import SceneWidget
from OpenGL.GL import *
import math

class Scene(SceneWidget):
    def renderScene(self):
        self._setupProjection()
        glTranslatef(0.0, 0.0, -5.0)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glBegin(GL_QUADS)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0,  1.0, -1.0)
        glVertex3f( 1.0,  1.0, -1.0)
        glVertex3f( 1.0, -1.0, -1.0)
        
        glVertex3f(-1.0, -1.0,  1.0)
        glVertex3f(-1.0,  1.0,  1.0)
        glVertex3f( 1.0,  1.0,  1.0)
        glVertex3f( 1.0, -1.0,  1.0)
        
        glVertex3f( 1.0, -1.0, -1.0)
        glVertex3f( 1.0, -1.0,  1.0)
        glVertex3f( 1.0,  1.0,  1.0)
        glVertex3f( 1.0,  1.0, -1.0)
        
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, -1.0,  1.0)
        glVertex3f(-1.0,  1.0,  1.0)
        glVertex3f(-1.0,  1.0, -1.0)
        
        glVertex3f(-1.0, -1.0,  1.0)
        glVertex3f( 1.0, -1.0, -1.0)
        glVertex3f( 1.0, -1.0, -1.0)
        glVertex3f(-1.0, -1.0,  1.0)
        
        glVertex3f(-1.0,  1.0,  1.0)
        glVertex3f( 1.0, -1.0, -1.0)
        glVertex3f( 1.0, -1.0, -1.0)
        glVertex3f(-1.0,  1.0,  1.0)
        glEnd()
        glLoadIdentity()
        self._resetProjection()

class PythonicUniverse(Application):
    def __init__(self, **kwargs):
        super(PythonicUniverse, self).__init__(**kwargs)
        scene = Scene(self.windows[0][1])
        self.addSceneWidget(scene)
