import re
from typing import List

import phonenumbers
from fastapi import HTTPException

from pebble.models.schemas.api_core_data_schema import SelectorSchema, ApiCoreDataSchemaV1


def phone_wrap(input_api_core_data: ApiCoreDataSchemaV1, output_api_core_data: ApiCoreDataSchemaV1, region: str = None) -> List[str]:
    """
    Calls all the phone numbers extractor functions
    :param region:
    :param text:
    :return:
    """
    if input_api_core_data.content_mime_type.lower() in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail=f'Phone extract cannot process image files')

    text: str = input_api_core_data.content_data.decode('utf-8')
    phone_numbers: List[str] = [set(phone_number_extractor(text, region) + phone_number_regex_extractor(text))]
    output_api_core_data.content_data = 'Pebble Service extracted the phone numbers ' + ' ,'.join(phone_numbers)
    output_api_core_data.content_url = 'http://pebble?Cmd=phone_extractors'
    builder: SelectorSchema = SelectorSchema(selector_type_name='phone')
    selectors: List[SelectorSchema] = []

    for phone_number in phone_numbers:
        selector = builder.model_copy()
        selector.selector_name = phone_number
        selectors.append(selector)
    output_api_core_data.content_selectors_json = selectors


def phone_number_regex_extractor(text: str) -> List[str]:
    phone_numbers: List[str] = re.findall(r'^(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$', text)
    return phone_numbers


def phone_number_extractor(text: str, region: str = None) -> List[str]:
    """
    Extract phone numbers from the given text
    :param text:
    :param region:
    :return:
    """
    phone_numbers: List[str] = []
    for match in phonenumbers.PhoneNumberMatcher(text, region=region):
        phone_numbers.append(match.raw_string)
    return phone_numbers
