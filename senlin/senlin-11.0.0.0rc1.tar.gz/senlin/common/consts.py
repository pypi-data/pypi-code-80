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

from oslo_log import log as logging

RPC_ATTRS = (
    CONDUCTOR_TOPIC,
    ENGINE_TOPIC,
    HEALTH_MANAGER_TOPIC,
    RPC_API_VERSION_BASE,
    RPC_API_VERSION,
) = (
    'senlin-conductor',
    'senlin-engine',
    'senlin-health-manager',
    '1.0',
    '1.1',
)

RPC_PARAMS = (
    PARAM_LIMIT, PARAM_MARKER, PARAM_GLOBAL_PROJECT,
    PARAM_SHOW_DETAILS, PARAM_SORT,
) = (
    'limit', 'marker', 'global_project',
    'show_details', 'sort',
)

SUPPORT_STATUSES = (
    EXPERIMENTAL, SUPPORTED, DEPRECATED, UNSUPPORTED,
) = (
    'EXPERIMENTAL', 'SUPPORTED', 'DEPRECATED', 'UNSUPPORTED',
)

ACTION_CAUSES = (
    CAUSE_RPC, CAUSE_DERIVED, CAUSE_DERIVED_LCH
) = (
    'RPC Request',
    'Derived Action',
    'Derived Action with Lifecycle Hook'
)

CLUSTER_ACTION_NAMES = (
    CLUSTER_CREATE, CLUSTER_DELETE, CLUSTER_UPDATE,
    CLUSTER_ADD_NODES, CLUSTER_DEL_NODES, CLUSTER_RESIZE,
    CLUSTER_CHECK, CLUSTER_RECOVER, CLUSTER_REPLACE_NODES,
    CLUSTER_SCALE_OUT, CLUSTER_SCALE_IN,
    CLUSTER_ATTACH_POLICY, CLUSTER_DETACH_POLICY, CLUSTER_UPDATE_POLICY,
    CLUSTER_OPERATION,
) = (
    'CLUSTER_CREATE', 'CLUSTER_DELETE', 'CLUSTER_UPDATE',
    'CLUSTER_ADD_NODES', 'CLUSTER_DEL_NODES', 'CLUSTER_RESIZE',
    'CLUSTER_CHECK', 'CLUSTER_RECOVER', 'CLUSTER_REPLACE_NODES',
    'CLUSTER_SCALE_OUT', 'CLUSTER_SCALE_IN',
    'CLUSTER_ATTACH_POLICY', 'CLUSTER_DETACH_POLICY', 'CLUSTER_UPDATE_POLICY',
    'CLUSTER_OPERATION',
)

CLUSTER_SCALE_ACTIONS = [CLUSTER_SCALE_IN, CLUSTER_SCALE_OUT]

NODE_ACTION_NAMES = (
    NODE_CREATE, NODE_DELETE, NODE_UPDATE,
    NODE_JOIN, NODE_LEAVE,
    NODE_CHECK, NODE_RECOVER, NODE_OPERATION,
) = (
    'NODE_CREATE', 'NODE_DELETE', 'NODE_UPDATE',
    'NODE_JOIN', 'NODE_LEAVE',
    'NODE_CHECK', 'NODE_RECOVER', 'NODE_OPERATION',
)

ADJUSTMENT_PARAMS = (
    ADJUSTMENT_TYPE, ADJUSTMENT_NUMBER, ADJUSTMENT_MIN_STEP,
    ADJUSTMENT_MIN_SIZE, ADJUSTMENT_MAX_SIZE, ADJUSTMENT_STRICT,
) = (
    'adjustment_type', 'number', 'min_step',
    'min_size', 'max_size', 'strict',
)

ADJUSTMENT_TYPES = (
    EXACT_CAPACITY, CHANGE_IN_CAPACITY, CHANGE_IN_PERCENTAGE,
) = (
    'EXACT_CAPACITY', 'CHANGE_IN_CAPACITY', 'CHANGE_IN_PERCENTAGE',
)

CLUSTER_ATTRS = (
    CLUSTER_NAME, CLUSTER_PROFILE, CLUSTER_DESIRED_CAPACITY,
    CLUSTER_MIN_SIZE, CLUSTER_MAX_SIZE, CLUSTER_ID,
    CLUSTER_DOMAIN, CLUSTER_PROJECT, CLUSTER_USER,
    CLUSTER_INIT_AT, CLUSTER_CREATED_AT, CLUSTER_UPDATED_AT,
    CLUSTER_STATUS, CLUSTER_STATUS_REASON, CLUSTER_TIMEOUT,
    CLUSTER_METADATA, CLUSTER_CONFIG,
) = (
    'name', 'profile_id', 'desired_capacity',
    'min_size', 'max_size', 'id',
    'domain', 'project', 'user',
    'init_at', 'created_at', 'updated_at',
    'status', 'status_reason', 'timeout',
    'metadata', 'config',
)

CLUSTER_PARAMS = (
    CLUSTER_PROFILE_ONLY, CLUSTER_DELETE_FORCE
) = (
    'profile_only', 'force',
)

