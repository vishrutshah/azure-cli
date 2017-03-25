# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# coding: utf-8
# pylint: skip-file
from msrest.serialization import Model


class FormulaPropertiesFromVm(Model):
    """Information about a VM from which a formula is to be created.

    :param lab_vm_id: The identifier of the VM from which a formula is to be
     created.
    :type lab_vm_id: str
    """

    _attribute_map = {
        'lab_vm_id': {'key': 'labVmId', 'type': 'str'},
    }

    def __init__(self, lab_vm_id=None):
        self.lab_vm_id = lab_vm_id
