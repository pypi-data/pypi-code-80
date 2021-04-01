# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import re_path
from grade_conversion_calculator.views import demo


urlpatterns = [
    re_path(r'^calculator-demo/?$', demo, name='calculator_demo'),
]
