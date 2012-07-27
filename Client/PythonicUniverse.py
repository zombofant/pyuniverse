# encoding=utf-8
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

import Engine.CEngine
import Engine.CEngine.GL as CGL
import Engine.CEngine.SceneGraph as CSceneGraph
import Engine.CEngine.Window.key as key
import Engine.CEngine.Pango as Pango

import cairo

import StringIO
from OpenGL.GL import *
import math
import os
import sys
import numpy as np
import gc
import time

from Engine.Application import Application
from Engine.UI import SceneWidget, VBox, HBox, LabelWidget, WindowWidget
from Engine.VFS.FileSystem import XDGFileSystem, MountPriority
from Engine.VFS.Mounts import MountDirectory
from Engine.Resources.Manager import ResourceManager
import Engine.Resources.PNGTextureLoader
import Engine.Resources.ModelLoader
import Engine.Resources.CSSLoader
import Engine.Resources.MaterialLoader
import Engine.Resources.ShaderLoader
from Engine.GL import makePOT
from Engine.GL.Shader import Shader
from Engine.GL.RenderModel import RenderModel
from Engine.GL.Texture import Texture2D
from Engine.UI.Theme import Theme
import Engine.GL.Base as GL
from Engine.UI.CSS.Rect import Rect

class Scene(SceneWidget):
    def __init__(self, parent, **kwargs):
        super(Scene, self).__init__(parent)
        self.rotX = 0.
        self.rotZ = 0.
        self._sceneGraph = CSceneGraph.SceneGraph()
        self._testModel = ResourceManager().require('spaceship.obj', RenderModel)
        self._node = CSceneGraph.Node() #rotationsnode
        self._sceneGraph.RootNode.addChild(self._node)
        transNode = CSceneGraph.Node()
        transNode.addChild(self._testModel)
        transNode.translate(0.,0.,-12.)
        transNode.scale(0.5,0.5,0.5)
        self._node.addChild(transNode)

    def renderScene(self):
        self._setupProjection()
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glPushMatrix()
        self._node.setRotation(self.rotX, 1.,0.,0.)
        self._node.rotate(self.rotZ, 0.,0.,1.)
        self._sceneGraph.update(0)
        self._sceneGraph.draw()
        self._resetProjection()
        glPopMatrix()
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)

    def update(self, timeDelta):
        self.rotX += timeDelta * 0.2
        self.rotZ += timeDelta * 0.3
        self.rotX -= (self.rotX // (2*math.pi)) * 2*math.pi
        self.rotZ -= (self.rotZ // (2*math.pi)) * 2*math.pi
        # print(timeDelta)

class LeafTest(CSceneGraph.Leaf):
    def __init__(self):
        super(LeafTest, self).__init__()

class MatTest(CGL.Class):
    def __init__(self):
        super(MatTest, self).__init__()
        self.StateGroup = CGL.StateGroup(self, 0)

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

        scene = Scene(mainScreen)
        self.addSceneWidget(scene)

        window = WindowWidget(self._windowLayer)
        window.Title.Text = "Test"
        window.AbsoluteRect.XYWH = (32, 32, 128, 128)

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
        shader = self._shader.bind(texturing=False)

        shader = self._shader.bind(texturing=True)
        glUniform1i(shader["texture"], 0)

        Shader.unbind()

    def clearCairoSurface(self):
        ctx = self._cairoContext
        ctx.set_source_rgba(0., 0., 0., 0.)
        ctx.set_operator(cairo.OPERATOR_SOURCE)
        ctx.paint()
        ctx.set_operator(cairo.OPERATOR_OVER)
        ctx.set_line_cap(cairo.LINE_CAP_SQUARE)

    def onKeyDown(self, symbol, modifiers):
        if symbol == key.Escape:
            print("bye!")
            self._eventLoop.terminate()
        elif symbol == key.f:
            if self.fullscreen:
                self._window.setWindowed(0, 800, 600)
                self.fullscreen = False
            else:
                self._window.setFullscreen(0, 0, 0, 0)
                self.fullscreen = True

    def doAlign(self):
        super(PythonicUniverse, self).doAlign()

        mainScreen = self._primaryWidget

        w, h = mainScreen.AbsoluteRect.Width, mainScreen.AbsoluteRect.Height
        if hasattr(self, "_cairoSurface") and w == self._cairoSurface.get_width() and h == self._cairoSurface.get_height():
            return
        potW, potH = makePOT(w), makePOT(h)

        self.cairoTexCoords = (w / potW, h / potH)

        self.cairoTex = Texture2D(
            potW, potH, format=GL_RGBA,
            data=(GL_RGBA, GL_UNSIGNED_BYTE, None))
        self._cairoSurface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        self._cairoContext = cairo.Context(self._cairoSurface)
        self._pangoContext = Pango.PangoCairoContext(self._cairoContext)
        self.updateRenderingContext()

    def frameUnsynced(self, deltaT):
        window = self._screens[0][0]
        window.switchTo()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        wx, wy, ww, wh = self._primaryWidget.AbsoluteRect.XYWH

        for sceneWidget in window._sceneWidgets:
            glViewport(*sceneWidget.AbsoluteRect.XYWH)
            sceneWidget.update(deltaT)
            sceneWidget.renderScene()

        glViewport(0, 0, ww, wh)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(wx, ww, wh, wy, -1., 1.)
        glMatrixMode(GL_MODELVIEW)
        ctx = self._cairoContext
        self.clearCairoSurface()

        self.render()

        self.cairoTex.bind()
        s, t = self.cairoTexCoords
        CGL.glTexCairoSurfaceSubImage2D(GL_TEXTURE_2D, 0, 0, 0, self._cairoSurface)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(0, 0)
        glTexCoord2f(0, t)
        glVertex2f(0, wh)
        glTexCoord2f(s, t)
        glVertex2f(ww, wh)
        glTexCoord2f(s, 0)
        glVertex2f(ww, 0)
        glEnd()
        Texture2D.unbind()

        window.flip()
