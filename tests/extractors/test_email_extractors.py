from typing import List

from pebble.extractors.email_extractors import email_by_regex


def test_email_not_found() -> None:
    emails: List[str] = email_by_regex("no emails in text")
    assert emails == []


def test_email_found() -> None:
    emails: List[str] = email_by_regex("This text has one email johndoe@example.com")
    assert emails == ['johndoe@example.com']
