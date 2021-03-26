# Copyright (c) 2016 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import ipaddress
import json
import socket
import sys

from oslo_config import cfg
from oslo_config import types
from oslo_log import log
from oslo_utils import importutils
from oslo_utils import units

from manila.common import constants
from manila import exception
from manila.i18n import _
from manila.message import api as message_api
from manila.message import message_field
from manila.share import driver
from manila.share.drivers import ganesha
from manila.share.drivers.ganesha import utils as ganesha_utils
from manila.share.drivers import helpers as driver_helpers

rados = None
json_command = None


def setup_rados():
    global rados
    if not rados:
        try:
            rados = importutils.import_module('rados')
        except ImportError:
            raise exception.ShareBackendException(
                _("rados python module is not installed"))


def setup_json_command():
    global json_command
    if not json_command:
        try:
            json_command = importutils.import_class(
                'ceph_argparse.json_command')
        except ImportError:
            raise exception.ShareBackendException(
                _("ceph_argparse python module is not installed"))


CEPHX_ACCESS_TYPE = "cephx"

# The default Ceph administrative identity
CEPH_DEFAULT_AUTH_ID = "admin"

DEFAULT_VOLUME_MODE = '755'

RADOS_TIMEOUT = 10

LOG = log.getLogger(__name__)

# Clone statuses
CLONE_CREATING = 'creating'
CLONE_FAILED = 'failed'
CLONE_CANCELED = 'canceled'
CLONE_PENDING = 'pending'
CLONE_INPROGRESS = 'in-progress'
CLONE_COMPLETE = 'complete'

cephfs_opts = [
    cfg.StrOpt('cephfs_conf_path',
               default="",
               help="Fully qualified path to the ceph.conf file."),
    cfg.StrOpt('cephfs_cluster_name',
               help="The name of the cluster in use, if it is not "
                    "the default ('ceph')."
               ),
    cfg.StrOpt('cephfs_auth_id',
               default="manila",
               help="The name of the ceph auth identity to use."
               ),
    cfg.StrOpt('cephfs_volume_path_prefix',
               deprecated_for_removal=True,
               deprecated_since='Wallaby',
               deprecated_reason='This option is not used starting with '
                                 'the Nautilus release of Ceph.',
               default="/volumes",
               help="The prefix of the cephfs volume path."
               ),
    cfg.StrOpt('cephfs_protocol_helper_type',
               default="CEPHFS",
               choices=['CEPHFS', 'NFS'],
               ignore_case=True,
               help="The type of protocol helper to use. Default is "
                    "CEPHFS."
               ),
    cfg.BoolOpt('cephfs_ganesha_server_is_remote',
                default=False,
                help="Whether the NFS-Ganesha server is remote to the driver."
                ),
    cfg.HostAddressOpt('cephfs_ganesha_server_ip',
                       help="The IP address of the NFS-Ganesha server."),
    cfg.StrOpt('cephfs_ganesha_server_username',
               default='root',
               help="The username to authenticate as in the remote "
                    "NFS-Ganesha server host."),
    cfg.StrOpt('cephfs_ganesha_path_to_private_key',
               help="The path of the driver host's private SSH key file."),
    cfg.StrOpt('cephfs_ganesha_server_password',
               secret=True,
               help="The password to authenticate as the user in the remote "
                    "Ganesha server host. This is not required if "
                    "'cephfs_ganesha_path_to_private_key' is configured."),
    cfg.ListOpt('cephfs_ganesha_export_ips',
                default='',
                help="List of IPs to export shares. If not supplied, "
                     "then the value of 'cephfs_ganesha_server_ip' "
                     "will be used to construct share export locations."),
    cfg.StrOpt('cephfs_volume_mode',
               default=DEFAULT_VOLUME_MODE,
               help="The read/write/execute permissions mode for CephFS "
                    "volumes, snapshots, and snapshot groups expressed in "
                    "Octal as with linux 'chmod' or 'umask' commands."),
    cfg.StrOpt('cephfs_filesystem_name',
               help="The name of the filesystem to use, if there are "
                    "multiple filesystems in the cluster."),
]


CONF = cfg.CONF
CONF.register_opts(cephfs_opts)


class RadosError(Exception):
    """Something went wrong talking to Ceph with librados"""

    pass


