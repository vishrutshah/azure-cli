# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------
# pylint: skip-file
from .rule_data_source import RuleDataSource


class RuleManagementEventDataSource(RuleDataSource):
    """A rule management event data source. The discriminator fields is always
    RuleManagementEventDataSource in this case.

    :param odatatype: Polymorphic Discriminator
    :type odatatype: str
    :param event_name: the event name.
    :type event_name: str
    :param event_source: the event source.
    :type event_source: str
    :param level: the level.
    :type level: str
    :param operation_name: The name of the operation that should be checked
     for. If no name is provided, any operation will match.
    :type operation_name: str
    :param resource_group_name: the resource group name.
    :type resource_group_name: str
    :param resource_provider_name: the resource provider name.
    :type resource_provider_name: str
    :param resource_uri: the resource uri.
    :type resource_uri: str
    :param status: The status of the operation that should be checked for. If
     no status is provided, any status will match.
    :type status: str
    :param sub_status: the substatus.
    :type sub_status: str
    :param claims: the claims.
    :type claims: :class:`RuleManagementEventClaimsDataSource
     <azure.mgmt.monitor.models.RuleManagementEventClaimsDataSource>`
    """

    _validation = {
        'odatatype': {'required': True},
    }

    _attribute_map = {
        'odatatype': {'key': 'odata\\.type', 'type': 'str'},
        'event_name': {'key': 'eventName', 'type': 'str'},
        'event_source': {'key': 'eventSource', 'type': 'str'},
        'level': {'key': 'level', 'type': 'str'},
        'operation_name': {'key': 'operationName', 'type': 'str'},
        'resource_group_name': {'key': 'resourceGroupName', 'type': 'str'},
        'resource_provider_name': {'key': 'resourceProviderName', 'type': 'str'},
        'resource_uri': {'key': 'resourceUri', 'type': 'str'},
        'status': {'key': 'status', 'type': 'str'},
        'sub_status': {'key': 'subStatus', 'type': 'str'},
        'claims': {'key': 'claims', 'type': 'RuleManagementEventClaimsDataSource'},
    }

    def __init__(self, event_name=None, event_source=None, level=None, operation_name=None, resource_group_name=None, resource_provider_name=None, resource_uri=None, status=None, sub_status=None, claims=None):
        super(RuleManagementEventDataSource, self).__init__()
        self.event_name = event_name
        self.event_source = event_source
        self.level = level
        self.operation_name = operation_name
        self.resource_group_name = resource_group_name
        self.resource_provider_name = resource_provider_name
        self.resource_uri = resource_uri
        self.status = status
        self.sub_status = sub_status
        self.claims = claims
        self.odatatype = 'Microsoft.Azure.Management.Insights.Models.RuleManagementEventDataSource'
