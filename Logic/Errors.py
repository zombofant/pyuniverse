# File name: Errors.py
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

__all__ = [
    "ContainerError", "MagnitudeError", "CapacityError",
    "QuotaError", "QuotaCapacityError", "TradableNotAllowedError"
]

class ContainerError(Exception):
    pass

class MagnitudeError(ContainerError):
    def __init__(self, got, cargoInstance):
        super(MagnitudeError, self).__init__(
            "Unsupported order of magnitude in {0}. Got {1}, maximum is {2}".format(
                cargoInstance,
                got,
                cargoInstance.MaxSizeMagnitude
            )
        )
        self._got = got

class CapacityError(ContainerError):
    def __init__(self, more, cargoInstance):
        super(CapacityError, self).__init__(
            "Capacity overflow in {0}. Got additional {1} units, capacity is {2}".format(
                cargoInstance,
                more,
                cargoInstance.Capacity
            )
        )
        self._more = more
        self._cargo = cargoInstance


class QuotaError(ContainerError):
    pass


class QuotaCapacityError(QuotaError):
    def __init__(self, more, quota, cargoInstance):
        super(QuotaCapacityError, self).__init__(
            "Capacity overflow in quota {3} in {0}. Got additional {1} units, capacity is {2}, quota limit is {4}".format(
                cargoInstance,
                more,
                cargoInstance.Capacity,
                quota,
                quota.Capacity
            )
        )
        self._more = more
        self._cargo = cargoInstance
        self._quota = quota

    @classmethod
    def fromCapacityError(cls, capacityErrorInstance, cargoInstance):
        return cls(capacityErrorInstance._more, capacityErrorInstance._cargo, cargoInstance)

class TradableNotAllowedError(QuotaError):
    def __init__(self, tradable, cargoInstance):
        super(TradableNotAllowedError, self).__init__(
            "Tradable not allowed in quota'd container {0}. Got {1}".format(
                cargoInstance,
                tradable
            )
        )
        self._tradable = tradable
        self._cargo = cargoInstance
