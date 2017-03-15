# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import re
import json

from six.moves.urllib.request import urlopen
from msrestazure.azure_exceptions import CloudError
from azure.cli.core._util import CLIError
from azure.cli.core.commands.arm import is_valid_resource_id
from ._client_factory import (get_devtestlabs_management_client)
from azure.mgmt.devtestlabs.models.gallery_image_reference import GalleryImageReference
import azure.cli.core.azlogging as azlogging

logger = azlogging.get_az_logger(__name__)


def get_complex_argument_processor(expanded_arguments, assigned_arg, model_type):
    """
    Return a validator which will aggregate multiple arguments to one complex argument.
    """
    def _expension_valiator_impl(namespace):
        """
        The validator create a argument of a given type from a specific set of arguments from CLI
        command.
        :param namespace: The argparse namespace represents the CLI arguments.
        :return: The argument of specific type.
        """
        ns = vars(namespace)
        kwargs = dict((k, ns[k]) for k in ns if k in set(expanded_arguments))

        setattr(namespace, assigned_arg, model_type(**kwargs))

    return _expension_valiator_impl


def default_location(namespace):
    if namespace.location is None:
        try:
            lab_operation = get_devtestlabs_management_client(None).lab
            lab = lab_operation.get_resource(namespace.resource_group, namespace.lab_name)
            namespace.location = lab.location
        except CloudError as err:
            raise CLIError(err)


def validate_authentication_type(namespace):
    # validate proper arguments supplied based on the authentication type
    if namespace.authentication_type == 'password':
        if namespace.ssh_key:
            raise ValueError(
                "incorrect usage for authentication-type 'password': "
                "[--admin-username USERNAME] --admin-password PASSWORD")

        if not namespace.admin_password:
            # prompt for admin password if not supplied
            from azure.cli.core.prompting import prompt_pass, NoTTYException
            try:
                namespace.admin_password = prompt_pass('Admin Password: ', confirm=True)
            except NoTTYException:
                raise CLIError('Please specify both username and password in non-interactive mode.')

    elif namespace.authentication_type == 'ssh':
        if namespace.admin_password:
            raise ValueError('Admin password cannot be used with SSH authentication type')

        validate_ssh_key(namespace)

        if not namespace.ssh_dest_key_path:
            namespace.ssh_dest_key_path = \
                '/home/{}/.ssh/authorized_keys'.format(namespace.admin_username)


def validate_network_parameters(namespace):
    from azure.cli.core.commands.client_factory import get_subscription_id
    vnet_operation = get_devtestlabs_management_client(None).virtual_network

    if not namespace.vnet_name:
        try:
            lab_vnets = list(vnet_operation.list(namespace.resource_group, namespace.lab_name, top=1))
            if not lab_vnets:
                err = "Unable to find any virtual network in the '{}' lab.".format(namespace.lab_name)
                raise CLIError(err)
            else:
                lab_vnet = lab_vnets[0]
                namespace.vnet_name = lab_vnet.name
                namespace.lab_virtual_network_id = lab_vnet.id
        except CloudError as err:
            raise CLIError(err)
    else:
        namespace.lab_virtual_network_id = '/subscriptions/{}/resourcegroups/{}/providers/microsoft.devtestlab' \
                                           '/labs/{}/virtualnetworks/{}'.format(get_subscription_id(),
                                                                                namespace.resource_group,
                                                                                namespace.lab_name,
                                                                                namespace.vnet_name)

    if not namespace.subnet:
        # Get the first subnet of the lab's virtual network
        lab_vnet = vnet_operation.get_resource(namespace.resource_group, namespace.lab_name, namespace.vnet_name)
        namespace.subnet = lab_vnet.subnet_overrides[0].lab_subnet_name

        # Determine value for disallow_public_ip_address based on subnet's use_public_ip_address_permission property
        if lab_vnet.subnet_overrides[0].use_public_ip_address_permission == 'Allow':
            namespace.disallow_public_ip_address = 'false'
        else:
            namespace.disallow_public_ip_address = 'true'


def validate_image_argument(namespace):
    image_type = _parse_image_argument(namespace)
    if image_type == 'urn' or image_type == 'gallery_image':
        namespace.gallery_image_reference = GalleryImageReference(offer=namespace.os_offer,
                                                                  publisher=namespace.os_publisher,
                                                                  os_type=namespace.os_type,
                                                                  sku=namespace.os_sku,
                                                                  version=namespace.os_version)
        namespace.notes = namespace.notes or namespace.image
    elif image_type == 'image_id':
        namespace.custom_image_id = namespace.image
    else:
        err = 'Invalid value for image "{}". Use a custom image id or pick one from lab gallery.'
        raise CLIError(err)


