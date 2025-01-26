from pydantic import BaseModel
from typing import Dict

class RequestModel(BaseModel):
    topics: Dict[str, int]

class ProviderModel(BaseModel):
    provider_topics: Dict[str, str]
