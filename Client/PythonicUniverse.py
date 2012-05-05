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

import CUni
import CUni.GL as CGL
import CUni.SceneGraph as CSceneGraph
import CUni.Window.key as key
import CUni.Pango as Pango

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
from Engine.GL.SceneGraph.Core import SceneGraph, Node
from Engine.UI.Theme import Theme
import Engine.GL.Base as GL
from Engine.UI.CSS.Rect import Rect

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

        #scene = Scene(mainScreen)
        #self.addSceneWidget(scene)

        for x in xrange(20):
            for y in xrange(20):
                window = WindowWidget(self._windowLayer)
                window.Title.Text = "Test"
                window.AbsoluteRect.XYWH = (x * 32, y * 32, 32, 32)

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

        #self._shaders.append(self._shader.bind(texturing=False))
        shader = self._shader.bind(texturing=True)
        glUniform1i(shader["texture"], 0)

        Shader.unbind()

        w, h = mainScreen.AbsoluteRect.Width, mainScreen.AbsoluteRect.Height
        potW, potH = makePOT(w), makePOT(h)

        self.cairoTexCoords = (w / potW, h / potH)
        
        self.cairoTex = Texture2D(
            potW, potH, format=GL_RGBA,
            data=(GL_RGBA, GL_UNSIGNED_BYTE, None))
        
        self.cairoSurf = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            w,
            h
        )
        self._cairoContext = cairo.Context(self.cairoSurf)
        self._pangoContext = Pango.PangoCairoContext(self._cairoContext)
            
        self.updateRenderingContext()
        
        # sys.exit(1)

    def clearCairoSurface(self):
        ctx = self._cairoContext
        ctx.set_source_rgba(0., 0., 0., 0.)
        ctx.set_operator(cairo.OPERATOR_SOURCE)
        ctx.paint()
        ctx.set_operator(cairo.OPERATOR_OVER)

    def onKeyDown(self, symbol, modifiers):
        if symbol == key.Escape:
            print("bye!")
            self._eventLoop.terminate()

    def cairoTesting(self):
        r = Rect()
        r.XYWH = (32, 32, 128, 24)

        pi = math.pi
        # topleft topright bottomleft bottomright
        radius = (2, 4, 8, 16)
        hasRadius = radius[0] > 0 or radius[1] > 0 or radius[2] > 0 or radius[3] > 0
        shearLeft, shearRight = 0, 0
        hasShear = shearLeft or shearRight
        top, left, right, bottom = r.Top, r.Left, r.Right, r.Bottom
        cr = self._cairoContext

        if not hasShear:
            if hasRadius:
                currRadius = radius[0]
                cr.arc(left + currRadius, top + currRadius, currRadius, 2*(pi/2), 3*(pi/2))
                currRadius = radius[1]
                cr.arc(right - currRadius, top + currRadius, currRadius, 3*(pi/2), 4*(pi/2))
                currRadius = radius[2]
                cr.arc(right - currRadius, bottom - currRadius, currRadius, 0*(pi/2), 1*(pi/2))  # ;o)
                currRadius = radius[3]
                cr.arc(left + currRadius, bottom - currRadius, currRadius, 1*(pi/2), 2*(pi/2))
                cr.close_path()
            else:
                cr.rectangle(top, left, r.Width, r.Height)
        else:
            if hasRadius:
                if shearLeft > 0:
                    x0y0 = (left + shearLeft + radius[0], top + radius[0])
                    x0y1 = (left + radius[2], bottom - radius[2])
                else:
                    x0y0 = (left + radius[0], top + radius[0])
                    x0y1 = (left + radius[2] - shearLeft, bottom - radius[2])
                if shearRight > 0:
                    x1y0 = (right - radius[1], top + radius[1])
                    x1y1 = (right - (shearRight + radius[3]), bottom - radius[3])
                else:
                    x1y0 = (right + shearRight - radius[1], top + radius[1])
                    x1y1 = (right - radius[3], bottom - radius[3])
                leftLessAngle = math.atan(shearLeft/r.Height)
                rightLessAngle = math.atan(shearRight/r.Height)
                cr.arc(x0y0[0], x0y0[1], radius[0], 2*(pi/2) + leftLessAngle, 3*(pi/2))
                cr.arc(x1y0[0], x1y0[1], radius[1], 3*(pi/2), 4*(pi/2) + rightLessAngle)
                cr.arc(x1y1[0], x1y1[1], radius[3], 0*(pi/2) + rightLessAngle, 1*(pi/2))  # ;o)
                cr.arc(x0y1[0], x0y1[1], radius[2], 1*(pi/2), 2*(pi/2) + leftLessAngle)
                cr.close_path()
            else:
                if shearLeft > 0:
                    x0y0 = (left + shearLeft, top)
                    x0y1 = (left, bottom)
                else:
                    x0y0 = (left, top)
                    x0y1 = (left - shearLeft, bottom)
                if shearRight > 0:
                    x1y0 = (right, top)
                    x1y1 = (right - shearRight, bottom)
                else:
                    x1y0 = (right + shearRight, top)
                    x1y1 = (right, bottom)
                cr.move_to(*x0y0)
                cr.line_to(*x1y0)
                cr.line_to(*x1y1)
                cr.line_to(*x0y1)
                cr.close_path()
                
            
        cr.set_line_width(1)
        cr.set_source_rgba(0.0, 0.5, 0.0, 1.0)
        cr.fill_preserve()
        cr.set_source_rgba(0.0, 1.0, 1.0, 1.0)
        cr.stroke()

        cr.set_line_width(1)
        cr.set_source_rgba(1., 0., 0., 1.)
        cr.rectangle(r.Left - 1.5, r.Top - 1.5, r.Width + 3, r.Height + 3)
        cr.stroke()

    def render(self):
        self._geometryBuffer.bind()
        self._shader.bind(texturing=True, upsideDown=False)
        super(PythonicUniverse, self).render()
        Shader.unbind()
        self._geometryBuffer.unbind()

    def frameUnsynced(self, deltaT):
        window = self._screens[0][0]
        window.switchTo()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        r = self._primaryWidget.AbsoluteRect.XYWH
        glOrtho(r[0], r[2], r[3], r[1], -1., 1.)
        glMatrixMode(GL_MODELVIEW)
        ctx = self._cairoContext
        self.clearCairoSurface()

        self.cairoTesting()

        self.cairoTex.bind()
        s, t = self.cairoTexCoords
        CGL.glTexCairoSurfaceSubImage2D(GL_TEXTURE_2D, 0, 0, 0, self.cairoSurf)
        glEnable(GL_TEXTURE_2D)
        glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(0, 0)
        glTexCoord2f(0, t)
        glVertex2f(0, r[3])
        glTexCoord2f(s, t)
        glVertex2f(r[2], r[3])
        glTexCoord2f(s, 0)
        glVertex2f(r[2], 0)
        glEnd()
        Texture2D.unbind()
        window.flip()
