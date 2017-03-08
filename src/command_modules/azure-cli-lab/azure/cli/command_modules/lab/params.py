# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from ._util import ParametersContext


with ParametersContext(command='lab vm create') as c:
    from azure.mgmt.devtestlabs.models.lab_virtual_machine import \
         LabVirtualMachine

    # c.expand('lab_virtual_machine', LabVirtualMachine)
    # c.register('gallery_image_reference', ('--gallery-image-reference',),
    #            type=json.loads,
    #            help='Microsoft Azure Marketplace image reference of the virtual.'
    #                 'JSON encoded gallery image reference. Use @{file} to load from a file.')
    c.register('lab_virtual_machine', ('--lab-virtual-machine',),
               type=json.loads,
               help='Microsoft Azure Marketplace image reference of the virtual.'
                    'JSON encoded gallery image reference. Use @{file} to load from a file.')

with ParametersContext(command='lab vm apply-artifacts') as c:
    from azure.mgmt.devtestlabs.models.artifact_install_properties import \
         ArtifactInstallProperties
    from azure.mgmt.devtestlabs.models.artifact_parameter_properties import \
         ArtifactParameterProperties

    c.expand('artifacts', ArtifactInstallProperties)
    c.expand('parameters', ArtifactParameterProperties)
