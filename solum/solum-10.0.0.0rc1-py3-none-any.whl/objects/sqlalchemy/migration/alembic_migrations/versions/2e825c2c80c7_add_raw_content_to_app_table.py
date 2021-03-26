#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""empty message

Revision ID: 2e825c2c80c7
Revises: e5f2e8af3b8
Create Date: 2016-01-04 21:58:38.225814

"""
from alembic import op
import sqlalchemy as sa

from solum.objects.sqlalchemy import models

# revision identifiers, used by Alembic.
revision = '2e825c2c80c7'
down_revision = 'e5f2e8af3b8'


def upgrade():
    op.add_column('app',
                  sa.Column('raw_content', models.YAMLEncodedDict(2048)))


def downgrade():
    op.drop_column('app', 'raw_content')
