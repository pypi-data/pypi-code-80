# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from sqlalchemy import MetaData, Numeric, Table


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    table = Table('action', meta, autoload=True)
    table.c.start_time.alter(type=Numeric('18,6'))
    table.c.end_time.alter(type=Numeric('18,6'))
