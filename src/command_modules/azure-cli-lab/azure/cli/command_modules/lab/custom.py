# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import getpass
from azure.cli.core._util import CLIError


def create_lab_vm(client, resource_group, lab_name, name, notes=None,
                  custom_image_id=None, size='Standard_DS1_v2',
                  admin_username=getpass.getuser(), admin_password=None,
                  ssh_key=None, authentication_type='password', lab_subnet_name=None,
                  lab_virtual_network_id=None, disallow_public_ip_address=True, artifact_id=None, artifact_names=[],
                  artifact_values=[],
                  offer=None, publisher=None, sku=None, os_type=None, version=None,
                  location=None, tags=None):
    '''
    :param resource_group: Name of resource group
    :param lab_name: Name of lab
    :param name: Name of the virtual machine
    :param notes: Notes for the virtual machine
    :param custom_image_id: Image ID of the custom image in the lab
    :param size: The VM size to be created
    :param admin_username: Username for the VM
    :param admin_password: Password for the VM if is_ssh_authentication is 'False'
    :param ssh_key: The SSH public key or public key file path
    :param authentication_type: Type of authentication to use with the VM. Defaults to password
                                for Windows and SSH public key for Linux.  Allowed values:
                                password, ssh
    :param lab_subnet_name: Name of the subnet
    :param lab_virtual_network_id: Fully qualified virtual network id of the lab. Ex. /subscriptions/{subscriptionID}/
                                   resourcegroups/{resourceGroup}/providers/microsoft.devtestlab/
                                   labs/{labName}/virtualnetworks/{VirtualNetworkName}
    :param disallow_public_ip_address: Whether to disallow public ip addresses
    :param artifact_id: The artifact’s identifier
    :param artifact_names: Space separated names of the artifact
    :param artifact_values: Space separated values of the artifact respective to artifact_names
    :param offer: The offer of the gallery image
    :param publisher: The publisher of the gallery image
    :param sku: The SKU of the gallery image
    :param os_type: The OS type of the gallery image
    :param version: The version of the gallery image
    :param location: Location in which to create VM.
    :param tags: Space separated tags in 'key[=value]' format. Use "" to clear existing tags
    '''
    from azure.mgmt.devtestlabs.models.lab_virtual_machine import LabVirtualMachine
    from azure.mgmt.devtestlabs.models.artifact_install_properties import ArtifactInstallProperties
    from azure.mgmt.devtestlabs.models.artifact_parameter_properties import ArtifactParameterProperties
    from azure.mgmt.devtestlabs.models.gallery_image_reference import GalleryImageReference

    # TODO:
    # custom_image_id: can be verified with CustomImage GET REST endpoint
    # gallery_image_reference: can be verified with GalleryImage GET REST endpoint
    # artifact_install_properties: each can be verified with Artifact GET REST endpoint
    # size: currently defaulted with Standard_DS1_v2 but lab admin can restrict possible values
    # disallow_public_ip_address: conditional default based subnet config [Get on DTL VirtualNetwork ]
    # location: Can be different from lab / resource group location
    # artifacts: How to get list of artifact_id with Dict or Dict from command line
    # authentication_type: Can be derived based OS from on CustomImage GET / GalleryImageReference GET
    # return of create_environment does not return lab_vm object

    # Verify either creating vm from custom image id or gallery image reference
    is_custom_image_provided = custom_image_id is not None
    gallery_image_required_parameters = [offer, publisher, sku, os_type, version]
    specified_parameters_number = [x for x in gallery_image_required_parameters if x]
    is_gallery_image_provided = len(specified_parameters_number) > 0

    if is_custom_image_provided and is_gallery_image_provided:
        raise CLIError("usage error: Provide custom image id or all Gallery Image Arguments.")
    if is_gallery_image_provided and len(specified_parameters_number) != 5:
        raise CLIError("usage error: Provide all Gallery Image Arguments.")
    if is_gallery_image_provided and not is_custom_image_provided:
        gallery_image_reference = GalleryImageReference(offer, publisher, sku, os_type, version)

    # Verify authentication type
    if authentication_type == 'password' and ssh_key:
        raise ValueError("incorrect usage for authentication-type 'password': "
                         "[--admin-username USERNAME] --admin-password PASSWORD")
    if authentication_type == 'password' and not admin_password:
        # prompt for admin password if not supplied
        from azure.cli.core.prompting import prompt_pass, NoTTYException
        try:
            admin_password = prompt_pass('Admin Password: ', confirm=True)
        except NoTTYException:
            raise CLIError('Please specify both username and password in non-interactive mode.')

    is_ssh_authentication = True if authentication_type == 'ssh' else False

    # Populate artifact properties to be applied
    artifact_install_properties = []

    if artifact_id:
        artifact_parameter_properties = []

        if len(artifact_names) == len(artifact_values):
            if len(artifact_names) != 0:
                artifact_parameter_property = ArtifactParameterProperties(artifact_names.pop(0), artifact_values.pop(0))
                artifact_parameter_properties.append(artifact_parameter_property)
        else:
            raise CLIError("{} and {} must be of same length".format(artifact_names, artifact_values))
        artifact_install_properties = ArtifactInstallProperties(artifact_id, artifact_parameter_properties)

    lab_virtual_machine = LabVirtualMachine(notes=notes,
                                            custom_image_id=custom_image_id,
                                            size=size,
                                            user_name=admin_username,
                                            password=admin_password,
                                            ssh_key=ssh_key,
                                            is_authentication_with_ssh_key=is_ssh_authentication,
                                            lab_subnet_name=lab_subnet_name,
                                            lab_virtual_network_id=lab_virtual_network_id,
                                            disallow_public_ip_address=disallow_public_ip_address,
                                            artifacts=artifact_install_properties,
                                            gallery_image_reference=gallery_image_reference,
                                            name=name,
                                            location=location,
                                            tags=tags)

    lab_vm = client.create_environment(resource_group, lab_name, lab_virtual_machine)
    return lab_vm
