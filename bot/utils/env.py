import os

from dotenv import load_dotenv

load_dotenv()


def get_env(key: str) -> str:
    if not isinstance(key, str):
        raise ValueError(f"Key '{key}' is not a string")
    
    value = os.getenv(key)
    if not value:
        raise KeyError(f"Key '{key}' not found in env")
    
    return value