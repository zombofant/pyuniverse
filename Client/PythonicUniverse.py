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

import StringIO
from OpenGL.GL import *
import math
import pyglet
import pyglet.window.key as key
import os
import sys
import numpy as np

from Engine.Application import Window, Application
from Engine.UI import SceneWidget, VBox, HBox
from Engine.VFS.FileSystem import XDGFileSystem, MountPriority
from Engine.VFS.Mounts import MountDirectory
from Engine.Resources.Manager import ResourceManager
import Engine.Resources.TextureLoader
import Engine.Resources.ModelLoader
import Engine.Resources.CSSLoader
import Engine.Resources.MaterialLoader
import Engine.Resources.ShaderLoader
from Engine.GL.Shader import Shader
from Engine.GL.RenderModel import RenderModel
from Engine.UI.Theme import Theme

class Scene(SceneWidget):
    def __init__(self, parent, **kwargs):
        super(Scene, self).__init__(parent)
        self.rotX = 0.
        self.rotZ = 0.
        self._testModel = ResourceManager().require('die.obj', RenderModel)
    
    def renderScene(self):
        self._setupProjection()
        glEnable(GL_CULL_FACE)
        glEnable(GL_TEXTURE_2D)
        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(self.rotX, 1.0, 0.0, 0.0)
        glRotatef(self.rotZ, 0.0, 0.0, 1.0)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glScalef(0.35,0.35,0.35)
        self._testModel.draw()
        glLoadIdentity()
        self._resetProjection()
        glDisable(GL_CULL_FACE)

    def update(self, timeDelta):
        self.rotX += timeDelta * 30.0
        self.rotZ += timeDelta * 45.0
        self.rotX -= (self.rotX // 360) * 360
        self.rotZ -= (self.rotZ // 360) * 360
        # print(timeDelta)

class PythonicUniverse(Application):
    def __init__(self, mountCWDData=True, **kwargs):
        super(PythonicUniverse, self).__init__(**kwargs)
        vfs = XDGFileSystem('pyuniverse')
        if mountCWDData:
            vfs.mount('/data', MountDirectory(os.path.join(os.getcwd(), "data")), MountPriority.FileSystem)

        ResourceManager(vfs)

        self.theme = Theme()
        self.theme.addRules(ResourceManager().require("ui.css"))

        mainScreen = self.windows[0][1]

        scene = Scene(mainScreen)
        self.addSceneWidget(scene)

        vbox = VBox(mainScreen)
        hbox1 = HBox(vbox)
        hbox1.StyleClasses.add("test")
        hbox2 = HBox(vbox)
        vbox21 = VBox(hbox2)
        vbox21.StyleClasses.add("test")
        vbox22 = VBox(hbox2)
        
        self.theme.applyStyles(self)

        self._uiShader = ResourceManager().require("/data/shaders/ui.shader", uniforms={
            "upsideDownHelper": glUniform2fv
        })
        self._upsideDownHelper = [
            np.asarray([1.0, 0.0], dtype=np.float32),
            np.asarray([-1.0, self.AbsoluteRect.Height], dtype=np.float32)
        ]
        self._uiShader.bind()
        glUniform2fv(self._uiShader["upsideDownHelper"], 1, self._upsideDownHelper[1])
        # self._uiShader["upsideDownHelper"] = self._upsideDownHelper[1]
        Shader.unbind()

    def onKeyDown(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            # FIXME: make this without an pyglet.app reference
            pyglet.app.exit()

    def render(self):
        self._uiShader.bind()
        super(PythonicUniverse, self).render()
        Shader.unbind()

    @property
    def UpsideDownMode(self):
        return self._upsideDownMode

    @UpsideDownMode.setter
    def UpsideDownMode(self, enabled):
        enabled = bool(enabled)
        if enabled:
            self._uiShader["upsideDownHelper"] = self._upsideDownHelper[1]
        else:
            self._uiShader["upsideDownHelper"] = self._upsideDownHelper[0]
