# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ._client_factory import (get_devtestlabs_virtual_machine_operation)
from ._util import (ServiceGroup, create_service_adapter)


# MANAGEMENT COMMANDS
virtual_machine_operations = create_service_adapter(
    'azure.mgmt.devtestlabs.operations.virtual_machine_operations',
    'VirtualMachineOperations')

with ServiceGroup(__name__, get_devtestlabs_virtual_machine_operation,
                  virtual_machine_operations) as s:
    with s.group('devtestlabs virtual-machine') as c:
        c.command('show', 'get_resource')
        c.command('list', 'list')
