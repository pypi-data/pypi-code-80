# Copyright (c) 2020-2021 Gekkonid Consulting/Kevin Murray <foss@kdmurray.id.au>
# Copyright (c) 2020 Australian Plant Phenomics Facility
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .base import PipelineStep

from os.path import splitext
from datetime import datetime


class TelegrafRecordStep(PipelineStep):
    """Write each file to output, without changing the file"""

    def __init__(self, metric_name, telegraf_host='localhost', telegraf_port=8092, tags={}):
        from telegraf.client import TelegrafClient
        self.client = TelegrafClient(host=telegraf_host, port=telegraf_port)
        self.metric_name = metric_name
        self.tags = tags

    def process_file(self, file):
        fileext = splitext(file.filename)[1].lower().lstrip(".")
        tags = {"InstantIndex": file.instant.index, "FileType": fileext}
        tags.update(self.tags)
        epoch_ns = int(file.instant.datetime.timestamp() * 1e9)  # to NS
        now_ns = int(datetime.utcnow().timestamp() * 1e9)
        report = file.report
        report.update({"CapturedAt": epoch_ns, "ProcessedAt": now_ns})
        self.client.metric(self.metric_name, report, timestamp=epoch_ns, tags=tags)
        return file
