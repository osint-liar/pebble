import logging
from fastapi import HTTPException
from pebble.models.schemas.api_core_data_schema import ApiCoreDataSchemaV1
import whisper

logger = logging.getLogger(__name__)


def whisper_extract_text_command(input_api_core_data: ApiCoreDataSchemaV1, output_api_core_data: ApiCoreDataSchemaV1) \
        -> None:
    """

    :param input_api_core_data: The origin parent record that is immutable, only a modified child(ren) node(s) can be
    modified
    :param output_api_core_data:
    :return:
    """

    mime_types = [
        "audio/mpeg",
        "audio/wav",
        "audio/x-wav",
        "audio/wave",
        "audio/x-pn-wav",
        "audio/ogg",
        "application/ogg",
        "audio/flac",
        "audio/x-flac",
        "audio/aac",
        "audio/x-aac",
        "audio/mp4",
        "audio/x-m4a"
    ]

    if input_api_core_data.content_mime_type.lower() not in mime_types:
        raise HTTPException(status_code=400, detail=f'Whisper cannot process non-audio files')

    file_path: str = input_api_core_data.content_file_path
    try:
        logger.debug(f'whisper text extract command: {file_path}')
        model = whisper.load_model("base")
        result = model.transcribe(file_path)
        text: str = result["text"]
        logging.debug(f"whisper text extract successful for {file_path}")
        output_api_core_data.content_data = text.strip()
        output_api_core_data.content_url = f'http://pebble/{whisper_extract_text_command.__name__}'
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except IOError:
        logging.error(f"IOError when opening {file_path}")
    except Exception as e:
        logging.error(f"Unexpected error for {file_path}: {e}")
