"""
Aktion: Prüft, ob ein bestimmter Key im Frontmatter fehlt.
"""

import os

from .base_action import BaseAction


class CheckKeyMissingAction(BaseAction):
    def get_description(self) -> str:
        """Beschreibung der Aktion für das Logging."""
        key_to_check = self.params.get("key", "UNBEKANNTER_KEY")
        return f"Batch: Prüfen, ob Key '{key_to_check}' fehlt"

    def execute_on_file_logic(self, post, file_path: str) -> tuple[bool, str]:
        """Prüft, ob der Key im Frontmatter fehlt."""
        key_to_check = self.params.get("key")
        base_name = os.path.basename(file_path)

        if not key_to_check:
            self.logger(
                f"FEHLER (CheckKeyMissingAction): Key nicht spezifiziert für {base_name}."
            )
            return False, "Key nicht spezifiziert"

        if key_to_check not in post.metadata:
            self.logger(f"Info: In '{base_name}': Key '{key_to_check}' fehlt.")
            return True, f"Key '{key_to_check}' fehlt."
        else:
            value = post.metadata[key_to_check]
            self.logger(
                f"Info: In '{base_name}': Key '{key_to_check}' vorhanden (Wert: '{value}')."
            )
            return False, f"Key '{key_to_check}' vorhanden (Wert: '{value}')."
