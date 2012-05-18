/**********************************************************************
File name: BoundingSphere.cpp
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
#include "BoundingSphere.hpp"

#include <cassert>

namespace PyUni {
namespace SceneGraph {

BoundingSphere::BoundingSphere()
    : _radius(1.0f), _center(Vector3(0.,0.,0.))
{
}

BoundingSphere::~BoundingSphere()
{
}

void BoundingSphere::computeFromVertices(int n, int elmSize, const char *data)
{
    // center (average)
    double sum[3] = { 0., 0., 0. };
    for(int i = 0; i < n; ++i)
    {
        const float *elements = (const float*)(data + i*elmSize);
        sum[0] += elements[0];
        sum[1] += elements[1];
        sum[2] += elements[2];
    }
    double rpN = 1. / (double)n;
    _center.x = sum[0] * rpN;
    _center.y = sum[1] * rpN;
    _center.z = sum[2] * rpN;

    // radius is largest distance from center
    _radius = 0.;
    for(int i = 0; i < n; ++i)
    {
        const double *elements = (const double*)(data + i*elmSize);
        double d[3] = {
            elements[0] - _center.x,
            elements[1] - _center.y,
            elements[2] - _center.z
        };
        double r = d[0]*d[0] + d[1]*d[1] + d[2]*d[2];
        if(r > _radius)
        {
            _radius = r;
        }
    }
    _radius = sqrt(_radius);
}

void BoundingSphere::transform(Matrix4 transformation, BoundingVolume *target)
{
    //target->_center = transformation * _center;
    //target->_radius = transformation.norm() * _radius;
}

/*int onSideOfPlane(const Plane3 plane) const
{
}*/

bool BoundingSphere::intersects(const Vector3 origin, const Vector3 direction) const
{
    return false;
}

bool BoundingSphere::intersects(const BoundingVolume *other) const
{
    return false;
}

void BoundingSphere::copyFrom(const BoundingVolume *other)
{
    BoundingSphere *sphere = (BoundingSphere*)other;
    _radius = sphere->_radius;
    _center = sphere->_center;
}

void BoundingSphere::growToContain(const BoundingVolume *other)
{
}

}
}
