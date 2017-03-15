# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from azure.cli.command_modules.lab.validators import \
    (validate_authentication_type, validate_image_argument,
     validate_network_parameters, default_location, validate_ssh_key)

from ._util import ParametersContext


with ParametersContext(command='lab vm create') as c:
    c.argument('image', validator=validate_image_argument, required=True)
    c.argument('size', required=True)
    c.register_alias('resource_group', ('--resource-group', '-g'))

    authentication_group_name = 'Authentication'
    c.argument('admin_username', arg_group=authentication_group_name)
    c.argument('admin_password', arg_group=authentication_group_name)
    c.argument('authentication_type', arg_group=authentication_group_name, validator=validate_authentication_type)
    c.argument('ssh_key', arg_group=authentication_group_name)
    c.ignore('is_authentication_with_ssh_key')
    c.ignore('user_name')
    c.ignore('password')

    # Add Artifacts from json object
    c.register('artifacts', ('--artifacts',), type=json.loads)

    network_group_name = 'Network'
    c.argument('disallow_public_ip_address', arg_group=network_group_name)
    c.argument('subnet', arg_group=network_group_name)
    c.argument('vnet_name', arg_group=network_group_name, validator=validate_network_parameters)
    c.ignore('lab_subnet_name')
    c.ignore('lab_virtual_network_id')

    # Ignore Gallery Image arguments
    c.ignore('gallery_image_reference')
    c.ignore('os_offer')
    c.ignore('os_publisher')
    c.ignore('os_type')
    c.ignore('os_sku')
    c.ignore('os_version')

    # Ignore Custom Image ID argument'
    c.ignore('custom_image_id')

    c.register('location', ('--location', '-l'), validator=default_location,
               help='Location in which to create VM. Defaults to the location of the lab')


with ParametersContext(command='lab vm apply-artifacts') as c:
    from azure.mgmt.devtestlabs.models.artifact_install_properties import \
         ArtifactInstallProperties
    from azure.mgmt.devtestlabs.models.artifact_parameter_properties import \
         ArtifactParameterProperties

    c.expand('artifacts', ArtifactInstallProperties)
    c.expand('parameters', ArtifactParameterProperties)