CLUSTER_STATUSES = (
    CS_INIT, CS_ACTIVE, CS_CREATING, CS_UPDATING, CS_RESIZING, CS_DELETING,
    CS_CHECKING, CS_RECOVERING, CS_CRITICAL, CS_ERROR, CS_WARNING,
    CS_OPERATING,
) = (
    'INIT', 'ACTIVE', 'CREATING', 'UPDATING', 'RESIZING', 'DELETING',
    'CHECKING', 'RECOVERING', 'CRITICAL', 'ERROR', 'WARNING',
    'OPERATING',
)

NODE_STATUSES = (
    NS_INIT, NS_ACTIVE, NS_ERROR, NS_WARNING, NS_CREATING, NS_UPDATING,
    NS_DELETING, NS_RECOVERING, NS_OPERATING,
) = (
    'INIT', 'ACTIVE', 'ERROR', 'WARNING', 'CREATING', 'UPDATING',
    'DELETING', 'RECOVERING', 'OPERATING',
)

CLUSTER_SORT_KEYS = [
    CLUSTER_NAME, CLUSTER_STATUS,
    CLUSTER_INIT_AT, CLUSTER_CREATED_AT, CLUSTER_UPDATED_AT,
]

NODE_ATTRS = (
    NODE_INDEX, NODE_NAME, NODE_PROFILE_ID, NODE_CLUSTER_ID,
    NODE_INIT_AT, NODE_CREATED_AT, NODE_UPDATED_AT,
    NODE_STATUS, NODE_ROLE, NODE_METADATA, NODE_TAINTED,
) = (
    'index', 'name', 'profile_id', 'cluster_id',
    'init_at', 'created_at', 'updated_at',
    'status', 'role', 'metadata', 'tainted',
)

NODE_SORT_KEYS = [
    NODE_INDEX, NODE_NAME, NODE_STATUS,
    NODE_INIT_AT, NODE_CREATED_AT, NODE_UPDATED_AT,
]

NODE_PARAMS = (
    NODE_DELETE_FORCE,
) = (
    'force',
)

PROFILE_ATTRS = (
    PROFILE_ID, PROFILE_NAME, PROFILE_TYPE,
    PROFILE_CREATED_AT, PROFILE_UPDATED_AT,
    PROFILE_SPEC, PROFILE_METADATA, PROFILE_CONTEXT,
) = (
    'id', 'name', 'type',
    'created_at', 'updated_at',
    'spec', 'metadata', 'context',
)

PROFILE_SORT_KEYS = [
    PROFILE_TYPE, PROFILE_NAME, PROFILE_CREATED_AT, PROFILE_UPDATED_AT,
]

POLICY_ATTRS = (
    POLICY_ID, POLICY_NAME, POLICY_TYPE, POLICY_SPEC,
    POLICY_CREATED_AT, POLICY_UPDATED_AT,
) = (
    'id', 'name', 'type', 'spec',
    'created_at', 'updated_at',
)

POLICY_SORT_KEYS = [
    POLICY_TYPE, POLICY_NAME,
    POLICY_CREATED_AT, POLICY_UPDATED_AT,
]

CLUSTER_POLICY_ATTRS = (
    CP_POLICY_ID, CP_ENABLED, CP_PRIORITY,
    CP_POLICY_NAME, CP_POLICY_TYPE,
) = (
    'policy_id', 'enabled', 'priority',
    'policy_name', 'policy_type',
)

CLUSTER_POLICY_SORT_KEYS = [
    CP_ENABLED,
]

EVENT_ATTRS = (
    EVENT_TIMESTAMP, EVENT_OBJ_ID, EVENT_OBJ_NAME, EVENT_OBJ_TYPE,
    EVENT_USER, EVENT_ACTION, EVENT_STATUS, EVENT_STATUS_REASON,
    EVENT_LEVEL, EVENT_CLUSTER_ID,
) = (
    'timestamp', 'oid', 'oname', 'otype',
    'user', 'action', 'status', 'status_reason',
    'level', 'cluster_id',
)

EVENT_SORT_KEYS = [
    EVENT_TIMESTAMP, EVENT_LEVEL, EVENT_OBJ_TYPE, EVENT_OBJ_NAME,
    EVENT_ACTION, EVENT_STATUS, EVENT_OBJ_ID, EVENT_CLUSTER_ID,
]

ACTION_ATTRS = (
    ACTION_NAME, ACTION_CLUSTER_ID, ACTION_TARGET, ACTION_ACTION, ACTION_CAUSE,
    ACTION_INTERVAL, ACTION_START_TIME, ACTION_END_TIME,
    ACTION_TIMEOUT, ACTION_STATUS, ACTION_STATUS_REASON,
    ACTION_INPUTS, ACTION_OUTPUTS, ACTION_DEPENDS_ON, ACTION_DEPENDED_BY,
    ACTION_CREATED_AT, ACTION_UPDATED_AT,
) = (
    'name', 'cluster_id', 'target', 'action', 'cause',
    'interval', 'start_time', 'end_time',
    'timeout', 'status', 'status_reason',
    'inputs', 'outputs', 'depends_on', 'depended_by',
    'created_at', 'updated_at',
)

