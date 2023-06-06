from fastapi import FastAPI
from api import ApiKubernetes
from modules.idling.KubernetesConfig import KubernetesConfig
from modules.idling.KubernetesCallMethod import KubernetesCallMethod
from modules.idling.KubernetesIdlingEngine import KubernetesIdlingEngine
from modules.common.Logging import ErrorManager

import sys, uvicorn, os

# Setup logging
logger = ErrorManager("INFO",__name__)

fastapi_app_name = os.getenv('FASTAPI_APP_NAME', "test-api")

app = FastAPI(
    title = fastapi_app_name,
    description = "My API",
    version = os.getenv('VERSION', "0.0.1"),
    debug=bool(os.getenv('DEBUG'))
    )
app.include_router(ApiKubernetes.router)
if __name__ == "__main__":
    port = int(sys.argv[1])
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port
        )