import pytest
from fastapi import HTTPException

import tests.data.files.file_utils
from pebble.extractors.api_core_data_extractors import api_core_data_clone
from pebble.extractors.audio_to_text_extractors import whisper_extract_text_command
from pebble.models.schemas.api_core_data_schema import ApiCoreDataSchemaV1


def test_bad_file() -> None:
    parent = ApiCoreDataSchemaV1(
        content_file_path=tests.data.files.file_utils.get_test_file_path('hello_world.txt'),
        content_mime_type='text/plain'
    )
    child = api_core_data_clone(parent)
    assert child.content_data is None
    with pytest.raises(HTTPException) as exc_info:
        whisper_extract_text_command(parent, child)
    assert child.content_data is None


def test_audio_to_text() -> None:
    parent = ApiCoreDataSchemaV1(
        content_file_path=tests.data.files.file_utils.get_test_file_path('hello_world.mp3'),
        content_mime_type='audio/mpeg'
    )
    child = api_core_data_clone(parent)
    assert child.content_data is None
    whisper_extract_text_command(parent, child)
    assert child.content_data == 'Hello world.'