ACTION_SORT_KEYS = [
    ACTION_NAME, ACTION_TARGET, ACTION_ACTION, ACTION_CREATED_AT,
    ACTION_STATUS,
]

RECEIVER_TYPES = (
    RECEIVER_WEBHOOK, RECEIVER_MESSAGE,
) = (
    'webhook', 'message',
)

RECEIVER_ATTRS = (
    RECEIVER_NAME, RECEIVER_TYPE, RECEIVER_CLUSTER, RECEIVER_CLUSTER_ID,
    RECEIVER_CREATED_AT, RECEIVER_UPDATED_AT, RECEIVER_USER_ID,
    RECEIVER_ACTOR, RECEIVER_ACTION, RECEIVER_PARAMS, RECEIVER_CHANNEL,
) = (
    'name', 'type', 'cluster', 'cluster_id',
    'created_at', 'updated_at', 'user',
    'actor', 'action', 'params', 'channel',
)

RECEIVER_SORT_KEYS = [
    RECEIVER_NAME, RECEIVER_TYPE, RECEIVER_ACTION, RECEIVER_CLUSTER_ID,
    RECEIVER_CREATED_AT, RECEIVER_USER_ID,
]

CLUSTER_DEFAULT_VALUE = (
    CLUSTER_DEFAULT_MIN_SIZE, CLUSTER_DEFAULT_MAX_SIZE
) = (
    0, -1
)

# Note: This is a copy of action status definition defined in
# senlin.engine.actions.base module.
ACTION_STATUSES = (
    ACTION_INIT, ACTION_WAITING, ACTION_READY, ACTION_RUNNING,
    ACTION_SUCCEEDED, ACTION_FAILED, ACTION_CANCELLED,
    ACTION_WAITING_LIFECYCLE_COMPLETION, ACTION_SUSPENDED,
) = (
    'INIT', 'WAITING', 'READY', 'RUNNING',
    'SUCCEEDED', 'FAILED', 'CANCELLED', 'WAITING_LIFECYCLE_COMPLETION',
    'SUSPENDED',
)

ACTION_PARAMS = (
    ACTION_UPDATE_FORCE,
) = (
    'force',
)

EVENT_LEVELS = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARN': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
}

DETECTION_TYPES = (
    LIFECYCLE_EVENTS, NODE_STATUS_POLLING, NODE_STATUS_POLL_URL,
    HYPERVISOR_STATUS_POLLING,
    # LB_STATUS_POLLING,
) = (
    'LIFECYCLE_EVENTS', 'NODE_STATUS_POLLING', 'NODE_STATUS_POLL_URL',
    'HYPERVISOR_STATUS_POLLING',
    # 'LB_STATUS_POLLING',
)

HEALTH_CHECK_TYPES = (
    EVENTS, POLLING,
) = (
    'EVENTS', 'POLLING'
)

RECOVERY_ACTIONS = (
    RECOVER_REBOOT, RECOVER_REBUILD, RECOVER_RECREATE,
) = (
    'REBOOT', 'REBUILD', 'RECREATE',
)

RECOVERY_CONDITIONAL = (
    ALL_FAILED, ANY_FAILED,
) = (
    'ALL_FAILED', 'ANY_FAILED',
)

NOTIFICATION_PRIORITIES = (
    PRIO_AUDIT, PRIO_CRITICAL, PRIO_ERROR, PRIO_WARN, PRIO_INFO, PRIO_DEBUG,
    PRIO_SAMPLE,
) = (
    'audit', 'critical', 'error', 'warn', 'info', 'debug', 'sample',
)

NOTIFICATION_PHASES = (
    PHASE_START, PHASE_END, PHASE_ERROR,
) = (
    'start', 'end', 'error',
)

LIFECYCLE_TRANSITION_TYPE = (
    LIFECYCLE_NODE_TERMINATION,
) = (
    'termination',
)

VM_STATUS = (
    VS_ACTIVE, VS_ERROR, VS_SUSPENDED, VS_SHUTOFF, VS_PAUSED, VS_RESCUE,
    VS_DELETED,
) = (
    'ACTIVE', 'ERROR', 'SUSPENDED', 'SHUTOFF', 'PAUSED', 'RESCUE', 'DELETED',
)

HEALTH_CHECK_MESSAGE = (
    POLL_STATUS_PASS, POLL_STATUS_FAIL, POLL_URL_PASS, POLL_URL_FAIL,
) = (
    'Poll Status health check passed',
    'Poll Status health check failed',
    'Poll URL health check passed',
    'Poll URL health check failed',
)

CONFLICT_BYPASS_ACTIONS = [
    CLUSTER_DELETE, NODE_DELETE, NODE_OPERATION,
]

LOCK_BYPASS_ACTIONS = [
    CLUSTER_DELETE, NODE_DELETE, NODE_OPERATION,
]

REBOOT_TYPE = 'type'

REBOOT_TYPES = (
    REBOOT_SOFT, REBOOT_HARD
) = (
    'SOFT', 'HARD'
)
