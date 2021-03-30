from kubernetes import client, config
from kubernetes.client import AppsV1Api, V1Deployment, CoreV1Api

class KubernetesClientFactory:
    @staticmethod
    def create_core(k8config_path: str) -> CoreV1Api:
        config.load_kube_config(k8config_path)
        configuration = client.Configuration()
        configuration.verify_ssl = False
        configuration.ssl_ca_cert = None
        kubernetes_client = client.CoreV1Api()
        kubernetes_client.api_client.configuration = configuration
        return kubernetes_client

    @staticmethod
    def create(k8config_path: str) -> AppsV1Api:
        config.load_kube_config(k8config_path)
        configuration = client.Configuration()
        configuration.verify_ssl = False
        configuration.ssl_ca_cert = None
        kubernetes_client = client.AppsV1Api()
        kubernetes_client.api_client.configuration = configuration
        return kubernetes_client