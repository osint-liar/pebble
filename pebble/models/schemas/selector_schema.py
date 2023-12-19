from typing import Optional

from pydantic import BaseModel


class SelectorSchema(BaseModel):
    selector_name: Optional[str] = None
    selector_type_name: str
    active: bool = False
    description: Optional[str] = None

