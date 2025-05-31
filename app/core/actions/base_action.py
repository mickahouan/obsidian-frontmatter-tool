import os
# frontmatter_tool_project/app/core/actions/base_action.py
from abc import ABC, abstractmethod
import frontmatter # Für frontmatter.dump in _save_changes

class BaseAction(ABC):
    def __init__(self, logger_func, params=None, dry_run=False, precondition_logic=None):
        """
        Initialisiert die Basisaktion.
        :param logger_func: Eine Funktion zum Loggen von Nachrichten.
        :param params: Ein Dictionary mit Parametern für die Aktion (key, value, new_key etc.).
        :param dry_run: Boolean, ob es ein Dry Run ist.
        :param precondition_logic: Optionale Funktion, die prüft, ob eine Vorbedingung erfüllt ist.
        Signatur: precondition_logic(post, params) -> bool
        """
        self.logger = logger_func
        self.params = params if params is not None else {}
        self.is_dry_run = dry_run
        self.precondition_logic = precondition_logic

    @abstractmethod
    def get_description(self) -> str:
        """Gibt eine Beschreibung der Aktion zurück (für Logging)."""
        pass

    @abstractmethod
    def execute_on_file_logic(self, post, file_path: str) -> tuple[bool, str]:
        """
        Führt die spezifische Logik der Aktion für eine einzelne Datei aus.
        Diese Methode wird von _process_file aufgerufen, nachdem Vorbedingungen geprüft wurden.

        :param post: Das geladene frontmatter.Post Objekt.
        :param file_path: Der Pfad zur Datei.
        :return: Tuple (bool: ob eine Änderung vorgenommen/simuliert wurde,
        str: eine spezifische Nachricht für diese Datei oder leerer String).
        """
        pass

    # In BaseAction._save_changes
    def _save_changes(
        self, post, file_path: str, action_description_for_log: str
    ) -> bool:
        if self.is_dry_run:
            self.logger(
                f"[DryRun] {action_description_for_log} würde in '{os.path.basename(file_path)}' gespeichert."
            )
            return True

        try:
            # ÄNDERUNG: Datei im Binärschreibmodus öffnen ('wb')
            with open(file_path, "wb") as f_out:  # 'wb' statt 'w'
                # frontmatter.dump wird jetzt die Bytes direkt schreiben können,
                # da es intern .encode() aufruft.
                frontmatter.dump(
                    post, f_out, encoding="utf-8"
                )  # encoding hier übergeben ist gut
            self.logger(
                f"GESPEICHERT: Änderungen nach '{action_description_for_log}' in '{os.path.basename(file_path)}'."
            )
            return True
        except Exception as e:
            self.logger(
                f"FEHLER beim Speichern nach '{action_description_for_log}' in '{os.path.basename(file_path)}': {e}"
            )
            return False

    def process_file(self, post, file_path: str) -> tuple[bool, str]:
        """
        Verarbeitet eine einzelne Datei. Prüft Vorbedingungen und ruft execute_on_file_logic auf.
        Diese Methode wird von der Hauptschleife in main_window aufgerufen.
        """
        # Vorbedingung prüfen, falls eine Logik dafür übergeben wurde
        if self.precondition_logic:
            if not self.precondition_logic(post, self.params): # params könnte hier auch die globalen Params sein
                base_name = os.path.basename(file_path)
                # Loggen, dass die Vorbedingung nicht erfüllt war, erfolgt idealerweise in der Hauptschleife,
                # die den Rückgabewert von precondition_logic direkt prüft.
                # Hier geben wir einfach zurück, dass nichts gemacht wurde.
                return False, f"Vorbedingung nicht erfüllt für {base_name}"

        # Eigentliche Aktionslogik ausführen
        return self.execute_on_file_logic(post, file_path)

# Importiere os für basename in _save_changes
