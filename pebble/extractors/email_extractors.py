import logging
import re
from typing import List

from pebble.models.schemas.api_core_data_schema import ApiCoreDataSchemaV1
from pebble.models.schemas.selector_schema import SelectorSchema

logger = logging.getLogger(__name__)


def email_wrap(input_api_core_data: ApiCoreDataSchemaV1, output_api_core_data: ApiCoreDataSchemaV1) -> None:
    """
    Wraps all the email extractors
    :return:
    """

    emails: List[str] = email_by_regex(input_api_core_data.content_data)
    builder: SelectorSchema = SelectorSchema(active=True, Description="Generated in Pebble Api ", selector_type_name='email')
    selectors: List[SelectorSchema]

    for email in emails:
        selector = builder.model_copy()
        selector.selector_name = email
        selectors.append(selector)
    output_api_core_data.content_selectors_json


def email_by_regex(text: str) -> List[str]:
    """
    Extract out a list of email addresses
    :param text:
    :return:
    """
    email_addresses: List[str] = re.findall(r"[A-Za-z0-9_%+-.]+"r"@[A-Za-z0-9.-]+"r"\.[A-Za-z]{2,5}", text)
    logger.info('Found %i email addresses.', len(email_addresses))
    return email_addresses
