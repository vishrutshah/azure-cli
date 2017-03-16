# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import getpass


# pylint: disable=too-many-locals, unused-argument, too-many-statements
def create_lab_vm(client, resource_group, lab_name, name, notes=None, image=None, size=None,
                  admin_username=getpass.getuser(), admin_password=None,
                  ssh_key=None, authentication_type='password',
                  vnet_name=None, subnet=None, disallow_public_ip_address=None, artifacts=None,
                  location=None, tags=None, custom_image_id=None, lab_virtual_network_id=None,
                  os_publisher=None, os_offer=None, os_sku=None, os_version=None, os_type=None,
                  gallery_image_reference=None, generate_ssh_keys=None, allow_claim=True,
                  storage_type='Standard', expiration_date=None):
    """ Command to create vm of in the Azure DevTest Lab """
    from .sdk.devtestlabs.models.lab_virtual_machine_creation_parameter import LabVirtualMachineCreationParameter

    is_ssh_authentication = authentication_type == 'ssh'

    lab_virtual_machine = LabVirtualMachineCreationParameter(notes=notes,
                                                             custom_image_id=custom_image_id,
                                                             size=size,
                                                             user_name=admin_username,
                                                             password=admin_password,
                                                             ssh_key=ssh_key,
                                                             is_authentication_with_ssh_key=is_ssh_authentication,
                                                             lab_subnet_name=subnet,
                                                             lab_virtual_network_id=lab_virtual_network_id,
                                                             disallow_public_ip_address=disallow_public_ip_address,
                                                             artifacts=artifacts,
                                                             gallery_image_reference=gallery_image_reference,
                                                             name=name,
                                                             location=location,
                                                             tags=tags,
                                                             allow_claim=True,
                                                             storage_type=storage_type,
                                                             expiration_date=expiration_date)

    return client.create_environment(resource_group, lab_name, lab_virtual_machine)


def list_vm(client, resource_group, lab_name, order_by=None, top=None,
            filters=None, my_vms=None, claimable=None, expand=None, object_id=None):
    """ Command to list vms by resource group in the Azure DevTest Lab """

    return client.list(resource_group, lab_name, expand=expand, filter=filters, top=top, order_by=order_by)