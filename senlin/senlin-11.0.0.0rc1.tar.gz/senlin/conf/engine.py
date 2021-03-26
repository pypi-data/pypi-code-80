# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from oslo_config import cfg

from senlin.common.i18n import _


ENGINE_GROUP = cfg.OptGroup('engine')
ENGINE_OPTS = [
    cfg.IntOpt('workers',
               default=1,
               deprecated_name='num_engine_workers',
               deprecated_group="DEFAULT",
               help=_('Number of senlin-engine processes.')),
    cfg.IntOpt('threads',
               default=1000,
               deprecated_name='scheduler_thread_pool_size',
               deprecated_group="DEFAULT",
               help=_('Number of senlin-engine threads.')),
]


def register_opts(conf):
    conf.register_group(ENGINE_GROUP)
    conf.register_opts(ENGINE_OPTS, group=ENGINE_GROUP)


def list_opts():
    return {
        ENGINE_GROUP: ENGINE_OPTS,
    }
