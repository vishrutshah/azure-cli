# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from ._util import ParametersContext


with ParametersContext(command='lab vm create') as c:
    authentication_group_name = 'Authentication'
    c.argument('admin_username', arg_group=authentication_group_name)
    c.argument('admin_password', arg_group=authentication_group_name)
    c.argument('authentication_type', arg_group=authentication_group_name)
    c.argument('ssh_key', arg_group=authentication_group_name)
    gallery_image_group_name = 'Gallery Image'
    c.argument('offer', arg_group=gallery_image_group_name)
    c.argument('publisher', arg_group=gallery_image_group_name)
    c.argument('os_type', arg_group=gallery_image_group_name)
    c.argument('sku', arg_group=gallery_image_group_name)
    c.argument('version', arg_group=gallery_image_group_name)
    custom_image_group_name = 'Custom Image'
    c.argument('custom_image_id', arg_group=custom_image_group_name)
    network_group_name = 'Network'
    c.argument('lab_subnet_name', arg_group=network_group_name)
    c.argument('lab_virtual_network_id', arg_group=network_group_name)
    c.argument('disallow_public_ip_address', arg_group=network_group_name)
    artifacts_group_name = 'Artifacts'
    c.argument('artifact_id', arg_group=artifacts_group_name)
    c.argument('artifact_names', arg_group=artifacts_group_name)
    c.argument('artifact_values', arg_group=artifacts_group_name)


with ParametersContext(command='lab vm apply-artifacts') as c:
    from azure.mgmt.devtestlabs.models.artifact_install_properties import \
         ArtifactInstallProperties
    from azure.mgmt.devtestlabs.models.artifact_parameter_properties import \
         ArtifactParameterProperties

    c.expand('artifacts', ArtifactInstallProperties)
    c.expand('parameters', ArtifactParameterProperties)
