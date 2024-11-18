from datetime import datetime
from bson import ObjectId
from typing import Any


def serialize_object(obj: Any) -> Any:
    """
    Recursively converts MongoDB-specific types like ObjectId and datetime
    to JSON-serializable formats.
    """
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):

        return {key: serialize_object(value) for key, value in obj.items()}
    elif isinstance(obj, list):

        return [serialize_object(item) for item in obj]
    else:
        return obj
