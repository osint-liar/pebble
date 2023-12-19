import uuid

import tests.data.files.file_utils
from pebble.extractors.api_core_data_extractors import api_core_data_clone
from pebble.extractors.ocr_extractors import pytesseract_ocr_command
from pebble.models.schemas.api_core_data_schema import ApiCoreDataSchemaV1


def test_bad_file_type() -> None:
    parent = ApiCoreDataSchemaV1(content_file_path=tests.data.files.file_utils.get_test_file_path('hello_world.txt'))
    child = api_core_data_clone(parent)
    assert child.content_text is None
    pytesseract_ocr_command(parent, child)
    assert child.content_text is None


def test_osintliar_com_png() -> None:
    parent = ApiCoreDataSchemaV1(content_uuid=str(uuid.uuid4()),
                                 content_file_path=tests.data.files.file_utils.get_test_file_path('osintliar.com.png'))
    child = api_core_data_clone(parent)
    assert child.content_data is None
    pytesseract_ocr_command(parent, child)
    assert child.content_data is not None
