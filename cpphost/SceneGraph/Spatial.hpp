/**********************************************************************
File name: Spatial.hpp
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
#ifndef _PYUNI_SCENEGRAPH_SPATIAL_H
#define _PYUNI_SCENEGRAPH_SPATIAL_H

#include <boost/shared_ptr.hpp>
#include <boost/weak_ptr.hpp>

#include "Math/Matrices.hpp"
#include "BoundingVolume.hpp"

namespace PyUni {
namespace SceneGraph {

class Spatial;

typedef boost::shared_ptr<Spatial> SpatialHandle;
typedef boost::weak_ptr<Spatial> WeakSpatialHandle;

class Spatial
{
    public:
        virtual ~Spatial();

        Matrix4 localTransformation;
        Matrix4 worldTransformation;
        BoundingVolume *worldBound;
        bool worldNeedsUpdate;

        void updateGeometryState(bool initiator=true);
        void updateBoundState();

        SpatialHandle getParent();
        void setParent(SpatialHandle p);

        const std::string getObjectName() { return _objectName; }
        void setObjectName(const std::string name) { _objectName = name; }

        virtual void translate(double x, double y, double z);
        virtual void setTranslation(double x, double y, double z);
        virtual void rotate(double angle, double x, double y, double z);
        virtual void setRotation(double angle, double x, double y, double z);
        virtual void scale(double x, double y, double z);
        virtual void setScale(double x, double y, double z);

        virtual void resetTransformation();
        virtual void applyTransformation();

        virtual void draw() = 0;

    protected:
        Spatial();
        virtual void updateWorldData();
        virtual void updateWorldBound() = 0;
        void advertiseBoundUpwards();

        WeakSpatialHandle _parent;
        WeakSpatialHandle _weak;
        std::string _objectName;
};

}
}
#endif

