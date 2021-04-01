# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.shortcuts import render


def demo(request):
    return render(request, "demo.html", {})
