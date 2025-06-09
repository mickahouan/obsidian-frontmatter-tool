"""
Aktion: Bennent einen Key im Frontmatter um.
"""

import os

from .base_action import BaseAction


class RenameKeyAction(BaseAction):
    def get_description(self) -> str:
        """Beschreibung der Aktion für das Logging."""
        old_key = self.params.get("old_key", "UNBEKANNTER_ALTER_KEY")
        new_key = self.params.get("new_key", "UNBEKANNTER_NEUER_KEY")
        return f"Batch: Key '{old_key}' zu '{new_key}' umbenennen"

    def execute_on_file_logic(self, post, file_path: str) -> tuple[bool, str]:
        """Bennent den Key im Frontmatter um."""
        old_key_name = self.params.get("old_key")
        new_key_name = self.params.get("new_key")
        base_name = os.path.basename(file_path)

        if not old_key_name or not new_key_name:
            self.logger(
                f"FEHLER (RenameKeyAction): Alter oder neuer Key nicht spezifiziert für {base_name}."
            )
            return False, "Alter oder neuer Key nicht spezifiziert"

        if old_key_name == new_key_name:
            self.logger(
                f"Info: In '{base_name}': Alter und neuer Key ('{old_key_name}') identisch. Keine Änderung."
            )
            return (
                False,
                f"Alter und neuer Key ('{old_key_name}') identisch. Keine Änderung.",
            )

        if old_key_name in post.metadata:
            value_to_move = post.metadata[old_key_name]
            action_description_for_log = (
                f"Key '{old_key_name}' zu '{new_key_name}' umbenennen"
            )

            warning_message_part = ""
            if new_key_name in post.metadata:
                existing_new_key_value = post.metadata[new_key_name]
                warning_message_part = f" (Warnung: Neuer Key '{new_key_name}' existierte mit Wert '{existing_new_key_value}' und wurde überschrieben!)"
                log_prefix = "[DryRun] " if self.is_dry_run else ""
                self.logger(
                    f"{log_prefix}In '{base_name}':{warning_message_part.strip()}"
                )

            if self.is_dry_run:
                log_detail = f"(Wert von '{old_key_name}' war: '{value_to_move}')."
                self.logger(
                    f"[DryRun] In '{base_name}': {action_description_for_log} {log_detail}"
                )
                return (
                    True,
                    f"[DryRun] Key '{old_key_name}' würde zu '{new_key_name}' umbenannt werden.{warning_message_part} {log_detail}",
                )
            else:
                del post.metadata[old_key_name]
                post.metadata[new_key_name] = value_to_move
                if self._save_changes(post, file_path, action_description_for_log):
                    return (
                        True,
                        f"Key '{old_key_name}' zu '{new_key_name}' umbenannt.{warning_message_part}",
                    )
                else:
                    return (
                        False,
                        f"Fehler beim Speichern nach Umbenennung von '{old_key_name}'",
                    )
        else:
            self.logger(
                f"Info: In '{base_name}': Alter Key '{old_key_name}' nicht gefunden. Keine Änderung."
            )
            return False, f"Alter Key '{old_key_name}' nicht gefunden. Keine Änderung."
