# Copyright 2021 Outside Open
# This file is part of Digital-Hydrant.

# Digital-Hydrant is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Digital-Hydrant is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Digital-Hydrant.  If not, see https://www.gnu.org/licenses/.

from digital_hydrant import logging
from digital_hydrant.scheduler import Scheduler
from digital_hydrant.uploader import Uploader
from digital_hydrant.collector_queue import CollectorQueue
from digital_hydrant.ping import Ping
from digital_hydrant.args import args
from digital_hydrant.process_manager import ProcessManager


def run():
    logger = logging.getLogger(__name__)
    manager = ProcessManager("Main")

    if args.clear_queue:
        queue = CollectorQueue()
        queue.remove_all()

    # ping the server
    ping = Ping()
    manager.add_process("ping", ping.__exec__)

    collect = args.collect
    upload = args.upload

    if not (collect or upload):
        collect = upload = True

    if collect:
        scheduler = Scheduler()
        manager.add_process("scheduler", scheduler.__schedule__)

    if upload:
        logger.info("Launching Uploader")
        # upload data to the api
        uploader = Uploader()
        manager.add_process("uploader", uploader.__upload__)

    manager.manage()
