from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from modules.common.Logging import ErrorManager
from modules.idling.KubernetesCallMethod import KubernetesCallMethod
from modules.idling.KubernetesIdlingEngine import KubernetesIdlingEngine
from modules.idling.KubernetesCRB_SA import KubernetesCRBSA
from .BaseModel import CronJobPostBaseModel
import os, json

# Setup logging
logger = ErrorManager(
    log_level = os.getenv('DEBUG') if os.getenv('DEBUG') else "INFO",
    name = __name__
    )

router = APIRouter()
Kubernetes_Call_Method = KubernetesCallMethod()
Kubernetes_Idling_Engine = KubernetesIdlingEngine()
Kubernetes_CRB_SA = KubernetesCRBSA()

@router.get("/")
def read_root(
    request: Request
    ):
    ForwardUrl = "/docs#/"
    message = {
        "clientIp":request.client.host,
        "ClientPort":request.client.port,
        "action": {
            "type":"redirect",
            "OriginUrl":request.url,
            "ForwardUrl": ForwardUrl
        }
    }
    logger.log_info(message)
    return RedirectResponse(url=ForwardUrl)

@router.get("/namespaces")
def get_namespace(
    request: Request
    ):
    return Kubernetes_Call_Method.get_namespaces()

@router.post("/namespaces/{namespace}/setup")
def post_namespace_setup(
    namespace: str,
    request: Request
    ):
    return Kubernetes_CRB_SA.workflow_RBAC_SA(namespace)

@router.get("/namespaces/{namespace}/deployments")
def get_deployments(
    namespace: str,
    request: Request,
    ):
    return Kubernetes_Call_Method.get_deployments(namespace)

@router.get("/namespaces/{namespace}/deployments/{deployment}")
def get_namespaced_deployment(
    namespace: str,
    deployment: str, 
    request: Request
    ):
    return Kubernetes_Call_Method.get_deployment(namespace,deployment)

@router.get("/namespaces/{namespace}/cronjobs")
def get_cronjobs(
    namespace: str,
    request: Request,
    ):
    return Kubernetes_Call_Method.get_cronjobs(namespace)

@router.get("/namespaces/{namespace}/cronjobs/{cronjob}")
def get_namespaced_cronjobs(
    namespace: str,
    cronjob: str, 
    request: Request
    ):
    return Kubernetes_Call_Method.get_cronjob(namespace,cronjob)

@router.post("/namespaces/{namespace}/cronjobs/create")
def post_namespaced_cronjob_create(
    namespace: str, 
    Item: CronJobPostBaseModel, 
    request: Request
    ):
    return Kubernetes_Idling_Engine.cronjob_idling_workflow(
        Item.namespace,
        Item.name,
        Item.starting_schedule,
        Item.stopping_schedule,
        Item.replicas
        )
    
@router.post("/namespaces/{namespace}/cronjobs/delete")
def post_namespaced_cronjob_delete(
    namespace: str, 
    Item: CronJobPostBaseModel, 
    request: Request
    ):
    return Kubernetes_Idling_Engine.cronjob_idling_workflow(
        Item.namespace,
        Item.name,
        Item.starting_schedule,
        Item.stopping_schedule,
        Item.replicas
        )