def rados_command(rados_client, prefix=None, args=None, json_obj=False):
    """Safer wrapper for ceph_argparse.json_command

    Raises error exception instead of relying on caller to check return
    codes.

    Error exception can result from:
    * Timeout
    * Actual legitimate errors
    * Malformed JSON output

    return: If json_obj is True, return the decoded JSON object from ceph,
            or None if empty string returned.
            If json is False, return a decoded string (the data returned by
            ceph command)
    """
    if args is None:
        args = {}

    argdict = args.copy()
    argdict['format'] = 'json'

    LOG.debug("Invoking ceph_argparse.json_command - rados_client=%(cl)s, "
              "prefix='%(pf)s', argdict=%(ad)s, timeout=%(to)s.",
              {"cl": rados_client, "pf": prefix, "ad": argdict,
               "to": RADOS_TIMEOUT})

    try:
        ret, outbuf, outs = json_command(rados_client,
                                         prefix=prefix,
                                         argdict=argdict,
                                         timeout=RADOS_TIMEOUT)
        if ret != 0:
            raise rados.Error(outs, ret)
        if not json_obj:
            result = outbuf.decode().strip()
        else:
            if outbuf:
                result = json.loads(outbuf.decode().strip())
            else:
                result = None
    except Exception as e:
        msg = _("json_command failed - prefix=%(pfx)s, argdict=%(ad)s - "
                "exception message: %(ex)s." %
                {"pfx": prefix, "ad": argdict, "ex": e})
        raise exception.ShareBackendException(msg)

    return result


