import logging
import re
from http.client import HTTPException
from typing import List

from pebble.models.schemas.api_core_data_schema import ApiCoreDataSchemaV1, SelectorSchema

logger = logging.getLogger(__name__)


def email_wrap(input_api_core_data: ApiCoreDataSchemaV1, output_api_core_data: ApiCoreDataSchemaV1) -> None:
    """
    Wraps all the email extractors
    :return:
    """
    if input_api_core_data.content_mime_type.lower() in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail=f'Email extract cannot process image files')

    text: str = input_api_core_data.content_data.decode('utf-8')
    emails: List[str] = filter(lambda e: not e.endswith('@mhtml.blink'), list(set(email_by_regex(text))))
    output_api_core_data.content_data = 'Pebble Service extracted the email addresses ' + ' ,'.join(emails)
    output_api_core_data.content_url = 'http://pebble?Cmd=email_extractors'
    builder: SelectorSchema = SelectorSchema(selector_type_name='email')
    selectors: List[SelectorSchema] = []

    for email in emails:
        selector = builder.model_copy()
        selector.selector_name = email
        selectors.append(selector)
    output_api_core_data.content_selectors_json = selectors


def email_by_regex(text: str) -> List[str]:
    """
    Extract out a list of email addresses
    :param text:
    :return:
    """
    email_addresses: List[str] = re.findall(r"[A-Za-z0-9_%+-.]+"r"@[A-Za-z0-9.-]+"r"\.[A-Za-z]{2,5}", text)
    logger.info('Found %i email addresses.', len(email_addresses))
    return email_addresses
