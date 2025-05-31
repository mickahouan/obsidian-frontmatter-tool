# frontmatter_tool_project/app/core/actions/write_kv_action.py
from .base_action import BaseAction
import os  # Für os.path.basename


class WriteKeyValueAction(BaseAction):
    def get_description(self) -> str:
        key = self.params.get("key", "UNBEKANNTER_KEY")
        value = self.params.get(
            "value", "UNBEKANNTER_WERT"
        )  # Default zu einem Platzhalter
        return f"Batch: Key '{key}' auf Wert '{value}' schreiben/überschreiben"

    def execute_on_file_logic(self, post, file_path: str) -> tuple[bool, str]:
        key_to_write = self.params.get("key")
        value_to_write = self.params.get("value")  # Value kann ein leerer String sein
        base_name = os.path.basename(file_path)

        if key_to_write is None:  # Key muss vorhanden sein
            self.logger(
                f"FEHLER (WriteKeyValueAction): Key nicht in Parametern spezifiziert für {base_name}."
            )
            return False, "Key nicht spezifiziert"

        # Value kann None sein, wenn es nicht explizit übergeben wird, aber ein leerer String ist ok.
        # Wenn value_to_write None ist, könnte man entscheiden, den Key zu löschen oder einen Fehler zu werfen.
        # Hier gehen wir davon aus, dass ein übergebener None-Wert als leerer String behandelt wird,
        # oder dass die UI sicherstellt, dass value_to_write zumindest ein leerer String ist.
        # Für mehr Robustheit könnte man hier explizit prüfen:
        if value_to_write is None:
            # Option 1: Fehler werfen/loggen
            # self.logger(f"WARNUNG (WriteKeyValueAction): Value für Key '{key_to_write}' ist None in {base_name}. Setze leeren String.")
            # value_to_write = ""
            # Option 2: Nichts tun oder spezifische Logik
            # Fürs Erste gehen wir davon aus, dass die UI einen String (ggf. leer) liefert.
            pass

        original_value = post.metadata.get(key_to_write)
        action_description_for_log = (
            f"Key '{key_to_write}' auf Wert '{value_to_write}' setzen"
        )

        # Prüfen, ob sich der Wert tatsächlich ändert
        if key_to_write in post.metadata and str(original_value) == str(value_to_write):
            # self.logger(f"Info: In '{base_name}': Key '{key_to_write}' hat bereits den Wert '{value_to_write}'. Nichts geändert.")
            return False, f"Key '{key_to_write}' hatte bereits Wert '{value_to_write}'"

        if self.is_dry_run:
            if original_value is not None:
                self.logger(
                    f"[DryRun] In '{base_name}': {action_description_for_log} (Wert war: '{original_value}')."
                )
            else:
                self.logger(
                    f"[DryRun] In '{base_name}': {action_description_for_log} (Key war nicht vorhanden)."
                )
            return True, f"würde Key '{key_to_write}' auf '{value_to_write}' setzen"
        else:
            post.metadata[key_to_write] = value_to_write
            if self._save_changes(post, file_path, action_description_for_log):
                if original_value is not None:
                    self.logger(
                        f"In '{base_name}': {action_description_for_log} (Wert war: '{original_value}')."
                    )
                else:
                    self.logger(
                        f"In '{base_name}': {action_description_for_log} (Key war nicht vorhanden)."
                    )
                return True, f"Key '{key_to_write}' auf '{value_to_write}' gesetzt"
            else:
                # _save_changes loggt bereits den Speicherfehler
                return (
                    False,
                    f"Fehler beim Speichern nach Setzen von Key '{key_to_write}'",
                )
