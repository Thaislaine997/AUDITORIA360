from services.ingestion.entity_schema import Entity
from typing import List
from pydantic import ValidationError


def validate_entities(raw_entities: List[dict]) -> (List[Entity], list):
    valid = []
    errors = []
    for ent in raw_entities:
        try:
            valid.append(Entity(**ent))
        except ValidationError as e:
            errors.append({"entity": ent, "error": str(e)})
    return valid, errors
