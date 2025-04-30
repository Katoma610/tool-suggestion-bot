import json
from typing import Dict, List


def format_tools(tools: List[Dict]) -> str:
    formatted = []
    for tool in tools:
        formatted.append(
            f"• {tool['name']}\n"
            f"  {tool['description']}\n"
            f"  💰  {tool['pricing']}\n"
            f"  🔗  {tool['url']}"
        )
    return '\n\n'.join(formatted)


class ToolParsing:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = self._read_data()

    def _read_data(self) -> Dict:
        with open(self.filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get_categories(self):
        return list(self.data.keys())

    def get_subcategories(self, category: str):
        return list(self.data.get(category, {}).keys())

    def get_tools(self, category: str, subcategory: str):
        return self.data.get(category, {}).get(subcategory, None)
