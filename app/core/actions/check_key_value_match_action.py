# frontmatter_tool_project/app/core/actions/check_key_value_match_action.py
from .base_action import BaseAction
import os

class CheckKeyValueMatchAction(BaseAction):
    def get_description(self) -> str:
        key = self.params.get('key', 'UNBEKANNTER_KEY')
        value = self.params.get('value', 'UNBEKANNTER_WERT')
        return f"Batch: Prüfen, ob Key '{key}' den Wert '{value}' hat"

    def execute_on_file_logic(self, post, file_path: str) -> tuple[bool, str]:
        key_to_check = self.params.get('key')
        value_to_match = self.params.get('value')
        base_name = os.path.basename(file_path)

        if not key_to_check: # Value kann hier optional sein, je nach Definition, aber für "Match" brauchen wir ihn
            self.logger(f"FEHLER (CheckKeyValueMatchAction): Key nicht spezifiziert für {base_name}.")
            return False, "Key nicht spezifiziert"
        if value_to_match is None: # Für einen Match brauchen wir einen Wert
             self.logger(f"FEHLER (CheckKeyValueMatchAction): Value nicht spezifiziert für {base_name}.")
             return False, "Value nicht spezifiziert"


        if key_to_check in post.metadata and str(post.metadata[key_to_check]) == str(value_to_match):
            self.logger(f"Info: In '{base_name}': Key '{key_to_check}' hat den Wert '{value_to_match}'.")
            return True, f"Key '{key_to_check}' hat Wert '{value_to_match}'"
        else:
            # Loggen, warum es nicht gematcht hat (optional, aber hilfreich)
            # if key_to_check not in post.metadata:
            #     self.logger(f"Info: In '{base_name}': Key '{key_to_check}' nicht gefunden für Wertprüfung.")
            # else:
            #     self.logger(f"Info: In '{base_name}': Key '{key_to_check}' hat Wert '{post.metadata[key_to_check]}', nicht '{value_to_match}'.")
            return False, f"Key '{key_to_check}' hat nicht Wert '{value_to_match}'"