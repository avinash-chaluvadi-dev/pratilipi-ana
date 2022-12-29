from typing import Union


def to_snake(s: str) -> str:
    """Takes a string and converts it to snake format"""
    return "".join(["_" + i.lower() if i.isupper() else i for i in s]).lstrip("_")


def dict_keys_snake(d: str) -> Union[list, dict]:
    """Takes a dict and converts its keys to snake format"""
    return {to_snake(a): dict_keys_snake(b) if isinstance(b, (dict, list)) else b for a, b in d.items()}
