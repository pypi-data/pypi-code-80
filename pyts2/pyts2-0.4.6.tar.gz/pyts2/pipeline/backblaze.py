# Copyright (c) 2020-2021 Gekkonid Consulting/Kevin Murray <foss@kdmurray.id.au>
# Copyright (c) 2020 Australian Plant Phenomics Facility
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .base import PipelineStep

import os


from b2sdk.v1 import InMemoryAccountInfo, B2Api


class WriteToB2Step(PipelineStep):
    """
    Write file to backblaze
    """

    def __init__(self,
                 b2_application_key_id=None,
                 b2_application_key=None,
                 b2_bucket_name=None,
                 b2_api=None,
                 prefix=""):

        from b2sdk.v1 import InMemoryAccountInfo, B2Api
        if b2_api is None:
            info = InMemoryAccountInfo()
            self.b2_api = B2Api(info)
            self.b2_api.authorize_account("production",
                                          self.b2_application_key_id,
                                          self.b2_application_key)
        else:
            self.b2_api = b2_api
        self.prefix = prefix.lstrip("/")

        self.b2_application_key_id = b2_application_key_id or os.environ.get("B2_APPLICATION_KEY_ID")
        self.b2_application_key = b2_application_key or os.environ.get("B2_APPLICATION_KEY")
        self.b2_bucket_name = b2_bucket_name or os.environ.get("B2_BUCKET_NAME")

    def process_file(self, file):
        from b2sdk.v1 import InMemoryAccountInfo, B2Api
        b2_bucket = self.b2_api.get_bucket_by_name(self.b2_bucket_name)
        file_version_info = b2_bucket.upload_bytes(file.content,
                                                   os.path.join(self.prefix, file.filename))

        file.filename = file_version_info.file_name
        assert file_version_info.content_md5 == file.md5sum
        return file
