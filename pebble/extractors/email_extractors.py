import logging
import re
from typing import List

logger = logging.getLogger(__name__)


def email_by_regex(text: str) -> List[str]:
    """
    Extract out a list of email addresses
    :param text:
    :return:
    """
    email_addresses: List[str] = re.findall(r"[A-Za-z0-9_%+-.]+"r"@[A-Za-z0-9.-]+"r"\.[A-Za-z]{2,5}", text)
    logger.info('Found %i email addresses.', len(email_addresses))
    return email_addresses
