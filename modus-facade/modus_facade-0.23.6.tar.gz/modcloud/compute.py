"""Provide wrapper and common functions for Google Cloud Compute REST API."""
import logging.config
import time

from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)


class Compute(object):
    """Wrapper around google cloud compute."""

    def __init__(self, project_id, zone="europe-west1-d"):
        """Facade Modules to work Google Cloud Compute Engine.

        :param project_id: name of project
        :type project_id: str
        :param zone: zone of compute
        :type zone: str
        :return: None
        """
        self.project_id = project_id
        self.zone = zone
        self.build_service()

    def build_service(self):
        """Build the compute service."""
        credentials = GoogleCredentials.get_application_default()
        self.api = build('compute', 'v1', credentials=credentials)
        logger.debug('authenticated')

    def get_disk_type_urls(self, name, zone=None):
        """Return a list of disk type urls from the api.

        Filtered by an exact match of supplied name.

        :param name: name of disk type to filter for
        :type name: str
        :param zone: Specify zone of disk type if different from default.
        :type zone: str
        :return: list of urls based on filter
        :rtype: list
        """
        if not zone:
            zone = self.zone
        disk_types = self.api.diskTypes()
        response = disk_types.list(
            project=self.project_id,
            zone=zone,
            filter='name eq {}'.format(name)
        ).execute()

        if 'items' not in response:
            raise Exception("No disk types found with name '{}'".format(name))

        disk_type_urls = []
        for disk_type in response['items']:
            disk_type_urls.append(disk_type['selfLink'])

        return disk_type_urls

    def list_disks(self):
        """List all disks in the project and zone.

        :return: All details regarding all disks.
        :rtype: list of dict
        """
        all_disks = self.api.disks().list(
            project=self.project_id,
            zone=self.zone
        ).execute()
        return all_disks["items"]

    def create_disk(self, name, disk_type="pd-standard", size=None, **kwargs):
        """Create a compute disk object.

        :param name: name of the disk
        :type name: str
        :param disk_type: type of disk. typically one of either pd-standard,
          pd-ssd, local-ssd
        :type disk_type: str
        :param size: size of the disk in GB
          If None, default size is 500GB.
        :type size: long
        :param kwargs: any other specifications as per the disk object
          defined here:
          https://cloud.google.com/compute/docs/reference/latest/disks#resource
        :return: job result message.  'success' when successful.
        :rtype: str
        """
        # Assuming there is only one disk type to use
        type_url = self.get_disk_type_urls(disk_type)[0]
        logger.info('got type url for disk type {}'.format(disk_type))
        logger.debug('type url {}'.format(type_url))

        disk = {
            "kind": "compute#operation",
            "name": name,
            "zone": self.zone,
            "sizeGb": size,
            "type": type_url,
        }

        for key, val in kwargs.items():
            disk[key] = val

        operation = self.api.disks().insert(
            project=self.project_id,
            zone=self.zone,
            body=disk
        ).execute()
        job_result = self.__monitor_zone_operation(operation['name'])
        return job_result

    def delete_disk(self, name):
        """Delete a disk by its name.

        :param name: name of disk to delete
        :type name: str
        :return: outcome of operation
        :rtype: ??
        """
        operation = self.api.disks().delete(
            project=self.project_id,
            zone=self.zone, disk=name
        ).execute()
        job_result = self.__monitor_zone_operation(operation['name'])
        return job_result

    def list_instances(self):
        """List all instances in the given project.

        :return: All instances that exist in project and zone.
        :rtype: list of dict
        """
        result = self.api.instances().list(
            project=self.project_id,
            zone=self.zone
        ).execute()
        return result['items']

    def create_instance(self,
                        name,
                        image=None,
                        scopes=None,
                        startup_script_path=None,
                        machine_type="n1-standard-2"):
        """Create a compute instance.

        :param name: The compute instance name.
        :type name: str
        :param image: The image config.
          If None, then default to ubuntu 16.04.  List of all images:
          https://cloud.google.com/compute/docs/images#os-compute-support
        :type image: dict
        :param scopes: Scopes that the instance has access to.
          If None, then it defaults to all access.
        :type scopes: list of str
        :param startup_script_path: Local path for a startup script.
          If None, then there is no startup script.
        :type startup_script_path: str
        :param machine_type: Type of machine to start up.
        :type machine_type: str
        :return: State of the operation.
        :rtype: str
        """
        if image is None:
            image = {
                'project': "ubuntu-os-cloud",
                'family': 'ubuntu-1604-lts'
            }

        if scopes is None:
            scopes = ['https://www.googleapis.com/auth/cloud-platform']

        # Get the specified image.
        image_response = self.api.images().getFromFamily(
            project=image["project"],
            family=image["family"]
        ).execute()

        source_disk_image = image_response['selfLink']
        machine = "zones/{}/machineTypes/{}".format(self.zone, machine_type)

        config = {
            'name': name,
            'machineType': machine,

            # Specify the boot disk and the image to use as a source.
            'disks': [{
                'boot': True,
                'autoDelete': True,
                'initializeParams': {'sourceImage': source_disk_image}
            }],

            # Specify a network interface with NAT to access public internet
            'networkInterfaces': [{
                'network': 'global/networks/default',
                'accessConfigs': [
                    {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
                ]
            }],

            # Specify what instance will have access to.
            'serviceAccounts': [{
                'email': 'default',
                'scopes': scopes
            }]
        }

        if startup_script_path:
            startup_script = open(startup_script_path, 'r').read()
            config["metadata"] = {
                "items": [{
                    'key': 'startup-script',
                    'value': startup_script
                }]
            }

        operation = self.api.instances().insert(
            project=self.project_id,
            zone=self.zone,
            body=config
        ).execute()

        job_result = self.__monitor_zone_operation(operation['name'])
        return job_result

    def start_instance(self, name):
        """Start a compute engine instance.

        :param name: name of compute instance
        :type name: str
        :return: result of action
        :rtype: str
        """
        logger.info('Starting instance {}'.format(name))
        operation = self.api.instances().start(
            project=self.project_id,
            instance=name,
            zone=self.zone
        ).execute()

        job_result = self.__monitor_zone_operation(operation['name'])
        return job_result

    def stop_instance(self, name):
        """Stop compute engine instance.

        :param name: name of compute instance
        :type name: str
        :return: result of action
        :rtype: str
        """
        logger.info('Stopping instance {}'.format(name))
        operation = self.api.instances().stop(
            project=self.project_id,
            instance=name,
            zone=self.zone
        ).execute()

        job_result = self.__monitor_zone_operation(operation['name'])
        return job_result

    def reset_instance(self, name):
        """Reset a compute engine instance.

        :param name: name of compute instance
        :type name: str
        :return: result of action
        :rtype: str
        """
        logger.info('Resetting instance {}'.format(name))
        operation = self.api.instances().reset(
            project=self.project_id,
            instance=name,
            zone=self.zone
        ).execute()

        job_result = self.__monitor_zone_operation(operation['name'])
        return job_result

    def delete_instance(self, name):
        """Delete compute engine instance.

        :param name: name of compute instance
        :type name: str
        :return: result of action
        :rtype: str
        """
        logger.info('Deleting instance {}'.format(name))
        operation = self.api.instances().delete(
            project=self.project_id,
            instance=name,
            zone=self.zone
        ).execute()

        job_result = self.__monitor_zone_operation(operation['name'])
        return job_result

    def get_zone_operation_status(self, operation_name):
        """Get the status of a zone operation from its name.

        :param operation_name:
        :type operation_name: str
        :return: operation status
        :rtype: ??
        """
        operation = self.api.zoneOperations().get(
            project=self.project_id,
            zone=self.zone,
            operation=operation_name
        ).execute()
        logger.info('operation {} status is {}'.format(
            operation_name,
            operation['status']
        ))

        if 'error' in operation:
            for error in operation['error']['errors']:
                logger.error('{} [{} {}]'.format(
                    error['message'],
                    error['code'],
                    error['location']
                ))
                raise Exception('{} [{} {}]'.format(
                    error['message'],
                    error['code'],
                    error['location']
                ))

        return operation['status']

    def __monitor_zone_operation(self, operation_name):
        """Monitor state of zone operation in loop until status == DONE or ERROR.

        :param operation_name:
        :type operation_name: str
        :return: success or fail
        :rtype: str
        """
        while True:
            status = self.get_zone_operation_status(operation_name)
            logger.info(
                'zone operation is in status {}, '
                'waiting for it to become DONE'.format(status)
            )
            if status == 'DONE':
                logger.info('zone operation complete')
                break
            elif status == 'ERROR':
                logger.error('zone operation {} in error')
                return 'fail'
            time.sleep(10)

        return 'success'

    def get_instance_ip_address(self, name):
        """get the IP address of the VM.

        :param name: name of VM instance
        :type name: str
        :return: str Name of VM
        :rtype: str
        """
        d_response = self.api.instances().get(
            project=self.project_id,
            zone=self.zone,
            instance=name
        ).execute()

        return d_response['networkInterfaces'][0]['accessConfigs'][0]['natIP']
