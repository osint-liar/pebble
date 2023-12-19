from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel

from pebble.models.schemas.api_core_data_schema import ApiCoreDataSchemaV1
from pebble.models.schemas.selector_schema import SelectorSchema


class MessageSchema(BaseModel):
    """Insert a message to be relayed to the end user"""
    type: str
    message: str
    title: str


class EnrichmentSchema(BaseModel):
    tags: Optional[List[str]] = []
    selectors: Optional[List[SelectorSchema]] = []
    text: Optional[str] = None
    attributes: Dict[str, Any] = dict()
    message: Optional[MessageSchema]
    name: Optional[str]
    version: Optional[str]
    created_on: datetime = datetime.utcnow()
    api_core_data_v1: Optional[ApiCoreDataSchemaV1]

