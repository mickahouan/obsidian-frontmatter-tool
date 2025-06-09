# frontmatter_tool_project/app/core/actions/delete_files_by_kv_action.py
import os

from .base_action import BaseAction


class DeleteFilesByKeyValueAction(BaseAction):
    def get_description(self) -> str:
        key = self.params.get("key", "UNBEKANNTER_KEY")
        value = self.params.get("value", "UNBEKANNTER_WERT")
        return f"Batch: Dateien löschen, wenn Key '{key}' den Wert '{value}' hat"

    def execute_on_file_logic(self, post, file_path: str) -> tuple[bool, str]:
        key_to_match = self.params.get("key")
        value_to_match = self.params.get("value")
        base_name = os.path.basename(file_path)

        if key_to_match is None or value_to_match is None:
            self.logger(
                f"FEHLER (DeleteFilesByKeyValueAction): Key oder Value nicht spezifiziert für {base_name}."
            )
            return False, "Key oder Value nicht spezifiziert"

        # Prüfen, ob der Key existiert und den gewünschten Wert hat
        if key_to_match in post.metadata and str(post.metadata[key_to_match]) == str(
            value_to_match
        ):
            if self.is_dry_run:
                self.logger(
                    f"[DryRun] In '{base_name}': Datei würde gelöscht (Match: '{key_to_match}':'{value_to_match}')."
                )
                return (
                    True,
                    f"[DryRun] Datei würde gelöscht (Match: '{key_to_match}':'{value_to_match}').",
                )
            else:
                try:
                    os.remove(file_path)
                    self.logger(
                        f"GELÖSCHT: Datei '{base_name}' ({file_path}) (Match: '{key_to_match}':'{value_to_match}')."
                    )
                    return (
                        True,
                        f"Datei gelöscht (Match: '{key_to_match}':'{value_to_match}').",
                    )
                except Exception as e:
                    self.logger(
                        f"FEHLER beim Löschen der Datei '{base_name}' ({file_path}): {e}"
                    )
                    return False, f"Fehler beim Löschen: {e}"
        elif key_to_match not in post.metadata:
            self.logger(
                f"Info: In '{base_name}': Key '{key_to_match}' nicht gefunden für Löschprüfung."
            )
            return False, f"Key '{key_to_match}' nicht gefunden für Löschprüfung."
        else:
            actual_value = post.metadata[key_to_match]
            self.logger(
                f"Info: In '{base_name}': Key '{key_to_match}' hat Wert '{actual_value}', nicht '{value_to_match}'. Keine Löschung."
            )
            return (
                False,
                f"Key '{key_to_match}' hat Wert '{actual_value}', nicht '{value_to_match}'. Keine Löschung.",
            )

    # Diese Aktion verwendet _save_changes nicht, da sie die Datei direkt löscht.
    # Die process_file Methode der BaseAction wird aber weiterhin verwendet,
    # um ggf. Vorbedingungen zu prüfen, bevor execute_on_file_logic aufgerufen wird.
