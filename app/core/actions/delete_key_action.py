# frontmatter_tool_project/app/core/actions/delete_key_action.py
from .base_action import BaseAction
import os # Für os.path.basename

class DeleteKeyAction(BaseAction):
    def get_description(self) -> str:
        key_to_delete = self.params.get('key', 'UNBEKANNTER_KEY')
        return f"Batch: Key '{key_to_delete}' entfernen"

    def execute_on_file_logic(self, post, file_path: str) -> tuple[bool, str]:
        key_to_delete = self.params.get('key')
        base_name = os.path.basename(file_path)

        if not key_to_delete:
            # Dieser Fehler sollte idealerweise schon vor der Iteration abgefangen werden
            self.logger(f"FEHLER (DeleteKeyAction): Key nicht in Parametern spezifiziert für {base_name}.")
            return False, "Key nicht spezifiziert"

        if key_to_delete in post.metadata:
            original_value = post.metadata[key_to_delete]
            action_description_for_log = f"Key '{key_to_delete}' entfernen"

            if self.is_dry_run:
                self.logger(f"[DryRun] In '{base_name}': {action_description_for_log} (Wert war: '{original_value}').")
                return True, f"würde Key '{key_to_delete}' entfernen"
            else:
                del post.metadata[key_to_delete]
                if self._save_changes(post, file_path, action_description_for_log):
                    self.logger(f"In '{base_name}': {action_description_for_log}.")
                    return True, f"Key '{key_to_delete}' entfernt"
                else:
                    # _save_changes loggt bereits den Fehler
                    return False, f"Fehler beim Speichern nach Entfernen von Key '{key_to_delete}'"
        else:
            # Key nicht gefunden, keine Aktion, aber auch kein Fehler im engeren Sinne der Aktion
            # self.logger(f"Info: In '{base_name}': Key '{key_to_delete}' nicht gefunden. Nichts entfernt.")
            return False, f"Key '{key_to_delete}' nicht gefunden"
