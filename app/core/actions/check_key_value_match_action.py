"""
Aktion: Prüft, ob ein Key einen bestimmten Wert hat.
"""

import os

from .base_action import BaseAction


class CheckKeyValueMatchAction(BaseAction):
    def get_description(self) -> str:
        """Beschreibung der Aktion für das Logging."""
        key = self.params.get("key", "UNBEKANNTER_KEY")
        value = self.params.get("value", "UNBEKANNTER_WERT")
        return f"Batch: Prüfen, ob Key '{key}' den Wert '{value}' hat"

    def execute_on_file_logic(self, post, file_path: str) -> tuple[bool, str]:
        """Prüft, ob der Key den gewünschten Wert hat."""
        key_to_check = self.params.get("key")
        value_to_match = self.params.get("value")
        base_name = os.path.basename(file_path)

        if not key_to_check:
            self.logger(
                f"FEHLER (CheckKeyValueMatchAction): Key nicht spezifiziert für {base_name}."
            )
            return False, "Key nicht spezifiziert"
        if value_to_match is None:
            self.logger(
                f"FEHLER (CheckKeyValueMatchAction): Value nicht spezifiziert für {base_name}."
            )
            return False, "Value nicht spezifiziert"

        if key_to_check in post.metadata and str(post.metadata[key_to_check]) == str(
            value_to_match
        ):
            self.logger(
                f"Info: In '{base_name}': Key '{key_to_check}' hat den Wert '{value_to_match}'."
            )
            return True, f"Key '{key_to_check}' hat Wert '{value_to_match}'."
        elif key_to_check not in post.metadata:
            self.logger(
                f"Info: In '{base_name}': Key '{key_to_check}' nicht gefunden für Wertprüfung."
            )
            return False, f"Key '{key_to_check}' nicht gefunden für Wertprüfung."
        else:
            actual_value = post.metadata[key_to_check]
            self.logger(
                f"Info: In '{base_name}': Key '{key_to_check}' hat Wert '{actual_value}', nicht '{value_to_match}'."
            )
            return (
                False,
                f"Key '{key_to_check}' hat Wert '{actual_value}', nicht '{value_to_match}'.",
            )
