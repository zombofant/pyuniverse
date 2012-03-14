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

import CUni
import CUni.GL as CGL

import StringIO
from OpenGL.GL import *
import math
import os
import sys
import numpy as np

from Engine.Application import Application
from Engine.UI import SceneWidget, VBox, HBox, LabelWidget, WindowWidget
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
from Engine.GL.SceneGraph.Core import SceneGraph, Node
from Engine.UI.Theme import Theme

class Scene(SceneWidget):
    def __init__(self, parent, **kwargs):
        super(Scene, self).__init__(parent)
        self.rotX = 0.
        self.rotZ = 0.
        self._frameN = 0
        self._frameT = 0
        self._sceneGraph = SceneGraph()
        self._testModel = ResourceManager().require('spaceship.obj', RenderModel)
        self._node = Node() #rotationsnode 
        self._sceneGraph.rootNode.addChild(self._node)
        transNode = Node()
        transNode.addChild(self._testModel)
        transNode.LocalTransformation.translate([0.,0.,-12.])
        transNode.LocalTransformation.scale([0.3,0.3,0.3])
        self._node.addChild(transNode)
 
    def renderScene(self):
        if self._frameT >= 5:
            print('%i Frames/s' % (self._frameN // 5))
            self._frameN = 0
            self._frameT -= 5
        self._setupProjection()
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glPushMatrix()
        self._node.LocalTransformation.rotate(self.rotX, [1., 0.,0.])
        self._node.LocalTransformation.rotate(self.rotZ, [0., 0.,1.])
        self._sceneGraph.update(0)
        self._sceneGraph.renderScene()
        self._node.LocalTransformation.reset()
        self._resetProjection()
        glPopMatrix()
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        self._frameN += 1

    def update(self, timeDelta):
        self.rotX += timeDelta * 5.
        self.rotZ += timeDelta * 10.
        self.rotX -= (self.rotX // 360 ) * 360
        self.rotZ -= (self.rotZ // 360) * 360
        self._frameT += timeDelta
        # print(timeDelta)

class PythonicUniverse(Application):
    def __init__(self, display, mountCWDData=True, **kwargs):
        super(PythonicUniverse, self).__init__(display, **kwargs)
        vfs = XDGFileSystem('pyuniverse')
        if mountCWDData:
            vfs.mount('/data', MountDirectory(os.path.join(os.getcwd(), "data")), MountPriority.FileSystem)

        ResourceManager(vfs)

        self.theme = Theme()
        self.theme.addRules(ResourceManager().require("ui.css"))

        mainScreen = self._primaryWidget

        #scene = Scene(mainScreen)
        #self.addSceneWidget(scene)

        window = WindowWidget(self._windowLayer)
        window.Title.Text = "Test"
        
        self.theme.applyStyles(self)

        self._shader = ResourceManager().require("/data/shaders/ui.shader")
        self._upsideDownHelper = np.asarray([-1.0, self.AbsoluteRect.Height], dtype=np.float32)
        self._shader.cacheShaders([
            {
                "texturing": True,
                "upsideDown": True
            },
            {
                "texturing": True,
                "upsideDown": False
            },
            {
                "texturing": False,
                "upsideDown": False
            },
        ])
        shader = self._shader.bind(texturing=True, upsideDown=False)
        self._shaders = [shader]
        shader.bind()
        glUniform1i(shader["texture"], 0)
        
        shader = self._shader.bind(texturing=True, upsideDown=True)
        self._shaders.append(shader)
        shader.bind()
        glUniform1i(shader["texture"], 0)
        glUniform2fv(shader["upsideDownHelper"], 1, self._upsideDownHelper)

        self._shaders.append(self._shader.bind(texturing=False, upsideDown=False))

        Shader.unbind()
        
        vf = CGL.VertexFormat("v:3;c:4")
        buffer = CGL.GeometryBuffer(vf, GL_DYNAMIC_DRAW)
        alloc = buffer.allocateVertices(3)
        view = CGL.GeometryBufferView(buffer, alloc)
        view.Vertex[0:3].set([
            1., 2., 3.,
            4., 5., 6.,
            7., 8., 9.
        ])
        view.Vertex[0:3:2].set([
            0., 0., 0.,
            0., 0., 0.
        ])
        view.Colour[0:3].set([
            1., 0., 0., 1.,
            0., 1., 0., 1.,
            0., 0., 1., 1.
        ])
        view.Vertex[:,0].set([1., 1., 1.])
        view.Vertex[:,1:2].set(
            [
                2., 3.,
                4., 2.,
                2., 1.,
            ]
        )
        print(view.Vertex.get())
        print(view.Colour.get())

    def _setUIOffset(self, x, y):
        xy = np.asarray([x, y], dtype=np.float32)
        for shader in self._shaders:
            shader.bind()
            glUniform2fv(shader["uiOffset"], 1, xy)

    def onKeyDown(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            cuni.exit()

    def render(self):
        super(PythonicUniverse, self).render()
        Shader.unbind()

    def frameUnsynced(self, deltaT):
        window = self._screens[0][0]
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glBegin(GL_TRIANGLES)
        glVertex2f(-1.0, -1.0)
        glVertex2f(1.0, 0.5)
        glVertex2f(0.5, -1.0)
        glEnd()
        window.flip()
