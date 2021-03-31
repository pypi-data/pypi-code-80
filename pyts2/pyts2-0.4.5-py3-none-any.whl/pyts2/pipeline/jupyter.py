# Copyright (c) 2021 Gekkonid Consulting/Kevin Murray <foss@kdmurray.id.au>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .base import PipelineStep

 
class JupyterDisplayImageStep(PipelineStep):
    """Displays an image in Jupyter"""

    def __init__(self, title_minter=None):
        self.title_minter = title_minter

    def process_file(self, file):
        # import here so that it's not a required dependency
        from IPython.core.display import Image, display
        if self.title_minter is not None:
            print(self.title_minter(file))
        display(Image(data=file.content))
        return file
