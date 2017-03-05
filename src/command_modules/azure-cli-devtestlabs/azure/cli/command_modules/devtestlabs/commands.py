# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ._client_factory import (get_devtestlabs_virtual_machine_operation,
                              get_devtestlabs_custom_image_operation)
from ._util import (ServiceGroup, create_service_adapter)


# Virtual Machine Operations Commands
virtual_machine_operations = create_service_adapter(
    'azure.mgmt.devtestlabs.operations.virtual_machine_operations',
    'VirtualMachineOperations')

with ServiceGroup(__name__, get_devtestlabs_virtual_machine_operation,
                  virtual_machine_operations) as s:
    with s.group('devtestlabs vm') as c:
        c.command('show', 'get_resource')
        c.command('list', 'list')
        c.command('delete', 'delete_resource')
        c.command('start', 'start')
        c.command('stop', 'stop')

# Custom Image Operations Commands
custom_image_operations = create_service_adapter(
    'azure.mgmt.devtestlabs.operations.custom_image_operations',
    'CustomImageOperations')

with ServiceGroup(__name__, get_devtestlabs_custom_image_operation,
                  custom_image_operations) as s:
    with s.group('devtestlabs custom-image') as c:
        c.command('show', 'get_resource')
        c.command('list', 'list')
        c.command('delete', 'delete_resource')
