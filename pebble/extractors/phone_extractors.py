import re
from typing import List

import phonenumbers


def phone_wrap(text: str, region: str = None) -> List[str]:
    """
    Calls all the phone numbers extractor functions
    :param region:
    :param text:
    :return:
    """
    return phone_number_extractor(text, region) + phone_number_regex_extractor(text)


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