class CephFSDriver(driver.ExecuteMixin, driver.GaneshaMixin,
                   driver.ShareDriver):
    """Driver for the Ceph Filesystem."""

    def __init__(self, *args, **kwargs):
        super(CephFSDriver, self).__init__(False, *args, **kwargs)
        self.backend_name = self.configuration.safe_get(
            'share_backend_name') or 'CephFS'

        setup_rados()
        setup_json_command()
        self._rados_client = None
        # name of the filesystem/volume used by the driver
        self._volname = None

        self.configuration.append_config_values(cephfs_opts)

        try:
            int(self.configuration.cephfs_volume_mode, 8)
        except ValueError:
            msg = _("Invalid CephFS volume mode %s")
            raise exception.BadConfigurationException(
                msg % self.configuration.cephfs_volume_mode)

        self._cephfs_volume_mode = self.configuration.cephfs_volume_mode
        self.ipv6_implemented = True

    def do_setup(self, context):
        if self.configuration.cephfs_protocol_helper_type.upper() == "CEPHFS":
            protocol_helper_class = getattr(
                sys.modules[__name__], 'NativeProtocolHelper')
        else:
            protocol_helper_class = getattr(
                sys.modules[__name__], 'NFSProtocolHelper')

        self.protocol_helper = protocol_helper_class(
            self._execute,
            self.configuration,
            rados_client=self.rados_client,
            volname=self.volname)

        self.protocol_helper.init_helper()

    def check_for_setup_error(self):
        """Returns an error if prerequisites aren't met."""
        self.protocol_helper.check_for_setup_error()

    def _update_share_stats(self):
        stats = self.rados_client.get_cluster_stats()

        total_capacity_gb = round(stats['kb'] / units.Mi, 2)
        free_capacity_gb = round(stats['kb_avail'] / units.Mi, 2)

        data = {
            'vendor_name': 'Ceph',
            'driver_version': '1.0',
            'share_backend_name': self.backend_name,
            'storage_protocol': self.configuration.safe_get(
                'cephfs_protocol_helper_type'),
            'pools': [
                {
                    'pool_name': 'cephfs',
                    'total_capacity_gb': total_capacity_gb,
                    'free_capacity_gb': free_capacity_gb,
                    'qos': 'False',
                    'reserved_percentage': self.configuration.safe_get(
                        'reserved_share_percentage'),
                    'dedupe': [False],
                    'compression': [False],
                    'thin_provisioning': [False]
                }
            ],
            'total_capacity_gb': total_capacity_gb,
            'free_capacity_gb': free_capacity_gb,
            'snapshot_support': True,
            'create_share_from_snapshot_support': True,
        }
        super(    # pylint: disable=no-member
            CephFSDriver, self)._update_share_stats(data)

    def _to_bytes(self, gigs):
        """Convert a Manila size into bytes.

        Manila uses gibibytes everywhere.

        :param gigs: integer number of gibibytes.
        :return: integer number of bytes.
        """
        return gigs * units.Gi

    def _get_export_locations(self, share):
        """Get the export location for a share.

        :param share: a manila share.
        :return: the export location for a share.
        """

        # get path of FS subvolume/share
        argdict = {
            "vol_name": self.volname,
            "sub_name": share["id"]
        }
        if share['share_group_id'] is not None:
            argdict.update({"group_name": share["share_group_id"]})

        subvolume_path = rados_command(
            self.rados_client, "fs subvolume getpath", argdict)

        return self.protocol_helper.get_export_locations(share, subvolume_path)

    @property
    def rados_client(self):
        if self._rados_client:
            return self._rados_client

        conf_path = self.configuration.safe_get('cephfs_conf_path')
        cluster_name = self.configuration.safe_get('cephfs_cluster_name')
        auth_id = self.configuration.safe_get('cephfs_auth_id')
        self._rados_client = rados.Rados(
            name="client.{0}".format(auth_id),
            clustername=cluster_name,
            conffile=conf_path,
            conf={}
        )

        LOG.info("[%(be)s] Ceph client found, connecting...",
                 {"be": self.backend_name})
        try:
            if self._rados_client.state != "connected":
                self._rados_client.connect()
        except Exception:
            self._rados_client = None
            raise exception.ShareBackendException(
                "[%(be)s] Ceph client failed to connect.",
                {"be": self.backend_name})
        else:
            LOG.info("[%(be)s] Ceph client connection complete.",
                     {"be": self.backend_name})

        return self._rados_client

    @property
    def volname(self):
        # Name of the CephFS volume/filesystem where the driver creates
        # manila entities such as shares, sharegroups, snapshots, etc.
        if self._volname:
            return self._volname

        self._volname = self.configuration.safe_get('cephfs_filesystem_name')
        if not self._volname:
            out = rados_command(
                self.rados_client, "fs volume ls", json_obj=True)
            if len(out) == 1:
                self._volname = out[0]['name']
            else:
                if len(out) > 1:
                    msg = _("Specify Ceph filesystem name using "
                            "'cephfs_filesystem_name' driver option.")
                else:
                    msg = _("No Ceph filesystem found.")
                raise exception.ShareBackendException(msg=msg)

        return self._volname

    def create_share(self, context, share, share_server=None):
        """Create a CephFS volume.

        :param context: A RequestContext.
        :param share: A Share.
        :param share_server: Always None for CephFS native.
        :return: The export locations dictionary.
        """
        requested_proto = share['share_proto'].upper()
        supported_proto = (
            self.configuration.cephfs_protocol_helper_type.upper())
        if (requested_proto != supported_proto):
            msg = _("Share protocol %s is not supported.") % requested_proto
            raise exception.ShareBackendException(msg=msg)
        size = self._to_bytes(share['size'])

        LOG.debug("[%(be)s]: create_share: id=%(id)s, size=%(sz)s, "
                  "group=%(gr)s.",
                  {"be": self.backend_name, "id": share['id'],
                   "sz": share['size'], "gr": share['share_group_id']})

        # create FS subvolume/share
        argdict = {
            "vol_name": self.volname,
            "sub_name": share["id"],
            "size": size,
            "namespace_isolated": True,
            "mode": self._cephfs_volume_mode,
        }
        if share['share_group_id'] is not None:
            argdict.update({"group_name": share["share_group_id"]})

        rados_command(self.rados_client, "fs subvolume create", argdict)

        return self._get_export_locations(share)

    def _need_to_cancel_clone(self, share):
        # Is there an ongoing clone operation that needs to be canceled
        # so we can delete the share?
        need_to_cancel_clone = False

        argdict = {
            "vol_name": self.volname,
            "clone_name": share["id"],
        }
        if share['share_group_id'] is not None:
            argdict.update({"group_name": share["share_group_id"]})

        try:
            status = rados_command(
                self.rados_client, "fs clone status", argdict)
            if status in (CLONE_PENDING, CLONE_INPROGRESS):
                need_to_cancel_clone = True
        except exception.ShareBackendException as e:
            # Trying to get clone status on a regular subvolume is expected
            # to fail.
            if 'not allowed on subvolume' not in str(e).lower():
                raise exception.ShareBackendException(
                    "Failed to remove share.")

        return need_to_cancel_clone

    def delete_share(self, context, share, share_server=None):
        # remove FS subvolume/share
        LOG.debug("[%(be)s]: delete_share: id=%(id)s, group=%(gr)s.",
                  {"be": self.backend_name, "id": share['id'],
                   "gr": share['share_group_id']})

        if self._need_to_cancel_clone(share):
            try:
                argdict = {
                    "vol_name": self.volname,
                    "clone_name": share["id"],
                    "force": True,
                }
                if share['share_group_id'] is not None:
                    argdict.update({"group_name": share["share_group_id"]})

                rados_command(self.rados_client, "fs clone cancel", argdict)
            except rados.Error:
                raise exception.ShareBackendException(
                    "Failed to cancel clone operation.")

        argdict = {
            "vol_name": self.volname,
            "sub_name": share["id"],
            # We want to clean up the share even if the subvolume is
            # not in a good state.
            "force": True,
        }
        if share['share_group_id'] is not None:
            argdict.update({"group_name": share["share_group_id"]})

        rados_command(self.rados_client, "fs subvolume rm", argdict)

    def update_access(self, context, share, access_rules, add_rules,
                      delete_rules, share_server=None):
        return self.protocol_helper.update_access(
            context, share, access_rules, add_rules, delete_rules,
            share_server=share_server)

    def ensure_share(self, context, share, share_server=None):
        # Creation is idempotent
        return self.create_share(context, share, share_server)

    def extend_share(self, share, new_size, share_server=None):
        # resize FS subvolume/share
        LOG.debug("[%(be)s]: extend_share: share=%(id)s, size=%(sz)s.",
                  {"be": self.backend_name, "id": share['id'],
                   "sz": new_size})

        argdict = {
            "vol_name": self.volname,
            "sub_name": share["id"],
            "new_size": self._to_bytes(new_size),
        }
        if share['share_group_id'] is not None:
            argdict.update({"group_name": share["share_group_id"]})

        LOG.debug("extend_share {id} {size}".format(
            id=share['id'], size=new_size))

        rados_command(self.rados_client, "fs subvolume resize", argdict)

    def shrink_share(self, share, new_size, share_server=None):
        # resize FS subvolume/share
        LOG.debug("[%(be)s]: shrink_share: share=%(id)s, size=%(sz)s.",
                  {"be": self.backend_name, "id": share['id'],
                   "sz": new_size})

        argdict = {
            "vol_name": self.volname,
            "sub_name": share["id"],
            "new_size": self._to_bytes(new_size),
            "no_shrink": True,
        }
        if share["share_group_id"] is not None:
            argdict.update({"group_name": share["share_group_id"]})

        try:
            rados_command(self.rados_client, "fs subvolume resize", argdict)
        except exception.ShareBackendException as e:
            if 'would be lesser than' in str(e).lower():
                raise exception.ShareShrinkingPossibleDataLoss(
                    share_id=share['id'])
            raise

    def create_snapshot(self, context, snapshot, share_server=None):
        # create a FS snapshot
        LOG.debug("[%(be)s]: create_snapshot: original share=%(id)s, "
                  "snapshot=%(sn)s.",
                  {"be": self.backend_name, "id": snapshot['share_id'],
                   "sn": snapshot['id']})

        argdict = {
            "vol_name": self.volname,
            "sub_name": snapshot["share_id"],
            "snap_name": "_".join([snapshot["snapshot_id"], snapshot["id"]]),
        }

        rados_command(
            self.rados_client, "fs subvolume snapshot create", argdict)

    def delete_snapshot(self, context, snapshot, share_server=None):
        # delete a FS snapshot
        LOG.debug("[%(be)s]: delete_snapshot: snapshot=%(id)s.",
                  {"be": self.backend_name, "id": snapshot['id']})
        argdict = {
            "vol_name": self.volname,
            "sub_name": snapshot["share_id"],
            "snap_name": '_'.join([snapshot['snapshot_id'], snapshot['id']]),
            "force": True,
        }

        rados_command(self.rados_client, "fs subvolume snapshot rm", argdict)

    def create_share_group(self, context, sg_dict, share_server=None):
        # delete a FS group
        LOG.debug("[%(be)s]: create_share_group: share_group=%(id)s.",
                  {"be": self.backend_name, "id": sg_dict['id']})

        argdict = {
            "vol_name": self.volname,
            "group_name": sg_dict['id'],
            "mode": self._cephfs_volume_mode,
        }

        rados_command(self.rados_client, "fs subvolumegroup create", argdict)

    def delete_share_group(self, context, sg_dict, share_server=None):
        # create a FS group
        LOG.debug("[%(be)s]: delete_share_group: share_group=%(id)s.",
                  {"be": self.backend_name, "id": sg_dict['id']})

        argdict = {
            "vol_name": self.volname,
            "group_name": sg_dict['id'],
            "force": True,
        }

        rados_command(self.rados_client, "fs subvolumegroup rm", argdict)

    def delete_share_group_snapshot(self, context, snap_dict,
                                    share_server=None):
        # delete a FS group snapshot
        LOG.debug("[%(be)s]: delete_share_group_snapshot: "
                  "share_group=%(sg_id)s, snapshot=%(sn)s.",
                  {"be": self.backend_name, "sg_id": snap_dict['id'],
                   "sn": snap_dict["share_group_id"]})

        argdict = {
            "vol_name": self.volname,
            "group_name": snap_dict["share_group_id"],
            "snap_name": snap_dict["id"],
            "force": True,
        }

        rados_command(
            self.rados_client, "fs subvolumegroup snapshot rm", argdict)

        return None, []

    def create_share_group_snapshot(self, context, snap_dict,
                                    share_server=None):
        # create a FS group snapshot
        LOG.debug("[%(be)s]: create_share_group_snapshot: share_group=%(id)s, "
                  "snapshot=%(sn)s.",
                  {"be": self.backend_name, "id": snap_dict['share_group_id'],
                   "sn": snap_dict["id"]})

        argdict = {
            "vol_name": self.volname,
            "group_name": snap_dict["share_group_id"],
            "snap_name": snap_dict["id"]
        }

        rados_command(
            self.rados_client, "fs subvolumegroup snapshot create", argdict)

        return None, []

    def _get_clone_status(self, share):
        """Check the status of a newly cloned share."""
        argdict = {
            "vol_name": self.volname,
            "clone_name": share["id"]
        }
        if share['share_group_id'] is not None:
            argdict.update({"group_name": share["share_group_id"]})

        out = rados_command(self.rados_client,
                            "fs clone status", argdict, True)
        return out['status']['state']

    def _update_create_from_snapshot_status(self, share):
        updates = {
            'status': constants.STATUS_ERROR,
            'progress': None,
            'export_locations': []
        }
        status = self._get_clone_status(share)
        if status == CLONE_COMPLETE:
            updates['status'] = constants.STATUS_AVAILABLE
            updates['progress'] = '100%'
            updates['export_locations'] = self._get_export_locations(share)
        elif status in (CLONE_PENDING, CLONE_INPROGRESS):
            updates['status'] = constants.STATUS_CREATING_FROM_SNAPSHOT
        else:
            # error if clone operation is not progressing or completed
            raise exception.ShareBackendException(
                "rados client clone of snapshot [%(sn)s}] to new "
                "share [%(shr)s}] did not complete successfully." %
                {"sn": share["snapshot_id"], "shr": share["id"]})
        return updates

    def get_share_status(self, share, share_server=None):
        """Returns the current status for a share.

        :param share: a manila share.
        :param share_server: a manila share server (not currently supported).
        :returns: manila share status.
        """

        if share['status'] != constants.STATUS_CREATING_FROM_SNAPSHOT:
            LOG.warning("Caught an unexpected share status '%s' during share "
                        "status update routine. Skipping.", share['status'])
            return
        return self._update_create_from_snapshot_status(share)

    def create_share_from_snapshot(self, context, share, snapshot,
                                   share_server=None, parent_share=None):
        """Create a CephFS subvolume from a snapshot"""

        LOG.debug("[%(be)s]: create_share_from_snapshot: id=%(id)s, "
                  "snapshot=%(sn)s, size=%(sz)s, group=%(gr)s.",
                  {"be": self.backend_name, "id": share['id'],
                   "sn": snapshot['id'], "sz": share['size'],
                   "gr": share['share_group_id']})

        argdict = {
            "vol_name": self.volname,
            "sub_name": parent_share["id"],
            "snap_name": '_'.join([snapshot["snapshot_id"], snapshot["id"]]),
            "target_sub_name": share["id"]
        }
        if share['share_group_id'] is not None:
            argdict.update({"group_name": share["share_group_id"]})

        rados_command(
            self.rados_client, "fs subvolume snapshot clone", argdict)

        return self._update_create_from_snapshot_status(share)

    def __del__(self):
        if self._rados_client:
            LOG.info("[%(be)s] Ceph client disconnecting...",
                     {"be": self.backend_name})
            self._rados_client.shutdown()
            self._rados_client = None
            LOG.info("[%(be)s] Ceph client disconnected",
                     {"be": self.backend_name})

    def get_configured_ip_versions(self):
        return self.protocol_helper.get_configured_ip_versions()


