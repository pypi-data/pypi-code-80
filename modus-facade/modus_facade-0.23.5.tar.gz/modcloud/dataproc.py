"""Functions for working with google dataproc.

Installs:
    pip install google-api-python-client
"""
import logging
import os
import time
import uuid

from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from modcloud import Storage

logger = logging.getLogger(__name__)


class DataProc(object):
    """Manage interactions with dataproc."""

    def __init__(self, project_id, zone='europe-west1-d', region='global'):
        """Facade Module to work with Google Cloud Dataproc.

        Includes ability to spin up, shut down and scale clusters

        :param project_id: Google Cloud Project ID where dataproc cluster
          actions will take place
        :type project_id: str
        :param zone: Zone where Dataproc cluster is located or should be
          located. E.g europe-west1-d
        :type zone: str
        :param region: region where dataproc commands should be executed.
          this defaults to global as per v1 API spec
        :type region: str
        :return: None
        """
        self.project_id = project_id
        self.zone = zone
        self.region = region
        self.zone_uri = '{}/projects/{}/zones/{}'.format(
            "https://www.googleapis.com/compute/v1",
            project_id,
            zone
        )

        self.build_service()
        logger.debug('DataProc init...')

    def build_service(self):
        """Using the Google Credentials service, builds service access.

        :return: None
        """
        logger.debug('DataProc:buildService...')
        credentials = GoogleCredentials.get_application_default()
        self.api = build('dataproc', 'v1', credentials=credentials)
        logger.info('Datproc:buildService acquired')

    def create_cluster(self,
                       cluster_name,
                       master_type='n1-standard-4',
                       worker_type='n1-standard-2',
                       number_workers=2,
                       preemtible_cluster=False,
                       executable_file_uri=None,
                       execution_timeout='600s',
                       tags=None,
                       scopes=None,
                       image_version='1.2'):
        """Create dataproc cluster.

        Example usage:
          create_cluster(
            "my-cluster-name",
            master_type='n1-standard-4',
            worker_type='n1-standard-2',
            number_workers=3,
            execution_timeout="1800s",
            executable_file_uri='gs://{}/{}/taxi_dataproc_init.sh'.format(
                UPLOAD_BUCKET, upload_location
            ),
            scopes=[
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/bigtable.admin.table",
                "https://www.googleapis.com/auth/bigtable.data",
                "https://www.googleapis.com/auth/devstorage.full_control",
                "https://www.googleapis.com/auth/datastore"
            ]
        )

        :param cluster_name: name of the cluster to be created
        :type cluster_name: str
        :param master_type: machine type for master.
          May be found with gcloud commmand `gcloud compute machine-types list`
        :type master_type: str
        :param worker_type: machine type for worker.
          May be found with gcloud commmand `gcloud compute machine-types list`
        :type worker_type: str
        :param number_workers: number of worker machines in the cluster
        :type number_workers: int
        :param preemtible_cluster: is the cluster preemtible
        :type preemtible_cluster: bool
        :param executable_file_uri: google storage uri for startup shell script
          Will be executed on master and workers
        :type executable_file_uri: str
        :param execution_timeout: length time in seconds available for cluster
          to execute initialisation script.
          default is 600 seconds
        :type execution_timeout: str
        :param tags: list of tags to be applied to all nodes in cluster
        :type tags: list
        :param scopes: list of compute access scopes
        :type scopes: list
        :param image_version: image version if the cluster
        :type image_version: str
        :return: cluster response object
        :rtype: dict
        """
        logger.info('Configuring cluster "{}"'.format(cluster_name))

        gce_cluster_config = {
            "zoneUri": self.zone_uri,
            "serviceAccountScopes": scopes,
            "tags": tags,
        }

        if executable_file_uri:
            logger.debug('URI of startup executable file: {}'.format(
                executable_file_uri
            ))
            initialization_actions = {
                "executableFile": executable_file_uri,
                "executionTimeout": execution_timeout,
            }
        else:
            initialization_actions = None

        master_config = self.define_instance_group(
            instance_type=master_type,
            preemtible=preemtible_cluster
        )
        worker_config = self.define_instance_group(
            number_instances=number_workers,
            instance_type=worker_type,
            preemtible=preemtible_cluster
        )

        cluster_config = {
            "projectId": self.project_id,
            "clusterName": cluster_name,
            "config": {
                "gceClusterConfig": gce_cluster_config,
                "masterConfig": master_config,
                "workerConfig": worker_config,
                "softwareConfig": {
                    "imageVersion": image_version
                },
                "initializationActions": [
                    [
                        initialization_actions
                    ]
                ],
            }
        }

        logger.debug('Cluster Configured with: {}'.format(cluster_config))

        logger.info('Creating cluster {}'.format(cluster_name))
        response = self.api.projects().regions().clusters().create(
            projectId=self.project_id,
            region=self.region, body=cluster_config
        ).execute()

        logger.debug(
            'Cluster create command accepted with response {}'.format(response)
        )

        # Wait for the cluster to become ready
        while True:
            status, status_time = self.get_cluster_status(cluster_name)
            logger.info(
                'Cluster state is {}, '
                'waiting for it to become RUNNING'.format(status)
            )

            if status == 'RUNNING':
                logger.info(
                    'Cluster has become RUNNING at {}'.format(status_time)
                )
                break
            assert (status != 'ERROR'), \
                "Creating cluster {} has returned error".format(cluster_name)
            time.sleep(10)

        response = self.api.projects().regions().clusters().get(
            projectId=self.project_id,
            region=self.region,
            clusterName=cluster_name
        ).execute()
        return response

    def define_instance_group(self,
                              number_instances=1,
                              instance_type='n1-standard-2',
                              preemtible=False,
                              disk_size=100,
                              local_ssd=0):
        """Define an instance group config object.

         Used as definitions  of the master and workers instances.

        :param number_instances: number of instances in the instance group
        :type number_instances: int
        :param instance_type: type of instances in the instances
        :type instance_type: str
        :param preemtible: should these VMs pre preemtible
          (i.e die after 24hrs)
        :type preemtible: bool
        :param disk_size: size of the disks in the cluster. default is 100
        :type disk_size: int
        :param local_ssd: number of local ssds attached for HDFS data.
          default is 0
        :type local_ssd: int
        :return: instance_group_config object
        :rtype: dict
        """
        logger.debug('instance group configured with params:')
        logger.debug('number of instances: {}'.format(number_instances))
        logger.debug('instance type: {}'.format(instance_type))
        logger.debug('preemtible: {}'.format(preemtible))
        intance_group_config = {
            "numInstances": number_instances,
            "machineTypeUri": (
                'https://www.googleapis.com/compute/v1/projects/'
                '{project_id}/zones/{zone}/machineTypes/'
                '{instance_type}'.format(
                    project_id=self.project_id,
                    zone=self.zone,
                    instance_type=instance_type
                )
            ),
            "isPreemptible": preemtible,
            "diskConfig": {
                "bootDiskSizeGb": disk_size,
                "numLocalSsds": local_ssd,
            }
        }

        return intance_group_config

    def get_cluster_status(self, cluster_name):
        """Get cluster status.

        :param cluster_name: name of cluster for which we are looking up status
        :type cluster_name: str
        :return: status, status_time
        :rtype: tuple
        """
        status = self.api.projects().regions().clusters().get(
            projectId=self.project_id,
            region=self.region,
            clusterName=cluster_name,
            fields='status'
        ).execute()

        return status['status']['state'], status['status']['stateStartTime']

    def delete_cluster(self, cluster_name):
        """Delete a cluster based on its name.

        :param cluster_name: name of cluster for which we trying to delete
        :type cluster_name: str
        :return: success string if successful else error message
        :rtype: str
        """
        self.api.projects().regions().clusters().delete(
            projectId=self.project_id,
            region=self.region,
            clusterName=cluster_name
        ).execute()

        # Wait for the cluster to be deleted
        while True:
            try:
                status, status_time = self.get_cluster_status(cluster_name)
                logger.info(
                    'Cluster state is {}, waiting for process to complete '
                    'and return 404'.format(status)
                )
                time.sleep(10)
            except HttpError as e:
                # Exceptional Case. We are passing the exception because,
                #   eventually, the 404 error is what we want
                if e.resp['status'] == '404':
                    logger.info(
                        'Cluster {} no longer found. Assuming its '
                        'deleted'.format(cluster_name)
                    )
                else:
                    logger.error(
                        'Delete instruction on API failing '
                        'with error {}'.format(e)
                    )
            except Exception as e:
                logger.error('Cluster status lookup failed with {}'.format(e))

            break

        return 'success'

    def resize_cluster(self,
                       cluster_name,
                       primary_workers=None,
                       secondary_workers=None):
        """Resize a dataproc cluster to the size provided.

        That is, the number of nodes will increase or decrease to
        the new cluster size(s) provided.

        :param cluster_name: name of the cluster to resize
        :type cluster_name: str
        :param primary_workers: number of primary workers the
          cluster will resize to
        :type primary_workers: int
        :param secondary_workers: number of secondary workers the
          cluster will resize to
        :type secondary_workers: int
        :return: cluster response object
        :rtype: dict
        """
        if primary_workers and not secondary_workers:
            worker_config = {"numInstances": primary_workers}
            secondary_worker_config = None
            update_mask = 'config.worker_config.num_instances'
        elif secondary_workers and not primary_workers:
            worker_config = None
            secondary_worker_config = {"numInstances": secondary_workers}
            update_mask = 'config.secondary_worker_config.num_instances'
        elif primary_workers and secondary_workers:
            worker_config = {"numInstances": primary_workers}
            secondary_worker_config = {"numInstances": secondary_workers}
            update_mask = 'config.worker_config.num_instances,config.' \
                          'secondary_worker_config.num_instances'
        else:
            logger.exception(
                'Both number of workers and number of '
                'secondary workers are none'
            )
            raise Exception(
                'Both number of workers and number of '
                'secondary workers are none'
            )

        cluster_config = {
            "projectId": self.project_id,
            "clusterName": cluster_name,
            "config": {
                "workerConfig": worker_config,
                "secondaryWorkerConfig": secondary_worker_config,
            }
        }

        logger.debug('Cluster Configured with: {}'.format(cluster_config))

        response = self.api.projects().regions().clusters().patch(
            projectId=self.project_id,
            region=self.region,
            clusterName=cluster_name,
            body=cluster_config,
            updateMask=update_mask
        ).execute()

        logger.info(
            'Cluster create command accepted with response {}'.format(response)
        )

        # Wait for the cluster to become ready
        while True:
            status, status_time = self.get_cluster_status(cluster_name)
            logger.info(
                'Cluster state is {}, '
                'waiting for it to become RUNNING'.format(status)
            )

            if status == 'RUNNING':
                logger.info(
                    'Cluster has become RUNNING at {}'.format(status_time)
                )
                break
            assert (status != 'ERROR'), \
                "Resize cluster {} has returned status error".format(
                    cluster_name
                )
            time.sleep(10)

        response = self.api.projects().regions().clusters().get(
            projectId=self.project_id,
            region=self.region,
            clusterName=cluster_name
        ).execute()

        return response

    def submit_pyspark_job(self,
                           cluster_name,
                           main_pyspark_file,
                           args=None,
                           python_files=None,
                           jar_files=None,
                           misc_files=None,
                           archives=None):
        """Submit a PySpark job to a dataproc cluster.

        Uploads files to clusters cloud storage bucket and ensures that
          bucket is cleared of old object.

        PROCESS:
            Dataproc does not upload files or accept files directly. Rather,
              we need to upload the files manually to
            Cloud Storage and then provide the Dataproc job with the URIs of
              the files in questions
            There are a number of file contexts we need to cater for:
            1 - The main pyspark executor file
            2 - Supporting python files
            3 - Compiled JARs to be exected by the driver
            4 - Misc files (eg CSVs) that support the job
            5 - Archive files for extraction

            See the Google Docs re the Dataproc REST API for more info on how
              these files are consumed by the Dataproc job

            The process, however, is as follows. First, we need to upload the
              files to Cloud Storage and then supply the
            URIs to the job configuration.
            By way of example, we use os.path.split(main_pyspark_file)[1] to
              get ONLY the filename for creation of the URI

            In this context, we use the following parts to create a
              reference URI:
            - gs:// : this is the static protocol prefix used for all
              cloud storage URIs
            - config_bucket: each cloud project has a storage bucket
              automatically created in the project that we can
               use for "stuff". This forms the base part of the uri
            - job_storage_path is common sub-dir for files used for this
              cluster + job combo
            - supporting file sub dir: if we're uploading supporting files,
              we chuck them in a subdir
            - filename: from the filepath, we extract the filename. this is
              the last part of the URI

        :param cluster_name: cluster where job will be executed
        :type cluster_name: str
        :param main_pyspark_file: the main pyspark python file to be exectuted
        :type main_pyspark_file: str
        :param args: a list of arguments to be passed to the main pyspark file
        :type args: list of str or None
        :param python_files:n list of python files to upload and pass to
          the PySpark framework
        :type python_files: list of str or None
        :param jar_files: list of jar files to upload and add to CLASSPATH
          of the Python driver
        :type jar_files: list of str or None
        :param misc_files: list of any files to be uploaded and stored in
          the working directory.
        Useful for naively parallel tasks.
        :type misc_files: list of str or None
        :param archives: list of archives files to be uploaded and extracted
          in the working directory
        :type archives: list of str or None
        :return: job submit response
        :rtype: dict
        """
        # Get config of cluster and thus config bucket Id
        config = self.api.projects().regions().clusters().get(
            projectId=self.project_id,
            region=self.region,
            clusterName=cluster_name,
            fields='config'
        ).execute()

        config_bucket = config['config']['configBucket']
        logger.debug('cluster config bucket: {}'.format(config_bucket))

        # Setup the job id.
        job_id = str(uuid.uuid4())
        logger.debug('job id set to generated uuid {}'.format(job_id))

        job_storage_path = "{}/{}".format(cluster_name, job_id)
        logger.debug('set job storage path as {}'.format(job_storage_path))

        # Upload the PySpark files.
        bucket = Storage()
        logger.info('clearing file in folder {}'.format(job_storage_path))
        bucket.clear_bucket(config_bucket, job_storage_path)

        logger.info('uploading files to gs://{}/{}'.format(
            config_bucket,
            job_storage_path)
        )

        logger.debug(
            "uploading main pyspark file from '{}' to "
            "bucket '{}' and path '{}'".format(
                main_pyspark_file,
                config_bucket,
                job_storage_path
            )
        )
        bucket.upload_object(
            main_pyspark_file,
            config_bucket,
            job_storage_path
        )
        main_file_uri = (
            'gs://' + config_bucket + '/' +
            job_storage_path + '/' +
            os.path.split(main_pyspark_file)[1]
        )
        logger.debug('main file uri configured as {}'.format(main_file_uri))

        python_file_uris = self.upload_files(
            bucket, config_bucket, job_storage_path,
            python_files, 'python_files', ('.py', '.egg', '.zip')
        )
        jar_file_uris = self.upload_files(
            bucket, config_bucket, job_storage_path,
            jar_files, 'jar_files', '.jar'
        )
        files_uris = self.upload_files(
            bucket, config_bucket, job_storage_path,
            misc_files, 'misc_files', None
        )
        archive_uris = self.upload_files(
            bucket, config_bucket, job_storage_path,
            archives, 'archive_files', ('.jar', '.tar', '.tar.gz', '.zip')
        )

        # Configure and submit job
        if not args:
            args = []

        job_config = {
            "job": {
                "reference": {
                    "projectId": self.project_id,
                    "jobId": job_id,
                },
                "placement": {
                    "clusterName": cluster_name,
                },
                "pysparkJob": {
                    "mainPythonFileUri": main_file_uri,
                    'args': args,
                    "pythonFileUris": python_file_uris,
                    "jarFileUris": jar_file_uris,
                    "fileUris": files_uris,
                    "archiveUris": archive_uris,
                },
            }
        }

        logger.info('submitting job to cluster {} with id {}'.format(
            cluster_name,
            job_id
        ))
        logger.debug('job config: {}'.format(job_config))

        response = self.api.projects().regions().jobs().submit(
            projectId=self.project_id,
            region=self.region,
            body=job_config
        ).execute()

        return response

    @staticmethod
    def upload_files(bucket,
                     config_bucket,
                     job_storage_path,
                     files,
                     storage_dir,
                     supported_types):
        """Upload files to storage.

        :param bucket: Storage bucket object.
        :type bucket: Storage
        :param config_bucket: Bucket name obtained from getting cluster config.
        :type config_bucket: str
        :param job_storage_path: Storage location in bucket.
        :type job_storage_path: str
        :param files: List of filenames that need to be copied over.
        :type files: list of str
        :param storage_dir: Name of storage directory 'folder'
        :type storage_dir: str
        :param supported_types: Accepted file types.  None for all.
        :type supported_types: tuple of str or str or None
        :return: List of uris to upload to.
        :rtype: list of str
        """
        file_uris = []
        if files:
            for fname in files:
                if supported_types and not fname.endswith(supported_types):
                    err = "filetype '{}' not supported. Pick from {}".format(
                        fname, supported_types
                    )
                    logger.exception(err)
                    raise Exception(err)
                bucket.upload_object(
                    fname,
                    config_bucket,
                    "{}/{}".format(job_storage_path, storage_dir)
                )
                fname = os.path.split(fname)[1]
                uri = (
                    "gs://{}/{}/{}/{}".format(
                        config_bucket, job_storage_path, storage_dir, fname
                    )
                )
                logger.debug("uploading file '{}' to '{}'".format(fname, uri))
                file_uris.append(uri)
        return file_uris

    def get_job_status(self, job_id):
        """Get status of job by ID.

        :param job_id: id of job we are querying
        :type job_id: str
        :return: status, status_time
        :rtype: tuple
        """
        status = self.api.projects().regions().jobs().get(
            projectId=self.project_id,
            region=self.region, jobId=job_id,
            fields='status'
        ).execute()

        return status['status']['state'], status['status']['stateStartTime']

    def monitor_job(self, job_id):
        """Monitor a running job until it either succeeds or fails.

        :param job_id:
        :type job_id: str
        :return: status and status_time
        :rtype: tuple
        """
        # Wait for the cluster to become ready
        while True:
            status, status_time = self.get_job_status(job_id)
            logger.info(
                'Job state is {}, waiting for it to become DONE'.format(status)
            )
            if status == 'DONE':
                logger.info('Job has finished at {}'.format(status_time))
                break
            assert (status != 'ERROR'), "Job {} has returned error".format(
                job_id)
            time.sleep(10)

        # noinspection PyUnboundLocalVariable
        return status, status_time
