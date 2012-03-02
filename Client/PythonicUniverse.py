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

from OpenGL.GL import *
import math
import pyglet
import pyglet.window.key as key
import os
import sys

from Engine.Application import Window, Application
from Engine.UI import SceneWidget
from Engine.VFS.FileSystem import XDGFileSystem, MountPriority
from Engine.VFS.Mounts import MountDirectory
from Engine.Resources.Manager import ResourceManager
from Engine.Resources.TextureLoader import TextureLoader
from Engine.Resources.ModelLoader import OBJModelLoader
from Engine.GL.RenderModel import RenderModel
from Engine.GL.SceneGraph.Core import SceneGraph, Node

class Scene(SceneWidget):
    def __init__(self, parent, **kwargs):
        super(Scene, self).__init__(parent)
        self.rotX = 0.
        self.rotZ = 0.
        self._sceneGraph = SceneGraph()
        self._testModel = ResourceManager().require('die.obj', RenderModel)
        self._nodes = []
        for j in range(0,25):
            node = Node()
            node.addChild(self._testModel)
            self._nodes.append(node)
            self._sceneGraph.rootNode.addChild(node)
    
    def renderScene(self):
        self._setupProjection()
        glEnable(GL_CULL_FACE)
        glEnable(GL_TEXTURE_2D)
        #self._testNode1.LocalTransformation.scale(0.25, 0.25, 0.25)
        a = 1.1
        for j in range(0,25):
            self._nodes[j].LocalTransformation.translate(a*(j%5)-2.5, a*(j//5)-2.2,-5)
            self._nodes[j].LocalTransformation.rotate(self.rotX+j*j, 1., 0., 0.)
            self._nodes[j].LocalTransformation.rotate(self.rotZ-j*j, 0., 0., 1.)
            self._nodes[j].LocalTransformation.scale(0.3,0.3,0.3)
        self._sceneGraph.update(0)
        self._sceneGraph.renderScene()
        for j in range(0,25):
            self._nodes[j].LocalTransformation.reset()
        self._resetProjection()

    def update(self, timeDelta):
        self.rotX += timeDelta * 22.
        self.rotZ += timeDelta * 70.
        self.rotX -= (self.rotX // 360 ) * 360
        self.rotZ -= (self.rotZ // 360) * 360
        # print(timeDelta)

class PythonicUniverse(Application):
    def __init__(self, mountCWDData=True, **kwargs):
        super(PythonicUniverse, self).__init__(**kwargs)
        vfs = XDGFileSystem('pyuniverse')
        if mountCWDData:
            vfs.mount('/data', MountDirectory(os.path.join(os.getcwd(), "data")), MountPriority.FileSystem)

        ResourceManager(vfs)

        scene = Scene(self.windows[0][1])
        self.addSceneWidget(scene)

    def onKeyDown(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            # FIXME: make this without an pyglet.app reference
            pyglet.app.exit()

