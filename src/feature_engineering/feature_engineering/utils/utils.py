import json

def str2bool(string: str) -> bool:
    return json.loads(string.lower())

def str2enum(string: str, enum_type: type):
    return enum_type[string.upper()]

