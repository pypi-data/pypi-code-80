"""Communicate with Seaweed NFS to PUT and GET files from it."""
import logging
import requests
import os

logger = logging.getLogger(__name__)


class Weed(object):
    """Handle operations with Seaweed."""

    def __init__(self, host, port="9333"):
        """Initialize and set the master node.

        :param host: Hostname for seaweed master node
        :type host: str
        :param port: Port for seaweed master node
        :type port: str
        """
        self.master_node = "{}:{}".format(host, port)

    def get_file(self, fid):
        """Get file from seeweed via file id.

        bytes from returned can be saved with:
            with open(path, 'wb') as f:
                f.write(file_content)

        :param fid: file id
        :type fid: str
        :return: Dict containint file content stored in seeweed.
        :rtype: dict
        """
        # first enter volume ID to master and get URL ()
        # http://sw-node-0.seaweed:9333/dir/lookup?volumeId=7
        volume_id = fid.split(',')[0]
        logger.info("getting worker node name for fid='{}'...".format(fid))
        master_url = "http://{}/dir/lookup?volumeId={}".format(
            self.master_node,
            volume_id
        )
        logger.info("master_url = '{}'".format(master_url))

        resp = requests.get(master_url)
        resp_dict = resp.json()

        logger.info(resp_dict)

        node_url = resp_dict['locations'][0]['url']
        logger.info("node_urls = '{}'".format(node_url))

        # then get file
        # http://sw-node-0.seaweed:8080/7,03b24c856e
        file_url = "http://{}/{}".format(node_url, fid)
        logger.info("getting from '{}'".format(file_url))
        file_resp = requests.get(file_url)

        filename = str(
            file_resp
            .headers['Content-Disposition']
            .split('filename=')[1]
            .replace('"', '')
        )

        resp = {
            'content': file_resp.content,
            'filename': filename,
            'fid': fid
        }

        return resp

    def put_file(self, file_obj):
        """PUT the file object into the Seaweed persistant file system.

        https://github.com/chrislusf/seaweedfs

        :param file_obj: File object to push into Seaweed
        :type file_obj: file
        :return: All info relating to the file uploaded to seaweed
        :rtype: dict
        """
        # find out from master file location id
        # http://sw-node-0.seaweed:9333/dir/assign
        logger.info("getting fid and node name...")
        master_url = "http://{}/dir/assign".format(self.master_node)
        logger.info("master_url = '{}'".format(master_url))

        resp = requests.put(master_url)
        resp_dict = resp.json()

        fid = resp_dict['fid']
        node_url = resp_dict['url']

        logger.info("fid = '{}'; node_url = '{}'".format(fid, node_url))

        # Then put file to location provided
        # http://sw-node-0.seaweed:8080/7,03b24c856e
        put_url = "http://{}/{}".format(node_url, fid)
        logger.info("put_url = '{}'".format(put_url))

        logger.info("putting file into seaweed...")

        filename = os.path.basename(file_obj.name)
        sea_resp = requests.put(
            put_url,
            files={filename: file_obj}
        )

        logger.info("Status code: '{}'".format(sea_resp.status_code))

        ret = {
            'status_code': sea_resp.status_code,
            'fid': fid,
            'name': sea_resp.json()['name'],
            'size': sea_resp.json()['size'],
        }

        return ret
