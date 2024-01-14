from kubernetes import config, client
from modules.common.Logging import ErrorManager
import os

class KubernetesConfig:
    """This class is about kubernetes client Api configuration."""

    def __init__(self):
        """Init of the Super Class, load k8s conf and setup client api."""
        # Setup logging
        self.__logger = ErrorManager("INFO",__name__)
        # Kube auth & api.
        try:
            config.load_incluster_config() if os.getenv('KUBERNETES_SERVICE_HOST') else config.load_kube_config()
            self._apiClient = client.ApiClient()
            self._appsV1Api = client.AppsV1Api()
            self._coreV1Api = client.CoreV1Api()
            self._batchV1Api = client.BatchV1Api()
            self._rbacAuthV1Api = client.RbacAuthorizationV1Api()
        except Exception as e:
            self.__logger.handle_critical(e)