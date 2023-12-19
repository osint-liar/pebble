import uuid

from pebble.models.schemas.api_core_data_schema import ApiCoreDataSchemaV1, ApiCoreDataSchemaV1Response
from pebble.models.schemas.pebble_schema import PebbleResponseSchema


def api_core_data_clone(parent: ApiCoreDataSchemaV1) -> ApiCoreDataSchemaV1:
    """
    Clones the given parent and sets the parent and root uuid values for the while unsetting the necessary values
    :param parent:
    :return: ApiCoreDataSchemaV1
    """
    child: ApiCoreDataSchemaV1 = parent.model_copy(update=dict(content_data=None), deep=True)
    child.content_root_uuid = parent.content_uuid
    child.content_parent_uuid = parent.content_uuid
    child.content_uuid = str(uuid.uuid4())
    return child


def api_core_data_convert_to_response(instance: ApiCoreDataSchemaV1) -> PebbleResponseSchema:

    return PebbleResponseSchema(
        Record=ApiCoreDataSchemaV1Response(**instance.model_dump())
    )
