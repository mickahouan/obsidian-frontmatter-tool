# frontmatter_tool_project/app/core/actions/write_kv_action.py
import os

from .base_action import BaseAction


class WriteKeyValueAction(BaseAction):
    def get_description(self) -> str:
        key = self.params.get("key", "UNBEKANNTER_KEY")
        value_param = self.params.get("value", "")
        if isinstance(value_param, str) and "," in value_param:
            processed_value_for_desc = [s.strip() for s in value_param.split(",")]
            return f"Batch: Key '{key}' auf Liste '{processed_value_for_desc}' schreiben/überschreiben"
        else:
            return (
                f"Batch: Key '{key}' auf Wert '{value_param}' schreiben/überschreiben"
            )

    def execute_on_file_logic(self, post, file_path: str) -> tuple[bool, str]:
        key_to_write = self.params.get("key")
        raw_value_to_write = self.params.get("value")
        base_name = os.path.basename(file_path)

        if key_to_write is None:
            self.logger(
                f"FEHLER (WriteKeyValueAction): Key nicht spezifiziert für {base_name}."
            )
            return False, "Key nicht spezifiziert"

        final_value_to_write: object
        if isinstance(raw_value_to_write, str) and "," in raw_value_to_write:
            final_value_to_write = [
                s.strip() for s in raw_value_to_write.split(",") if s.strip()
            ]
        else:
            final_value_to_write = raw_value_to_write

        original_value = post.metadata.get(key_to_write)

        changed = False
        if type(original_value) != type(final_value_to_write):
            changed = True
        elif isinstance(final_value_to_write, list):
            if sorted(
                original_value if isinstance(original_value, list) else []
            ) != sorted(final_value_to_write):
                changed = True
        elif str(original_value) != str(final_value_to_write):
            changed = True

        if not changed:
            self.logger(
                f"Info: In '{base_name}': Key '{key_to_write}' hat bereits den Wert '{original_value}'. Keine Änderung."
            )
            return False, f"Key '{key_to_write}' hatte bereits Wert '{original_value}'"

        action_description_for_log = (
            f"Key '{key_to_write}' auf Wert '{final_value_to_write}' setzen"
        )

        if self.is_dry_run:
            log_original_value = (
                f"(Wert war: '{original_value}')"
                if original_value is not None
                else "(Key war nicht vorhanden)"
            )
            self.logger(
                f"[DryRun] In '{base_name}': {action_description_for_log} {log_original_value}."
            )
            return (
                True,
                f"[DryRun] Key '{key_to_write}' würde auf '{final_value_to_write}' gesetzt werden. {log_original_value}",
            )
        else:
            post.metadata[key_to_write] = final_value_to_write
            if self._save_changes(post, file_path, action_description_for_log):
                log_original_value = (
                    f"(Wert war: '{original_value}')"
                    if original_value is not None
                    else "(Key war nicht vorhanden)"
                )
                self.logger(
                    f"In '{base_name}': {action_description_for_log} {log_original_value}."
                )
                return (
                    True,
                    f"Key '{key_to_write}' auf '{final_value_to_write}' gesetzt. {log_original_value}",
                )
            else:
                return (
                    False,
                    f"Fehler beim Speichern nach Setzen von Key '{key_to_write}'",
                )
