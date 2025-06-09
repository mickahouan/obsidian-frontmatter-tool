# frontmatter_tool_project/app/core/actions/write_kv_action.py
import os

from .base_action import BaseAction


class WriteKeyValueAction(BaseAction):
    def get_description(self) -> str:
        key = self.params.get("key", "UNBEKANNTER_KEY")
        value_param = self.params.get("value", "")  # Hole den rohen Value-Parameter

        # Für die Beschreibung: Wenn es Kommas enthält, deute eine Liste an
        if isinstance(value_param, str) and "," in value_param:
            processed_value_for_desc = [s.strip() for s in value_param.split(",")]
            return f"Batch: Key '{key}' auf Liste '{processed_value_for_desc}' schreiben/überschreiben"
        else:
            return (
                f"Batch: Key '{key}' auf Wert '{value_param}' schreiben/überschreiben"
            )

    def execute_on_file_logic(self, post, file_path: str) -> tuple[bool, str]:
        key_to_write = self.params.get("key")
        raw_value_to_write = self.params.get("value")  # Der String aus der UI
        base_name = os.path.basename(file_path)

        if key_to_write is None:
            self.logger(
                f"FEHLER (WriteKeyValueAction): Key nicht spezifiziert für {base_name}."
            )
            return False, "Key nicht spezifiziert"

        # --- NEUE LOGIK ZUR VERARBEITUNG DES WERTES ---
        final_value_to_write: object  # Typ-Annotation für Klarheit
        if isinstance(raw_value_to_write, str) and "," in raw_value_to_write:
            # Wenn Kommas im String sind, als Liste interpretieren
            # Entferne führende/nachfolgende Leerzeichen von jedem Element
            final_value_to_write = [
                s.strip() for s in raw_value_to_write.split(",") if s.strip()
            ]  # if s.strip() um leere Elemente zu vermeiden
            # Wenn nach dem Splitten nur ein Element übrig bleibt und es leer war, oder alle leer waren,
            # könnte man es als leeren String behandeln, je nach gewünschtem Verhalten.
            # Hier: Wenn die Liste nach dem Filtern leerer Strings leer ist, wird eine leere Liste geschrieben.
            # Wenn die Liste nur ein Element enthält, wird eine Liste mit einem Element geschrieben.
        else:
            # Ansonsten den Wert so nehmen, wie er ist (kann leerer String sein)
            final_value_to_write = raw_value_to_write

        original_value = post.metadata.get(key_to_write)

        # Für den Vergleich und das Logging ist es wichtig, wie wir final_value_to_write darstellen
        # und wie wir es mit original_value vergleichen.
        # PyYAML serialisiert Listen und Strings unterschiedlich.

        # Prüfen, ob sich der Wert tatsächlich ändert
        # Dieser Vergleich wird komplexer, wenn original_value eine Liste sein könnte
        # und final_value_to_write auch.
        # Einfacher Vergleich: Konvertiere beide zu String für einen einfachen Check,
        # oder vergleiche Typen und Inhalte sorgfältiger.
        # Für einen robusten Vergleich:
        changed = False
        if type(original_value) != type(final_value_to_write):
            changed = True
        elif isinstance(final_value_to_write, list):
            # Vergleiche Listeninhalte (Reihenfolge spielt hier eine Rolle)
            if sorted(
                original_value if isinstance(original_value, list) else []
            ) != sorted(final_value_to_write):  # Reihenfolge ignorieren
                changed = True
        elif str(original_value) != str(
            final_value_to_write
        ):  # Einfacher String-Vergleich
            changed = True

        # Alternativ, wenn man immer überschreiben will, außer es ist exakt gleich:
        # if original_value == final_value_to_write und type(original_value) == type(final_value_to_write):
        #     changed = False
        # else:
        #     changed = True

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
            post.metadata[key_to_write] = (
                final_value_to_write  # Hier wird die Liste oder der String gesetzt
            )
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
