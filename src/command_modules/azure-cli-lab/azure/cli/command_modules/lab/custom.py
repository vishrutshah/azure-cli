# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import getpass
from ._client_factory import (get_devtestlabs_management_client)

def create_lab_vm(client, resource_group, lab_name, name, notes=None, image=None, size=None,
                  admin_username=getpass.getuser(), admin_password=None,
                  ssh_key=None, authentication_type='password',
                  vnet_name=None, subnet=None, disallow_public_ip_address=None, artifacts=None,
                  location=None, tags=None, custom_image_id=None,
                  is_authentication_with_ssh_key=False, lab_virtual_network_id=None,
                  os_publisher=None, os_offer=None, os_sku=None, os_version=None, os_type=None,
                  gallery_image_reference=None):
    '''
    :param resource_group: Name of the lab resource group
    :param lab_name: Name of lab
    :param name: Name of the virtual machine
    :param notes: Notes for the virtual machine
    :param image: The name of the operating system image (URN alias, URN, Custom Image ID or Gallery Image Name).
                  Use az lab gallery-image list for available Gallery Images or
                  Use az lab custom-image list for available Custom Images
    :param size: The VM size to be created
    :param admin_username: Username for the VM
    :param admin_password: Password for the VM.
    :param ssh_key: The SSH public key or public key file path
    :param authentication_type: Type of authentication to use with the VM. Allowed values:
                                    password, ssh
    :param subnet: The name of the subnet to reference an existing one in lab. If omitted, an appropriate lab's subnet
                   will be selected based on provided or defaulted --vnet-name
    :param vnet_name: Name of the virtual network to reference an existing one in lab. If omitted, an appropriate lab's
                      VNet and subnet will be selected automatically
    :param disallow_public_ip_address: Based on the selected or defaulted subnet this will be set to true or false
    :param artifacts: JSON encoded array of artifacts to be applied. Use @{file} to load from a file
    :param location: Location in which to create VM. Defaults to the location of the lab
    :param tags: Space separated tags in 'key[=value]' format. Use "" to clear existing tags
    :param custom_image_id:
    :param is_authentication_with_ssh_key:
    '''
    from azure.mgmt.devtestlabs.models.lab_virtual_machine import LabVirtualMachine

    # TODO:
    # [DONE] gallery_image_reference: can be verified with GalleryImage GET REST endpoint
    # [DONE] disallow_public_ip_address: conditional default based subnet config [Get on DTL VirtualNetwork ]
    # [DONE] location: Can be different from lab's location
    # [DONE] artifacts: How to get list of artifact_id with Dict or Dict from command line - load json
    # [DONE] authentication_type: Defaulted to password as portal does
    # return of create_environment does not return lab_vm object

    is_authentication_with_ssh_key = True if authentication_type == 'ssh' else False

    lab_virtual_machine = LabVirtualMachine(notes=notes,
                                            custom_image_id=custom_image_id,
                                            size=size,
                                            user_name=admin_username,
                                            password=admin_password,
                                            ssh_key=ssh_key,
                                            is_authentication_with_ssh_key=is_authentication_with_ssh_key,
                                            lab_subnet_name=subnet,
                                            lab_virtual_network_id=lab_virtual_network_id,
                                            disallow_public_ip_address=disallow_public_ip_address,
                                            artifacts=artifacts,
                                            gallery_image_reference=gallery_image_reference,
                                            name=name,
                                            location=location,
                                            tags=tags)
    # print(lab_virtual_machine)
    return client.create_environment(resource_group, lab_name, lab_virtual_machine)
