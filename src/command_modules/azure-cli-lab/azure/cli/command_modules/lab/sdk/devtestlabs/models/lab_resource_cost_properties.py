# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# coding: utf-8
# pylint: skip-file
from msrest.serialization import Model


class LabResourceCostProperties(Model):
    """The properties of a resource cost item.

    :param resourcename: The name of the resource.
    :type resourcename: str
    :param resource_uid: The unique identifier of the resource.
    :type resource_uid: str
    :param resource_cost: The cost component of the resource cost item.
    :type resource_cost: float
    :param resource_type: The logical resource type (ex. virtualmachine,
     storageaccount)
    :type resource_type: str
    :param resource_owner: The owner of the resource (ex.
     janedoe@microsoft.com)
    :type resource_owner: str
    :param resource_pricing_tier: The category of the resource (ex.
     Premium_LRS, Standard_DS1)
    :type resource_pricing_tier: str
    :param resource_status: The status of the resource (ex. Active)
    :type resource_status: str
    :param resource_id: The ID of the resource
    :type resource_id: str
    :param external_resource_id: The ID of the external resource
    :type external_resource_id: str
    """

    _attribute_map = {
        'resourcename': {'key': 'resourcename', 'type': 'str'},
        'resource_uid': {'key': 'resourceUId', 'type': 'str'},
        'resource_cost': {'key': 'resourceCost', 'type': 'float'},
        'resource_type': {'key': 'resourceType', 'type': 'str'},
        'resource_owner': {'key': 'resourceOwner', 'type': 'str'},
        'resource_pricing_tier': {'key': 'resourcePricingTier', 'type': 'str'},
        'resource_status': {'key': 'resourceStatus', 'type': 'str'},
        'resource_id': {'key': 'resourceId', 'type': 'str'},
        'external_resource_id': {'key': 'externalResourceId', 'type': 'str'},
    }

    def __init__(self, resourcename=None, resource_uid=None, resource_cost=None, resource_type=None, resource_owner=None, resource_pricing_tier=None, resource_status=None, resource_id=None, external_resource_id=None):
        self.resourcename = resourcename
        self.resource_uid = resource_uid
        self.resource_cost = resource_cost
        self.resource_type = resource_type
        self.resource_owner = resource_owner
        self.resource_pricing_tier = resource_pricing_tier
        self.resource_status = resource_status
        self.resource_id = resource_id
        self.external_resource_id = external_resource_id
