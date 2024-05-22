# {"user": "Bob"}
CREATE_USER = {
    "type": "object",
    "required": [
        "user",
    ],
    "properties": {"user": {"type": "string", "minLength": 3, "maxLength": 10}},
}

# {"game_id": "05548915-a38b-4bad-b96f-1974f5691f57", "user": "Bob", "roll": "Tree"}
PLAY_ROUND = {
    "type": "object",
    "required": [
        "game_id",
        "user",
        "roll",
    ],
    "properties": {
        "game_id": {
            "type": "string",
            "pattern": "^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[4][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$",  # noqa
            # UUID4 regex pattern
        },
        "user": {"type": "string", "minLength": 3, "maxLength": 10},
        "roll": {"type": "string", "minLength": 3, "maxLength": 10},
    },
}
