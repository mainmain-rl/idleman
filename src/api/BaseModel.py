from pydantic import BaseModel

class BaseModelNamespaceResponse(BaseModel):
    namespace: list
    
class CronJobPostBaseModel(BaseModel):
    namespace: str
    name: str
    starting_schedule: str
    stopping_schedule : str
    replicas: int