from typing import List, Optional, Dict, Any

from pebble.models.schemas.pascal_case_model import PascalCaseModel
from pebble.models.schemas.selector_schema import SelectorSchema


class MessageSchema(PascalCaseModel):
    """Insert a message to be relayed to the end user"""
    type: str
    message: str
    title: str


class EnrichmentSchema(PascalCaseModel):
    tags: List[str] = []
    selectors: List[SelectorSchema] = []
    text: Optional[str] = None
    attributes: Dict[str, Any] = dict()
    message: Optional[MessageSchema]

