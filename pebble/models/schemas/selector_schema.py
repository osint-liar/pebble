from pebble.models.schemas.pascal_case_model import PascalCaseModel


class SelectorSchema(PascalCaseModel):
    selector_name: str
    selector_type_name: str

