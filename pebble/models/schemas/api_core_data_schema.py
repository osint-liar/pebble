from typing import Optional, Any, List
import stringcase
from pydantic import BaseModel, ConfigDict


def to_pascal(name: str) -> str:
    return stringcase.pascalcase(name)


class SelectorSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_pascal, populate_by_name=True)
    selector_name: Optional[str] = None
    selector_type_name: str


class ApiCoreDataSchema(BaseModel):
    """ The core data is used inside pebble. On input or output the data fields use Pascal Case"""
    content_uuid: Optional[str] = None
    content_text: Optional[str] = None
    content_data: Optional[Any] = None
    content_type: Optional[str] = None
    content_parent_uuid: Optional[str] = None
    content_root_uuid: Optional[str] = None
    content_mime_type: Optional[str] = None
    content_file_path: Optional[str] = None
    content_size: Optional[int] = None
    content_url: Optional[str] = None
    content_note: Optional[str] = None
    content_sourced_from: str = 'Pebble Api'
    content_title: Optional[str] = None
    content_selectors_json: Optional[List[SelectorSchema]] = None
    case_management_uuid: Optional[str] = None
    case_management_name: Optional[str] = None


class ApiCoreDataSchemaV1(ApiCoreDataSchema):
    """ Transform from the incoming core data"""
    model_config = ConfigDict(alias_generator=to_pascal, populate_by_name=True)


class ApiCoreDataSchemaV1Response(ApiCoreDataSchema):
    """ Transform from intermediate format to pascal case for outputting it"""
    model_config = ConfigDict(alias_generator=to_pascal, populate_by_name=True)

