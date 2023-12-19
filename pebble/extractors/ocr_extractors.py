import logging
import pytesseract

from pebble.models.schemas.api_core_data_schema import ApiCoreDataSchemaV1

logger = logging.getLogger(__name__)



def pytesseract_ocr_command(input_api_core_data: ApiCoreDataSchemaV1, output_api_core_data: ApiCoreDataSchemaV1) \
        -> None:
    """

    :param input_api_core_data: The origin parent record that is immutable, only a modified child(ren) node(s) can be
    modified
    :param output_api_core_data:
    :return:
    """
    file_path: str = input_api_core_data.content_file_path
    try:
        logger.debug(f'pytesseract ocr_command: {file_path}')
        text: str = pytesseract.image_to_string(file_path)
        logging.debug(f"OCR successful for {file_path}")
        output_api_core_data.content_data = text
        output_api_core_data.content_url = 'http://pebble'
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except pytesseract.TesseractError as e:
        logging.error(f"Tesseract error for {file_path}: {e}")
    except IOError:
        logging.error(f"IOError when opening {file_path}")
    except Exception as e:
        logging.error(f"Unexpected error for {file_path}: {e}")
