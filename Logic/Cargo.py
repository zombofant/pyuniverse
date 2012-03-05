# File name: Cargo.py
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

import itertools

from Errors import *
from Object import TradableObject

class AbstractCargo(object):
    def __init__(self, maxSizeMagnitude, capacity, **kwargs):
        super(AbstractCargo, self).__init__(**kwargs)
        self._maxSizeMagnitude = int(maxSizeMagnitude)
        self._capacity = int(capacity)
        self._usedCapacity = 0

    def __setitem__(self, tradable, amount):
        amount = int(amount)
        if amount < 0:
            raise ValueError("Cannot have negative ware amounts.")
        existing = self[tradable]
        if amount > existing:
            self.add(tradable, amount - existing)
        else:
            self.remove(tradable, existing - amount)

    def __delitem__(self, tradable, amount):
        self.remove(tradable, self[tradable])

    def _checkCapacity(self, more):
        if self._usedCapacity + more > self._capacity:
            raise CapacityError(more, self)

    @property
    def Capacity(self):
        return self._capacity

    @Capacity.setter
    def Capacity(self, value):
        if value >= self._usedCapacity:
            self._capacity = int(value)
        else:
            raise ContainerError("Cannot resize a container to a size smaller than the currently used storage.")

    @property
    def MaxSizeMagnitude(self):
        return self._maxSizeMagnitude

    @MaxSizeMagnitude.setter
    def MaxSizeMagnitude(self, value):
        if len(self._contents) > 0:
            raise ContainerError("Cannot resize container with stuff in it.")
        self._maxSizeMagnitude = int(value)

    @property
    def UsedCapacity(self):
        return self._usedCapacity


class Cargo(AbstractCargo):
    def __init__(self, maxSizeMagnitude, capacity, **kwargs):
        super(Cargo, self).__init__(maxSizeMagnitude, capacity, **kwargs)
        self._contents = {}

    def _forceAdd(self, tradable, amount, total):
        self._contents[tradable] = self._contents.setdefault(tradable, 0) + amount
        self._usedCapacity += total

    def add(self, tradable, amount):
        """
        Attempts the given *amount* of *tradable* to the cargo. 

        *tradable* must be hashable for this to work. See the Freeze
        module to see how to produce hashable instances of some objects.

        The check for overflow is done with *_checkCapacity*, which by
        default raises a CapacityError if there is not enough space
        for the given *amount* of *tradable*.
        """
        
        magnitude = tradable.SizeMagnitude
        if magnitude > self._maxSizeMagnitude:
            raise MagnitudeError(magnitude, self)
        total = tradable.Size * amount
        self._checkCapacity(total)
        self._forceAdd(tradable, amount, total)

    def __iter__(self):
        return self._contents.iteritems()

    def remove(self, tradable, amount):
        if not tradable in self:
            return False
        existing = self._contents[tradable]
        if existing < amount:
            amount = existing
            del self._contents[tradable]
        else:
            self._contents[tradable] = existing - amount
        self._usedCapacity -= tradable.Size * amount
        return amount

    def __contains__(self, tradable):
        return tradable in self._contents

    def __getitem__(self, tradable):
        return self._contents.get(tradable, 0)


class QuotaStack(Cargo):
    def __init__(self, quotaCargo, maxSizeMagnitude, limits, **kwargs):
        capacity, self._allowOverflow = limits
        super(QuotaStack, self).__init__(maxSizeMagnitude, capacity, **kwargs)
        self._cargo = quotaCargo

    def add(self, tradable, amount):
        total = tradable.Size * amount
        # we use 1 here for the capacity check if overflowing is allowed
        # as we do not want to allow a full stack to become overfull
        # (only non-full stacks may become overfull)
        self._checkCapacity(1 if self._allowOverflow else total)
        self._forceAdd(tradable, amount, total)

    def _checkCapacity(self, more):
        if self._usedCapacity + more > self._capacity:
            raise QuotaCapacityError(more, self, self._cargo)


class QuotaCargo(AbstractCargo):
    def __init__(self, maxSizeMagnitude, capacity, quotaGroupDict, groupLimits, **kwargs):
        super(QuotaCargo, self).__init__(maxSizeMagnitude, capacity)
        self._contents = dict()
        self._quotaDict = dict()
        for tradable, group in quotaGroupDict.iteritems():
            quotaCargo = self._contents.setdefault(group, QuotaStack(self, maxSizeMagnitude, groupLimits[group]))
            self._quotaDict[tradable] = quotaCargo

    def _getQuotaStack(self, tradable):
        quotaDict = self._quotaDict
        cargo = quotaDict.get(tradable, None)
        if cargo is None:
            cargo = quotaDict.get(None, None)
        return cargo

    def add(self, tradable, amount):
        """
        Adds the given *amount* of *tradable* to this container.
        """
        magnitude = tradable.SizeMagnitude
        if magnitude > self._maxSizeMagnitude:
            raise MagnitudeError(magnitude, self)
        
        cargo = self._getQuotaStack(tradable)
        if cargo is None:
            raise TradableNotAllowedError(tradable, self)

        total = amount * tradable.Size
        self._checkCapacity(total)
        cargo.add(tradable, amount)

        self._usedCapacity += tradable.Size * amount

    def remove(self, tradable, amount):
        cargo = self._getQuotaStack(tradable)
        if cargo is None:
            return

        status = cargo.remove(tradable, amount)
        if status:
            self._usedCapacity -= status * tradable.Size

    def __getitem__(self, tradable):
        cargo = self._getQuotaStack(tradable)
        return 0 if cargo is None else cargo[tradable]
    
