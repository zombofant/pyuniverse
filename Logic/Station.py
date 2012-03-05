# File name: Station.py
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

from Object import TradableObject, OwnableObject, PositionableObject
from Cargo import QuotaCargo, Sizes

class Station(TradableObject, OwnableObject, PositionableObject):
    def __init__(self, **kwargs):
        super(Station, self).__init__(**kwargs)
        self.Products = dict()
        self.Resources = dict()
        self.SecondaryResources = dict()
        self.DockWares = set()
        # initialize with zero cargo capacity
        self.Cargo = QuotaCargo(Sizes.SizeST, 0)
        self._productQuota = self.Cargo.addQuota(0, True)
        self._resourceQuota = self.Cargo.addQuota(0, True)
        self._secondaryResourceQuota = self.Cargo.addQuota(0, False)
        self._dockWareQuota = self.Cargo.addQuota(0, True)
        self._cycleDuration = None

    def _checkTradable(self, tradable):
        if (    tradable in self.Products or
                tradable in self.Resources or
                tradable in self.SecondaryResources or
                tradable in self.DockWares):
            raise ValueError("Tradable {0} already defined as product, resource or dock ware in {1}".format(tradable, self)

    def addProduct(self, product, perCycle):
        self._checkTradable(product)
        self.Products[product] = perCycle
        self.Cargo.addTradableToQuota(self._productQuota, product)

    def addResource(self, resource, perCycle):
        self._checkTradable(product)
        self.Resources[resource] = perCycle
        self.Cargo.addTradableToQuota(self._resourceQuota, resource)

    def addSecondaryResource(self, resource, perCycle):
        self._checkTradable(resource)
        self.SecondaryResources[resource] = perCycle
        self.Cargo.addTradableToQuota(self._secondaryResourceQuota, resource)

    def addDockWare(self, ware, perCycle):
        self._checkTradable(ware)
        self.DockWare[ware] = perCycle
        self.Cargo.addTradableToQuota(self._dockWareQuota, ware)

    @property
    def ProductQuota(self):
        return self._productQuota.Capacity

    @ProductQuota.setter
    def ProductQuota(self, value):
        self._productQuota.Capacity = value

    @property
    def CycleDuration(self):
        return self._cycleDuration

    @CycleDuration.setter
    def CycleDuration(self, value):
        duration = float(value)
        if duration == 0:
            raise ValueError("CycleDuration must be greater than zero. Got {0}.".format(duration))
        self._cycleDuration = value
