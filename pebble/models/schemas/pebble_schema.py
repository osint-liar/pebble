from typing import Optional, Union, List

from pydantic import BaseModel

from pebble.models.schemas.api_core_data_schema import ApiCoreDataSchemaV1Response


class PebbleResponseSchema(BaseModel):
    Title: Optional[str] = None
    Record: Optional[ApiCoreDataSchemaV1Response] = None
    Message: Optional[str] = None
    Type: Optional[str] = None