def _parse_image_argument(namespace):
    """ Systematically determines what type is supplied for the --image parameter. Updates the
        namespace and returns the type for subsequent processing. """

    # 1 - easy check for URI
    if namespace.image.lower().endswith('.vhd'):
        return 'uri'

    # 2 - attempt to match an URN alias (most likely)
    images = load_images_from_aliases_doc()
    matched = next((x for x in images if x['urnAlias'].lower() == namespace.image.lower()), None)
    if matched:
        namespace.os_publisher = matched['publisher']
        namespace.os_offer = matched['offer']
        namespace.os_sku = matched['sku']
        namespace.os_version = matched['version']
        return 'urn'

    # 3 - attempt to match an URN pattern
    urn_match = re.match('([^:]*):([^:]*):([^:]*):([^:]*)', namespace.image)
    if urn_match:
        namespace.os_publisher = urn_match.group(1)
        namespace.os_offer = urn_match.group(2)
        namespace.os_sku = urn_match.group(3)
        namespace.os_version = urn_match.group(4)
        return 'urn'

    # 4 - check if a fully-qualified ID (assumes it is an image ID)
    if is_valid_resource_id(namespace.image):
        print("Yes found it")
        return 'image_id'

    # 5 - check if an existing lab Gallery Image Reference
    try:
        gallery_image_operation = get_devtestlabs_management_client(None).gallery_image
        odata_filter = "name eq '{}'".format(namespace.image)
        lab_images = list(gallery_image_operation.list(namespace.resource_group, namespace.lab_name,
                                                       odata_filter, top=1))

        if not lab_images:
            err = "Unable to find '{}' image in the '{}' lab Gallery.".format(namespace.image, namespace.lab_name)
            raise CLIError(err)
        else:
            image = lab_images[0]
            namespace.os_offer = image.image_reference.offer
            namespace.os_publisher = image.image_reference.publisher
            namespace.os_sku = image.image_reference.sku
            namespace.os_type = image.image_reference.os_type
            namespace.os_version = image.image_reference.version
        return 'gallery_image'
    except CloudError:
        err = 'Invalid image "{}". Use a custom image name, id, or pick one from {}'
        raise CLIError(err.format(namespace.image, [x['urnAlias'] for x in images]))


def load_images_from_aliases_doc(publisher=None, offer=None, sku=None):
    target_url = ('https://raw.githubusercontent.com/Azure/azure-rest-api-specs/'
                  'master/arm-compute/quickstart-templates/aliases.json')
    txt = urlopen(target_url).read()
    dic = json.loads(txt.decode())
    try:
        all_images = []
        result = (dic['outputs']['aliases']['value'])
        for v in result.values():  # loop around os
            for alias, vv in v.items():  # loop around distros
                all_images.append({
                    'urnAlias': alias,
                    'publisher': vv['publisher'],
                    'offer': vv['offer'],
                    'sku': vv['sku'],
                    'version': vv['version']
                })

        all_images = [i for i in all_images if (_partial_matched(publisher, i['publisher']) and
                                                _partial_matched(offer, i['offer']) and
                                                _partial_matched(sku, i['sku']))]
        return all_images
    except KeyError:
        raise CLIError('Could not retrieve image list from {}'.format(target_url))


def _partial_matched(pattern, string):
    if not pattern:
        return True  # empty pattern means wildcard-match
    pattern = r'.*' + pattern
    return re.match(pattern, string, re.I)  # pylint: disable=no-member


def validate_ssh_key(namespace):
    string_or_file = (namespace.ssh_key or
                      os.path.join(os.path.expanduser('~'), '.ssh/id_rsa.pub'))
    content = string_or_file
    if os.path.exists(string_or_file):
        logger.info('Use existing SSH public key file: %s', string_or_file)
        with open(string_or_file, 'r') as f:
            content = f.read()
    elif not _is_valid_ssh_rsa_public_key(content):
        if namespace.generate_ssh_keys:
            # figure out appropriate file names:
            # 'base_name'(with private keys), and 'base_name.pub'(with public keys)
            public_key_filepath = string_or_file
            if public_key_filepath[-4:].lower() == '.pub':
                private_key_filepath = public_key_filepath[:-4]
            else:
                private_key_filepath = public_key_filepath + '.private'
            content = _generate_ssh_keys(private_key_filepath, public_key_filepath)
            logger.warning('Created SSH key files: %s,%s',
                           private_key_filepath, public_key_filepath)
        else:
            raise CLIError('An RSA key file or key value must be supplied to SSH Key Value. '
                           'You can use --generate-ssh-keys to let CLI generate one for you')
    namespace.ssh_key = content


def _generate_ssh_keys(private_key_filepath, public_key_filepath):
    import paramiko

    ssh_dir, _ = os.path.split(private_key_filepath)
    if not os.path.exists(ssh_dir):
        os.makedirs(ssh_dir)
        os.chmod(ssh_dir, 0o700)

    key = paramiko.RSAKey.generate(2048)
    key.write_private_key_file(private_key_filepath)
    os.chmod(private_key_filepath, 0o600)

    with open(public_key_filepath, 'w') as public_key_file:
        public_key = '%s %s' % (key.get_name(), key.get_base64())
        public_key_file.write(public_key)
    os.chmod(public_key_filepath, 0o644)

    return public_key


def _is_valid_ssh_rsa_public_key(openssh_pubkey):
    # http://stackoverflow.com/questions/2494450/ssh-rsa-public-key-validation-using-a-regular-expression # pylint: disable=line-too-long
    # A "good enough" check is to see if the key starts with the correct header.
    import struct
    try:
        from base64 import decodebytes as base64_decode
    except ImportError:
        # deprecated and redirected to decodebytes in Python 3
        from base64 import decodestring as base64_decode
    parts = openssh_pubkey.split()
    if len(parts) < 2:
        return False
    key_type = parts[0]
    key_string = parts[1]

    data = base64_decode(key_string.encode())  # pylint:disable=deprecated-method
    int_len = 4
    str_len = struct.unpack('>I', data[:int_len])[0]  # this should return 7
    return data[int_len:int_len + str_len] == key_type.encode()