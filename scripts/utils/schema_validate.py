import json, os
from jsonschema import validate, ValidationError
from utils.log_utils import log

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "master_schema.json")

def validate_entity(entity: dict, entity_type: str) -> bool:
    """Validate a JSON object against the master schema."""
    if not os.path.exists(SCHEMA_PATH):
        log(f"❌ Schema file not found at {SCHEMA_PATH}")
        return False

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        try:
            schema = json.load(f)
        except Exception as e:
            log(f"❌ Failed to load schema: {e}")
            return False

    if "definitions" not in schema or entity_type not in schema["definitions"]:
        log(f"❌ Entity type '{entity_type}' not defined in schema")
        return False

    entity_schema = schema["definitions"][entity_type]

    try:
        validate(instance=entity, schema=entity_schema)
        log(f"✅ {entity_type} is valid")
        return True
    except ValidationError as e:
        log(f"❌ Validation failed for {entity_type}: {e.message}")
        return False