class NativeProtocolHelper(ganesha.NASHelperBase):
    """Helper class for native CephFS protocol"""

    supported_access_types = (CEPHX_ACCESS_TYPE, )
    supported_access_levels = (constants.ACCESS_LEVEL_RW,
                               constants.ACCESS_LEVEL_RO)

    def __init__(self, execute, config, **kwargs):
        self.rados_client = kwargs.pop('rados_client')
        self.volname = kwargs.pop('volname')
        self.message_api = message_api.API()
        super(NativeProtocolHelper, self).__init__(execute, config,
                                                   **kwargs)

    def _init_helper(self):
        pass

    def check_for_setup_error(self):
        """Returns an error if prerequisites aren't met."""
        return

    def get_mon_addrs(self):
        result = []
        mon_map = rados_command(self.rados_client, "mon dump", json_obj=True)
        for mon in mon_map['mons']:
            ip_port = mon['addr'].split("/")[0]
            result.append(ip_port)

        return result

    def get_export_locations(self, share, subvolume_path):
        # To mount this you need to know the mon IPs and the path to the volume
        mon_addrs = self.get_mon_addrs()

        export_location = "{addrs}:{path}".format(
            addrs=",".join(mon_addrs),
            path=subvolume_path)

        LOG.info("Calculated export location for share %(id)s: %(loc)s",
                 {"id": share['id'], "loc": export_location})

        return {
            'path': export_location,
            'is_admin_only': False,
            'metadata': {},
        }

    def _allow_access(self, context, share, access, share_server=None):
        if access['access_type'] != CEPHX_ACCESS_TYPE:
            raise exception.InvalidShareAccessType(type=access['access_type'])

        ceph_auth_id = access['access_to']

        # We need to check here rather than the API or Manila Client to see
        # if the ceph_auth_id is the same as the one specified for Manila's
        # usage. This is due to the fact that the API and the Manila client
        # cannot read the contents of the Manila configuration file. If it
        # is the same, we need to error out.
        if ceph_auth_id == CONF.cephfs_auth_id:
            error_message = (_('Ceph authentication ID %s must be different '
                             'than the one the Manila service uses.') %
                             ceph_auth_id)
            raise exception.InvalidShareAccess(reason=error_message)

        argdict = {
            "vol_name": self.volname,
            "sub_name": share["id"],
            "auth_id": ceph_auth_id,
            "tenant_id": share["project_id"],
        }
        if share["share_group_id"] is not None:
            argdict.update({"group_name": share["share_group_id"]})

        readonly = access['access_level'] == constants.ACCESS_LEVEL_RO

        if readonly:
            argdict.update({"access_level": "r"})
        else:
            argdict.update({"access_level": "rw"})

        try:
            auth_result = rados_command(
                self.rados_client, "fs subvolume authorize", argdict)
        except exception.ShareBackendException as e:
            if 'not allowed' in str(e).lower():
                msg = ("Access to client %(client)s is not allowed. "
                       "Reason: %(reason)s")
                msg_payload = {'client': ceph_auth_id, 'reason': e}
                raise exception.InvalidShareAccess(
                    reason=msg % msg_payload)
            raise

        return auth_result

    def _deny_access(self, context, share, access, share_server=None):
        if access['access_type'] != CEPHX_ACCESS_TYPE:
            LOG.warning("Invalid access type '%(type)s', "
                        "ignoring in deny.",
                        {"type": access['access_type']})
            return

        argdict = {
            "vol_name": self.volname,
            "sub_name": share["id"],
            "auth_id": access['access_to']
        }
        if share["share_group_id"] is not None:
            argdict.update({"group_name": share["share_group_id"]})

        rados_command(self.rados_client, "fs subvolume deauthorize", argdict)
        rados_command(self.rados_client, "fs subvolume evict", argdict)

    def update_access(self, context, share, access_rules, add_rules,
                      delete_rules, share_server=None):
        access_updates = {}

        argdict = {
            "vol_name": self.volname,
            "sub_name": share["id"],
        }
        if share["share_group_id"] is not None:
            argdict.update({"group_name": share["share_group_id"]})

        if not (add_rules or delete_rules):  # recovery/maintenance mode
            add_rules = access_rules

            existing_auths = None

            existing_auths = rados_command(
                self.rados_client, "fs subvolume authorized_list",
                argdict, json_obj=True)

            if existing_auths:
                existing_auth_ids = set()
                for rule in range(len(existing_auths)):
                    for cephx_id in existing_auths[rule]:
                        existing_auth_ids.add(cephx_id)
                want_auth_ids = set(
                    [rule['access_to'] for rule in add_rules])
                delete_auth_ids = existing_auth_ids.difference(
                    want_auth_ids)
                delete_auth_ids_list = delete_auth_ids
                for delete_auth_id in delete_auth_ids_list:
                    delete_rules.append(
                        {
                            'access_to': delete_auth_id,
                            'access_type': CEPHX_ACCESS_TYPE,
                        })

        # During recovery mode, re-authorize share access for auth IDs that
        # were already granted access by the backend. Do this to fetch their
        # access keys and ensure that after recovery, manila and the Ceph
        # backend are in sync.
        for rule in add_rules:
            try:
                access_key = self._allow_access(context, share, rule)
            except (exception.InvalidShareAccessLevel,
                    exception.InvalidShareAccessType):
                self.message_api.create(
                    context,
                    message_field.Action.UPDATE_ACCESS_RULES,
                    share['project_id'],
                    resource_type=message_field.Resource.SHARE,
                    resource_id=share['share_id'],
                    detail=message_field.Detail.UNSUPPORTED_CLIENT_ACCESS)
                log_args = {'id': rule['access_id'],
                            'access_level': rule['access_level'],
                            'access_to': rule['access_to']}
                LOG.exception("Failed to provide %(access_level)s access to "
                              "%(access_to)s (Rule ID: %(id)s). Setting rule "
                              "to 'error' state.", log_args)
                access_updates.update({rule['access_id']: {'state': 'error'}})
            except exception.InvalidShareAccess:
                self.message_api.create(
                    context,
                    message_field.Action.UPDATE_ACCESS_RULES,
                    share['project_id'],
                    resource_type=message_field.Resource.SHARE,
                    resource_id=share['share_id'],
                    detail=message_field.Detail.FORBIDDEN_CLIENT_ACCESS)
                log_args = {'id': rule['access_id'],
                            'access_level': rule['access_level'],
                            'access_to': rule['access_to']}
                LOG.exception("Failed to provide %(access_level)s access to "
                              "%(access_to)s (Rule ID: %(id)s). Setting rule "
                              "to 'error' state.", log_args)
                access_updates.update({rule['access_id']: {'state': 'error'}})
            else:
                access_updates.update({
                    rule['access_id']: {'access_key': access_key},
                })

        for rule in delete_rules:
            self._deny_access(context, share, rule)

        return access_updates

    def get_configured_ip_versions(self):
        return [4]


