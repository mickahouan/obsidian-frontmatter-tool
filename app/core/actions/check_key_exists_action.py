# frontmatter_tool_project/app/core/actions/check_key_exists_action.py
from .base_action import BaseAction
import os


class CheckKeyExistsAction(BaseAction):
    def get_description(self) -> str:
        key_to_check = self.params.get("key", "UNBEKANNTER_KEY")
        return f"Batch: Prüfen, ob Key '{key_to_check}' existiert"

    def execute_on_file_logic(self, post, file_path: str) -> tuple[bool, str]:
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
                f"Key '{key_to_check}' vorhanden",
            )  # Gibt True zurück, um als "betroffen" zu zählen
        else:
            # self.logger(f"Info: In '{base_name}': Key '{key_to_check}' nicht gefunden.")
            return False, f"Key '{key_to_check}' nicht gefunden"
