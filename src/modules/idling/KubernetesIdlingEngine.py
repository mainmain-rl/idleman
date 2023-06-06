
import os, sys, json
from kubernetes.client import ApiException
from modules.common.Logging import ErrorManager
from modules.ResponseModel.ResponseModel import ResponseModel
from modules.idling.CronJobModelJson import CronJobModelJson
from modules.idling.KubernetesConfig import KubernetesConfig
from modules.idling.KubernetesNamespaceSecurity import KubernetesNamespaceSecurity
from modules.idling.KubernetesCallMethod import KubernetesCallMethod

class KubernetesIdlingEngine(KubernetesConfig):
    """This class is about the management of resources inside a Kubernetes cluster."""

    def __init__(self):
        """Init of the class, load k8s conf and setup client api.
        """
        # Set super class
        super().__init__()
        
        # Setup logger  
        self.__logger = ErrorManager("INFO",__name__)
        
        # KubernetesNamespaceSecurity class
        self.__kubernetes_namespace_security = KubernetesNamespaceSecurity()
        self.check_namespace_list = self.__kubernetes_namespace_security.check_namespace_list
        
        # KubernetesCallMethod class
        self.__kubernetes_call_method = KubernetesCallMethod()
        self.check_cronjob_exists = self.__kubernetes_call_method.check_cronjob_exists
        self.create_namespaced_cron_job = self.__kubernetes_call_method.create_namespaced_cron_job
        self.patch_namespaced_cron_job = self.__kubernetes_call_method.patch_namespaced_cron_job
        
        # ENV
        try:
            self._IMAGE = os.environ['IMAGE']
        except KeyError as e:
            self.__logger.error(f"KeyError: {e} env variable missing")
            sys.exit()
    
    def cronjob_idling_workflow(
        self,
        namespace: str, 
        name: str, 
        starting_schedule: str,
        stopping_schedule : str,
        replicas: str
        ):
        # Check NamespaceSecurity
        if not self.check_namespace_list(namespace):
            return ResponseModel(f"Not Authorized on namespace {namespace}","failed")
        
        # Building json
        myJsonList = [
            {
                "idlingName": f"{name}-idling-resume",
                "action": "START",
                "schedule": starting_schedule,
                "replicas": replicas,
            },
            {
                "idlingName": f"{name}-idling-pause",
                "action": "STOP",
                "schedule": stopping_schedule,
                "replicas": "0",
            }
        ]
        for item in myJsonList:
            item["body"] = CronJobModelJson(
                namespace,
                name,
                item.get("idlingName"),
                item.get("action"),
                self._IMAGE,
                item.get("schedule"),
                f'{namespace}-idling-sa',
                item.get("replicas")
                )
        
        try:
            for item in myJsonList:
                if not self.check_cronjob_exists(namespace,item.get("idlingName")):
                    self.create_namespaced_cron_job(namespace,item.get("body"))
                    
                
                patch_body = {
                    "metadata":{
                        "name":item.get("idlingName")
                        },
                    "spec":{
                        "cronSpec": item.get("schedule")
                        }
                    }
                self.patch_namespaced_cron_job(namespace,patch_body)
            return ResponseModel(f'cronjobs {[item.get("idlingName") for item in myJsonList]} has been created',"success")
        except ApiException as e:
            self.__logger.log_error(e)
            return ResponseModel(e,"failed")
        except Exception as e:
            self.__logger.handle_exception(e)
            return ResponseModel(e,"failed")