class NFSProtocolHelper(ganesha.GaneshaNASHelper2):

    shared_data = {}
    supported_protocols = ('NFS',)

    def __init__(self, execute, config_object, **kwargs):
        if config_object.cephfs_ganesha_server_is_remote:
            execute = ganesha_utils.SSHExecutor(
                config_object.cephfs_ganesha_server_ip, 22, None,
                config_object.cephfs_ganesha_server_username,
                password=config_object.cephfs_ganesha_server_password,
                privatekey=config_object.cephfs_ganesha_path_to_private_key)
        else:
            execute = ganesha_utils.RootExecutor(execute)

        self.ganesha_host = config_object.cephfs_ganesha_server_ip
        if not self.ganesha_host:
            self.ganesha_host = socket.gethostname()
            LOG.info("NFS-Ganesha server's location defaulted to driver's "
                     "hostname: %s", self.ganesha_host)

        super(NFSProtocolHelper, self).__init__(execute, config_object,
                                                **kwargs)

        if not hasattr(self, 'rados_client'):
            self.rados_client = kwargs.pop('rados_client')
        if not hasattr(self, 'volname'):
            self.volname = kwargs.pop('volname')
        self.export_ips = config_object.cephfs_ganesha_export_ips
        if not self.export_ips:
            self.export_ips = [self.ganesha_host]
        self.configured_ip_versions = set()
        self.config = config_object

    def check_for_setup_error(self):
        """Returns an error if prerequisites aren't met."""
        host_address_obj = types.HostAddress()
        for export_ip in self.config.cephfs_ganesha_export_ips:
            try:
                host_address_obj(export_ip)
            except ValueError:
                msg = (_("Invalid list member of 'cephfs_ganesha_export_ips' "
                         "option supplied %s -- not a valid IP address or "
                         "hostname.") % export_ip)
                raise exception.InvalidParameterValue(err=msg)

    def get_export_locations(self, share, subvolume_path):
        export_locations = []
        for export_ip in self.export_ips:
            export_path = "{server_address}:{mount_path}".format(
                server_address=driver_helpers.escaped_address(export_ip),
                mount_path=subvolume_path)

            LOG.info("Calculated export path for share %(id)s: %(epath)s",
                     {"id": share['id'], "epath": export_path})
            export_location = {
                'path': export_path,
                'is_admin_only': False,
                'metadata': {},
            }
            export_locations.append(export_location)
        return export_locations

    def _default_config_hook(self):
        """Callback to provide default export block."""
        dconf = super(NFSProtocolHelper, self)._default_config_hook()
        conf_dir = ganesha_utils.path_from(__file__, "conf")
        ganesha_utils.patch(dconf, self._load_conf_dir(conf_dir))
        return dconf

    def _fsal_hook(self, base, share, access):
        """Callback to create FSAL subblock."""
        ceph_auth_id = ''.join(['ganesha-', share['id']])

        argdict = {
            "vol_name": self.volname,
            "sub_name": share["id"],
            "auth_id": ceph_auth_id,
            "access_level": "rw",
            "tenant_id": share["project_id"],
        }
        if share["share_group_id"] is not None:
            argdict.update({"group_name": share["share_group_id"]})

        auth_result = rados_command(
            self.rados_client, "fs subvolume authorize", argdict)

        # Restrict Ganesha server's access to only the CephFS subtree or path,
        # corresponding to the manila share, that is to be exported by making
        # Ganesha use Ceph auth IDs with path restricted capabilities to
        # communicate with CephFS.
        return {
            'Name': 'Ceph',
            'User_Id': ceph_auth_id,
            'Secret_Access_Key': auth_result
        }

    def _cleanup_fsal_hook(self, base, share, access):
        """Callback for FSAL specific cleanup after removing an export."""
        ceph_auth_id = ''.join(['ganesha-', share['id']])

        argdict = {
            "vol_name": self.volname,
            "sub_name": share["id"],
            "auth_id": ceph_auth_id,
        }
        if share["share_group_id"] is not None:
            argdict.update({"group_name": share["share_group_id"]})

        rados_command(self.rados_client, "fs subvolume deauthorize", argdict)

    def _get_export_path(self, share):
        """Callback to provide export path."""
        argdict = {
            "vol_name": self.volname,
            "sub_name": share["id"]
        }
        if share["share_group_id"] is not None:
            argdict.update({"group_name": share["share_group_id"]})

        path = rados_command(
            self.rados_client, "fs subvolume getpath", argdict)

        return path

    def _get_export_pseudo_path(self, share):
        """Callback to provide pseudo path."""
        return self._get_export_path(share)

    def get_configured_ip_versions(self):
        if not self.configured_ip_versions:
            try:
                for export_ip in self.export_ips:
                    self.configured_ip_versions.add(
                        ipaddress.ip_address(str(export_ip)).version)
            except Exception:
                # export_ips contained a hostname, safest thing is to
                # claim support for IPv4 and IPv6 address families
                LOG.warning("Setting configured IP versions to [4, 6] since "
                            "a hostname (rather than IP address) was supplied "
                            "in 'cephfs_ganesha_server_ip' or "
                            "in 'cephfs_ganesha_export_ips'.")
                return [4, 6]
        return list(self.configured_ip_versions)
