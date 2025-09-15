# schema_utils.py
import re

def load_schema_text(file_path: str) -> str:
    with open(file_path, 'r', encoding="utf-8") as f:
        return f.read()

def parse_schema_to_table_blocks(schema_text: str) -> dict:
    blocks = schema_text.strip().split('\n\n')
    table_blocks = {}
    for block in blocks:
        lines = block.strip().splitlines()
        if not lines:
            continue
        match = re.match(r"^(\w+):", lines[0])
        if match:
            table_name = match.group(1)
            table_blocks[table_name] = block
    return table_blocks
