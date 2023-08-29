import stringcase
from pydantic import BaseModel


def to_pascal(name: str) -> str:
    return stringcase.pascalcase(name)


class PascalCaseModel(BaseModel):
    """
    All inbound and outbound will get renamed to PascalCode variable names, because that is what OSINT LIAR is
    expecting.
    """
    class Config:
        alias_generator = to_pascal
        populate_by_name = True
