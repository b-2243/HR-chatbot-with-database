# utils/prompts_loader.py

import json
import os

# PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "../prompts.json")
PROMPTS_PATH="D:/hrchatbot/hrchatbot/chatbotmodule/utils/prompts.json"

with open(PROMPTS_PATH, "r", encoding="utf-8") as f:
    PROMPTS = json.load(f)

def get_formatted_prompt(prompt_key: str, **kwargs) -> str:
    template = PROMPTS.get(prompt_key)
    if not template:
        raise ValueError(f"Prompt key '{prompt_key}' not found.")
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Missing placeholder for: {str(e)}")
