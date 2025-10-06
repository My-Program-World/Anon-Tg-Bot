from textwrap import dedent
from typing import Any
from pathlib import Path

import yaml


def remove_space(text: str) -> str:
    return dedent(text)

def get_texts(folder_path: str, is_dedent: bool = False) -> dict[str, Any]:
    data: dict[str, Any] = {}
    
    for file in Path(folder_path).glob('*.yaml'):
        with file.open(encoding='utf-8') as f:
            data[file.stem] = yaml.safe_load(f)

    return data
