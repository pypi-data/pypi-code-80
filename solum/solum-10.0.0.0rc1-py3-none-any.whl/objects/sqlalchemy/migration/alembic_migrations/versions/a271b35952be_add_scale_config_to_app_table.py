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

Revision ID: a271b35952be
Revises: 272e7cd352f9
Create Date: 2016-02-03 15:46:27.641527

"""
from alembic import op
import sqlalchemy as sa

from solum.objects.sqlalchemy import models

# revision identifiers, used by Alembic.
revision = 'a271b35952be'
down_revision = '272e7cd352f9'


def upgrade():
    op.add_column('app',
                  sa.Column('scale_config', models.JSONEncodedDict(1024)))


def downgrade():
    op.drop_column('app', 'scale_config')
