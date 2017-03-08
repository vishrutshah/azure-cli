# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.help_files import helps


helps['lab'] = """
            type: group
            short-summary: Commands to manage Azure DevTestLabs service.
            """
helps['lab vm'] = """
            type: group
            short-summary: Commands to manage vm of Azure DevTestLab.
            """
helps['lab custom-image'] = """
            type: group
            short-summary: Commands to manage custom images of Azure DevTestLab.
            """
helps['lab gallery-image'] = """
            type: group
            short-summary: Commands to list gallery images of Azure DevTestLab.
            """
helps['lab artifact'] = """
            type: group
            short-summary: Commands to manage artifact of Azure DevTestLab.
            """
