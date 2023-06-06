import os, json, sys
from modules.common.Logging import ErrorManager
from modules.ResponseModel.ResponseModel import ResponseModel
from modules.idling.KubernetesConfig import KubernetesConfig
from modules.idling.KubernetesNamespaceSecurity import KubernetesNamespaceSecurity

class KubernetesCallMethod(KubernetesConfig):
    """This class is about the management of resources inside a Kubernetes cluster."""

    def __init__(self):
        """Init of the class, load k8s conf and setup client api.
        """
        # Init super class
        super().__init__() 
        
        # Setup logging
        self.__logger = ErrorManager("INFO",__name__)
        
        # ENV
        try:
            self._IMAGE = os.environ['IMAGE']
            self._SERVICE_ACCOUNT = os.environ["SERVICE_ACCOUNT"]
        except KeyError as e:
            self.__logger.error(f"KeyError: {e} env variable missing")
            sys.exit()
        
        # KubernetesNamespaceSecurity class
        self.__kubernetes_namespace_security = KubernetesNamespaceSecurity()
        self.check_namespace_list = self.__kubernetes_namespace_security.check_namespace_list
    def get_namespaces(self):
        """Get all namespace.

        Returns:
            dict: json call response
        """
        try:
            namespaces = self._coreV1Api.list_namespace()
            message = {"namespaces": self.check_namespace_list([ns.metadata.name for ns in namespaces.items])}
            return ResponseModel(message,"success")
        except Exception as e:
            return ResponseModel(e,"failed")
    
    def get_deployments(
        self,
        namespace: str = 'default'
        ):
        """Get deployments in namespace.

        Args:
            namespace (str, optional): namespace for filtering. Defaults to 'default'.

        Returns:
            dict: Json response.
        """
        if not self.check_namespace_list(namespace):
            return ResponseModel(f"Not Authorized on namespace {namespace}","failed")
        try:
            deployments = self._appsV1Api.list_namespaced_deployment(namespace)
            message = {"deployments": [dep.metadata.name for dep in deployments.items]}
            return ResponseModel(message,"success")
        except Exception as e:
            return ResponseModel(e,"failed")
    
    def get_deployment(
        self,
        namespace: str, 
        deployment: str
        ):
        """Get a specific deployment.

        Args:
            namespace (str): namespace for filter.
            deployment (str): concerned deployment.

        Returns:
            dict: response call api json.
        """
        if not self.check_namespace_list(namespace):
            return ResponseModel(f"Not Authorized on namespace {namespace}","failed")
        try:
            deploy = self._appsV1Api.read_namespaced_deployment(
                deployment,
                namespace,
                _preload_content=False)
            return ResponseModel(json.loads(deploy.data),"success")
        except Exception as e:
            return ResponseModel(e,"failed")
    
    def get_cronjobs(
        self,
        namespace: str = 'default'
        ):
        """Get cronjobs in namespace

        Args:
            namespace (str, optional): namespace for filtering. Defaults to 'default'.

        Returns:
            dict: Json response.
        """
        if not self.check_namespace_list(namespace):
            return ResponseModel(f"Not Authorized on namespace {namespace}","failed")
        try:
            cronjobs = self._batchV1Api.list_namespaced_cron_job(namespace)
            message = {"cronjobs": [cronjob.metadata.name for cronjob in cronjobs.items]}
            print(__name__, "your are in the get_cronjobs method",message)
            return ResponseModel(message,"success")
        except Exception as e:
            return ResponseModel(e,"failed")
    
    def get_cronjob(
        self,
        namespace: str, 
        cronjob: str
        ):
        """Get a specific cronjob.

        Args:
            namespace (str): namespace for filter.
            cronjob (str): concerned cronjob.

        Returns:
            dict: response call api json.
        """
        if not self.check_namespace_list(namespace):
            return ResponseModel(f"Not Authorized on namespace {namespace}","failed")
        try:
            print(__name__, "your are in the get_cronjob method")
            cron = self._batchV1Api.read_namespaced_cron_job(
                cronjob,
                namespace,
                _preload_content=False)
            cronjob_values = json.loads(cron.data)
            print(__name__, "your are in the get_cronjob method",cronjob_values)
            # json_body = {
            #     "uid": cronjob_values.get("metadata").get("uid"),
            #     "creationTimestamp": cronjob_values.get("metadata").get("creationTimestamp"),
            #     "name": cronjob_values.get("metadata").get("name"),
            #     "namespace": cronjob_values.get("metadata").get("namespace"),
            #     "schedule": cronjob_values.get("spec").get("schedule"),
            # }
            
            return ResponseModel(cronjob_values,"success")
        except Exception as e:
            return ResponseModel(e,"failed")
    
    def check_cronjob_exists(
        self,
        namespace: str, 
        name: str
        ):
        """Check if cronjob already exist.

        Args:
            namespace (str): Namespace for filtering.
            name (str): cronjob's name to check.

        Returns:
            bool: True if exist, False if not.
        """
        cron_job_list = self.get_cronjobs(namespace)
        return any(name == cron_job for cron_job in cron_job_list.message.get('cronjobs'))
    
    def create_namespaced_cron_job(
        self,
        namespace: str = 'default', 
        body: dict = None
        ):
        """Create a namespaced cronjob.

        Args:
            namespace (str, optional): namespace where create the cronjob. Defaults to 'default'.
            body (dict): cronjob will be created with this body, it's mandatory.

        Returns:
            dict: json body response.
        """
        if not self.check_namespace_list(namespace):
            return ResponseModel(f"Not Authorized on namespace {namespace}","failed")
        if body is None or not isinstance(body, dict):
            return ResponseModel('body is required as dict!', 'failed')
        try:
            print(f'{namespace}: Voilà le putain de body: {body}')
            ret = self._batchV1Api.create_namespaced_cron_job(namespace=namespace, body=body, 
                pretty=True,
                _preload_content=False, 
                async_req=False
                )
            ret_dict = json.loads(ret.data)
            return ResponseModel({json.dumps(ret_dict)},'success')
        except Exception as e:
            self.__logger.log_error(e)
            return ResponseModel(str(e),'failed')

    def delete_namespaced_cron_job(
        self,
        namespace: str = 'default', 
        name: str = None
        ):
        if not self.check_namespace_list(namespace):
            return ResponseModel(f"Not Authorized on namespace {namespace}","failed")
        if name is None:
            return ResponseModel('name is required!', 'failed')
        if not self.check_cronjob_exists(namespace, name):
            return ResponseModel(f"{name} doesn't exists",'failed')
        ret = self._batchV1Api.delete_namespaced_cron_job(
            name=name, 
            namespace=namespace,
            preload_content=False, 
            async_req=False
            )
        ret_dict = json.loads(ret.data)
        return ResponseModel({json.dumps(ret_dict)},'success')

    def patch_namespaced_cron_job(
        self,
        namespace='default', 
        body=None
        ):
        if not self.check_namespace_list(namespace):
            return ResponseModel(f"Not Authorized on namespace {namespace}","failed")
        if body is None or not isinstance(body, dict):
            self.__logger.log_error(type(body))
            return ResponseModel('body is required as dict!', 'failed')
        try:
            name = body['metadata']['name']
            ret = self._batchV1Api.patch_namespaced_cron_job(
                name=name, 
                namespace=namespace, 
                body=body,
                _preload_content=False, 
                async_req=False
                )
            ret_dict = json.loads(ret.data)
            return ResponseModel({json.dumps(ret_dict)},'success')
        except Exception as e:
            return ResponseModel(str(e),'failed')
