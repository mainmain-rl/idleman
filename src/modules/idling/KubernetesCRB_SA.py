
from modules.common.Logging import ErrorManager
from modules.ResponseModel.ResponseModel import ResponseModel
from modules.idling.KubernetesConfig import KubernetesConfig
from modules.idling.KubernetesNamespaceSecurity import KubernetesNamespaceSecurity
from modules.idling.ClusterRoleBindingModelJson import ClusterRoleBindingModelJson
from modules.idling.ServiceAccountModelJson import ServiceAccountModelJson
from kubernetes.client import ApiException

class KubernetesCRBSA(KubernetesConfig):
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
        
    def workflow_RBAC_SA(self,namespace: str):
        """Create service account & cluster role binding resources for a namespace

        Args:
            namespace (str): _description_

        Returns:
            _type_: _description_
        """
        if not self.check_namespace_list(namespace):
            return ResponseModel(f"Not Authorized on namespace {namespace}","failed")
        
        ServiceAccountName = f'{namespace}-idling-sa'
        RbacName = f'{namespace}-idling-rbac'
        ServiceAccountBody = ServiceAccountModelJson(
                namespace, 
                ServiceAccountName)
        try:
            self._coreV1Api.create_namespaced_service_account(namespace,ServiceAccountBody)
        except ApiException as e:
            if e.status not in [409, 200]:
                self.__logger.log_error(e)
                return ResponseModel(e,"failed")
        except Exception as e:
            self.__logger.log_error(e)
            return ResponseModel(e,"failed")

        RoleBindingBody = ClusterRoleBindingModelJson(
            namespace, 
            RbacName,
            ServiceAccountName)
        try:
            self._rbacAuthV1Api.create_cluster_role_binding(RoleBindingBody)
            return ResponseModel("ServiceAccount & RoleBinding ok","success")
        except ApiException as e:
            if e.status in [409, 200]:
                return ResponseModel("ServiceAccount & RoleBinding ok","success")
            self.__logger.log_error(e)
            return ResponseModel(e,"failed")
        except Exception as e:
            self.__logger.log_error(e)
            return ResponseModel(e,"failed")
        
        
        
    
    