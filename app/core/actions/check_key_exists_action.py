"""
Aktion: Prüft, ob ein bestimmter Key im Frontmatter existiert.
"""

import os

from .base_action import BaseAction


class CheckKeyExistsAction(BaseAction):
    def get_description(self) -> str:
        """Beschreibung der Aktion für das Logging."""
        key_to_check = self.params.get("key", "UNBEKANNTER_KEY")
        return f"Batch: Prüfen, ob Key '{key_to_check}' existiert"

    def execute_on_file_logic(self, post, file_path: str) -> tuple[bool, str]:
        """Prüft, ob der Key im Frontmatter vorhanden ist."""
        key_to_check = self.params.get("key")
        base_name = os.path.basename(file_path)

        if not key_to_check:
            self.logger(
                f"FEHLER (CheckKeyExistsAction): Key nicht spezifiziert für {base_name}."
            )
            return False, "Key nicht spezifiziert"

        if key_to_check in post.metadata:
            value = post.metadata[key_to_check]
            self.logger(
                f"Info: In '{base_name}': Key '{key_to_check}' vorhanden (Wert: '{value}')."
            )
            return (
                True,
                f"Key '{key_to_check}' vorhanden (Wert: '{value}')",
            )
        else:
            self.logger(f"Info: In '{base_name}': Key '{key_to_check}' nicht gefunden.")
            return False, f"Key '{key_to_check}' nicht gefunden."
