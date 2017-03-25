# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from azure.cli.command_modules.lab.validators import (validate_lab_vm_create,
                                                      validate_lab_vm_list)

from azure.cli.core.sdk.util import ParametersContext


with ParametersContext(command='lab vm create') as c:
    c.register_alias('resource_group', ('--resource-group', '-g'), validator=validate_lab_vm_create)
    c.register_alias('name', ('--name', '-n'))

    # Authentication related arguments
    authentication_group_name = 'Authentication'
    c.argument('admin_username', arg_group=authentication_group_name)
    c.argument('admin_password', arg_group=authentication_group_name)
    c.argument('authentication_type', arg_group=authentication_group_name)
    c.argument('ssh_key', arg_group=authentication_group_name)
    c.argument('generate_ssh_keys', action='store_true', arg_group=authentication_group_name)

    # Add Artifacts from json object
    c.argument('artifacts', type=json.loads)

    # Image related arguments
    c.ignore('gallery_image_reference')
    c.ignore('custom_image_id')
    c.argument('image')

    # Network related arguments
    network_group_name = 'Network'
    c.argument('disallow_public_ip_address', arg_group=network_group_name)
    c.argument('subnet', arg_group=network_group_name)
    c.argument('vnet_name', arg_group=network_group_name)
    c.ignore('lab_subnet_name')
    c.ignore('lab_virtual_network_id')

    c.register('location', ('--location', '-l'),
               help='Location in which to create VM. Defaults to the location of the lab')
    c.argument('expiration_date')
    c.argument('formula')
    c.argument('allow_claim', action='store_true')


with ParametersContext(command='lab vm list') as c:
    filter_arg_group_name = 'Filter'
    c.argument('filters', arg_group=filter_arg_group_name)
    c.argument('all', action='store_true', arg_group=filter_arg_group_name)
    c.argument('claimable', action='store_true', arg_group=filter_arg_group_name)
    c.register_alias('resource_group', ('--resource-group', '-g'), validator=validate_lab_vm_list)


with ParametersContext(command='lab vm apply-artifacts') as c:
    c.register('artifacts', ('--artifacts',), type=json.loads)
    c.register_alias('name', ('--name', '-n'))


with ParametersContext(command='lab formula') as c:
    c.register_alias('name', ('--name', '-n'))
