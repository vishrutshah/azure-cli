# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator 0.17.0.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ScaleCapacity(Model):
    """The number of instances that can be used during this profile.

    :param minimum: the minimum number of instances for the resource.
    :type minimum: str
    :param maximum: the maximum number of instances for the resource. The
     actual maximum number of instances is limited by the cores that are
     available in the subscription.
    :type maximum: str
    :param default: the number of instances that will be set if metrics are
     not available for evaluation. The default is only used if the current
     instance count is lower than the default.
    :type default: str
    """ 

    _validation = {
        'minimum': {'required': True},
        'maximum': {'required': True},
        'default': {'required': True},
    }

    _attribute_map = {
        'minimum': {'key': 'minimum', 'type': 'str'},
        'maximum': {'key': 'maximum', 'type': 'str'},
        'default': {'key': 'default', 'type': 'str'},
    }

    def __init__(self, minimum, maximum, default):
        self.minimum = minimum
        self.maximum = maximum
        self.default = default
