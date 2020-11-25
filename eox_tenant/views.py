# -*- coding: utf-8 -*-
"""The generic views for the eox-tenant plugin project"""

from __future__ import unicode_literals

from os.path import dirname, realpath
from subprocess import CalledProcessError, check_output

from django.http import JsonResponse

import eox_tenant


def info_view(request):  # pylint: disable=unused-argument
    """
    Basic view to show the working version and the exact git commit of the
    installed app.
    """
    try:
        working_dir = dirname(realpath(__file__))
        git_data = check_output(["git", "rev-parse", "HEAD"], cwd=working_dir)
        git_data = git_data.decode().rstrip('\r\n')
    except CalledProcessError:
        git_data = ""

    return JsonResponse(
        {
            "version": eox_tenant.__version__,
            "name": "eox-tenant",
            "git": git_data,
        },
    )
