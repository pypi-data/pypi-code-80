# Copyright (c) 2020-2021 Gekkonid Consulting/Kevin Murray <foss@kdmurray.id.au>
# Copyright (c) 2020 Australian Plant Phenomics Facility
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .base import PipelineStep

from os.path import splitext
from datetime import datetime


class InfluxClientRecordStep(PipelineStep):
    """Write each file to output, without changing the file

    You can generate a Token from the "Tokens Tab" in the InfluxDB 2.0 UI
    buckets for influxdb cloud2.0 are "email-address"

    1.8 considerations:
        tokens are "username:password"
        bucket == database
        org is ignored

    """

    def __init__(self,
                 metric_name,
                 influxdb_url,
                 influxdb_bucket,
                 influxdb_token,
                 tags={},
                 tz=None,
                 influxdb_org="",
                 client=None):
        from influxdb_client import InfluxDBClient
        self.metric_name = metric_name
        self.org = influxdb_org
        self.bucket = influxdb_bucket
        self.tags = tags
        if client is not None:
            self.client = client
        else:
            self.client = InfluxDBClient(url=influxdb_url,
                                         token=influxdb_token,
                                         org=influxdb_org)

    def process_file(self, file):
        from influxdb_client import Point
        from influxdb_client.client.write_api import SYNCHRONOUS
        fileext = splitext(file.filename)[1].lower().lstrip(".")
        tags = {"InstantIndex": file.instant.index, "FileType": fileext}
        tags.update(self.tags)

        epoch_ns = int(file.instant.datetime.timestamp() * 1e9)  # to NS
        now_ns = int(datetime.utcnow().timestamp() * 1e9)

        file.report.update({"CapturedAt": epoch_ns, "ProcessedAt": now_ns})

        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        point = Point.from_dict({
            "measurement": self.metric_name,
            "time": epoch_ns,
            "fields": file.report,
            "tags": tags
        })
        write_api.write(bucket=self.bucket, org=self.org, record=point)
        return file
