# File name: Texture.py
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
from Base import *
from Renderbuffer import RenderbufferBase

class TextureBase(GLObject):
    def __init__(self, format=None, **kwargs):
        assert format is not None
        super(TextureBase, self).__init__(**kwargs)
        self.format = format
        self.id = glGenTextures(1)
        
    def __del__(self):
        glDeleteTextures(self.id)
        super(TextureBase, self).__del__()
        
    def bind(self):
        glBindTexture(self._textureClass, self.id)
        
    def __setitem__(self, key, value):
        if type(value) == int:
            glTexParameteri(self._textureClass, key, value)
        else:
            glTexParameterf(self._textureClass, key, value)
        
    @classmethod
    def unbind(self):
        glBindTexture(self._textureClass, 0)
        
class Texture1D(TextureBase):
    _textureClass = GL_TEXTURE_1D
    
    def __init__(self, width=None, format=None, **kwargs):
        super(Texture1D, self).__init__(format=format, **kwargs)
        self._dimensions = (width, )
        self.bind()
        glTexImage1D(GL_TEXTURE_1D, 0, format, self._dimensions[0], 0, GL_LUMINANCE, GL_UNSIGNED_BYTE, 0)
        self[GL_TEXTURE_MAG_FILTER] = GL_NEAREST
        self[GL_TEXTURE_MIN_FILTER] = GL_NEAREST
        self[GL_TEXTURE_WRAP_S] = GL_CLAMP_TO_EDGE
        Texture1D.unbind()
    
    @property
    def Dimensions(self):
        return self._dimensions

class Texture2D(TextureBase, RenderbufferBase):
    _textureClass = GL_TEXTURE_2D
    
    def __init__(self, width=None, height=None, format=None, **kwargs):
        super(Texture2D, self).__init__(width=width, height=height, format=format, **kwargs)
        self.bind()
        glTexImage2D(GL_TEXTURE_2D, 0, format, self._dimensions[0], self._dimensions[1], 0, GL_LUMINANCE, GL_UNSIGNED_BYTE, 0)
        self[GL_TEXTURE_MAG_FILTER] = GL_NEAREST
        self[GL_TEXTURE_MIN_FILTER] = GL_NEAREST
        self[GL_TEXTURE_WRAP_S] = GL_CLAMP_TO_EDGE
        self[GL_TEXTURE_WRAP_T] = GL_CLAMP_TO_EDGE
        Texture2D.unbind()
        
    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.id)
        
    def attach(self, target):
        glFramebufferTexture2D(GL_FRAMEBUFFER, target, GL_TEXTURE_2D, self.id, 0)
        
    def _getValid(self):
        return True

