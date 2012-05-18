/**********************************************************************
File name: BoundingVolume.hpp
This file is part of: Pythonic Universe

LICENSE

The contents of this file are subject to the Mozilla Public License
Version 1.1 (the "License"); you may not use this file except in
compliance with the License. You may obtain a copy of the License at
http://www.mozilla.org/MPL/

Software distributed under the License is distributed on an "AS IS"
basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
License for the specific language governing rights and limitations under
the License.

Alternatively, the contents of this file may be used under the terms of
the GNU General Public license (the  "GPL License"), in which case  the
provisions of GPL License are applicable instead of those above.

FEEDBACK & QUESTIONS

For feedback and questions about pyuni please e-mail one of the authors
named in the AUTHORS file.
**********************************************************************/
#ifndef _PYUNI_SCENEGRAPH_BOUNDINGVOLUME_H
#define _PYUNI_SCENEGRAPH_BOUNDINGVOLUME_H

#include <vector>

#include <boost/shared_ptr.hpp>

#include "Math/Matrices.hpp"

namespace PyUni {
namespace SceneGraph {

class BoundingVolume
{
    protected:
        BoundingVolume();

    public:
        ~BoundingVolume();

        virtual void computeFromVertices(int n, int elmSize, const char *data) = 0;
        virtual void transform(Matrix4 transformation, BoundingVolume *target) = 0;
        //virtual int onSideOfPlane(const Plane3 plane) const = 0;
        virtual bool intersects(const Vector3 origin, const Vector3 direction) const = 0;
        virtual bool intersects(const BoundingVolume *other) const = 0;
        virtual void copyFrom(const BoundingVolume *other) = 0;
        virtual void growToContain(const BoundingVolume *other) = 0;
};

}
}

#endif

