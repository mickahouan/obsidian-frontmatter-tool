"""
Aktion: Entfernt einen Key aus dem Frontmatter.
"""

import os  # Für os.path.basename

from .base_action import BaseAction


class DeleteKeyAction(BaseAction):
    def get_description(self) -> str:
        """Beschreibung der Aktion für das Logging."""
        key_to_delete = self.params.get("key", "UNBEKANNTER_KEY")
        return f"Batch: Key '{key_to_delete}' entfernen"

    def execute_on_file_logic(self, post, file_path: str) -> tuple[bool, str]:
        """Entfernt den Key aus dem Frontmatter."""
        key_to_delete = self.params.get("key")
        base_name = os.path.basename(file_path)

        if not key_to_delete:
            self.logger(
                f"FEHLER (DeleteKeyAction): Key nicht in Parametern spezifiziert für {base_name}."
            )
            return False, "Key nicht spezifiziert"

        if key_to_delete in post.metadata:
            original_value = post.metadata[key_to_delete]
            action_description_for_log = f"Key '{key_to_delete}' entfernen"

            if self.is_dry_run:
                self.logger(
                    f"[DryRun] In '{base_name}': {action_description_for_log} (Wert war: '{original_value}')."
                )
                return (
                    True,
                    f"[DryRun] Key '{key_to_delete}' würde entfernt werden. (Wert war: '{original_value}')",
                )
            else:
                del post.metadata[key_to_delete]
                if self._save_changes(post, file_path, action_description_for_log):
                    self.logger(
                        f"In '{base_name}': {action_description_for_log}. (Wert war: '{original_value}')"
                    )
                    return (
                        True,
                        f"Key '{key_to_delete}' entfernt. (Wert war: '{original_value}')",
                    )
                else:
                    return (
                        False,
                        f"Fehler beim Speichern nach Entfernen von Key '{key_to_delete}'",
                    )
        else:
            self.logger(
                f"Info: In '{base_name}': Key '{key_to_delete}' nicht gefunden. Keine Änderung."
            )
            return False, f"Key '{key_to_delete}' nicht gefunden. Keine Änderung."
