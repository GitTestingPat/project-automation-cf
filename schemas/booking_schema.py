BOOKING_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "flight_id": {"type": "string"},
        "user_id": {"type": "string"},
        "status": {
            "type": "string",
            "enum": ["draft", "paid", "checked_in", "cancelled"]
        },
        "passengers": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "full_name": {"type": "string"},
                    "passport": {"type": "string"},
                    "seat": {"type": ["string", "null"]}
                },
                "required": ["full_name", "passport"]
            }
        }
    },
    "required": ["id", "flight_id", "user_id", "status", "passengers"],
    "additionalProperties": False
}