import os
from abc import ABC, abstractmethod

import frontmatter


class BaseAction(ABC):
    def __init__(
        self, logger_func, params=None, dry_run=False, precondition_logic=None
    ):
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

    def _save_changes(
        self, post, file_path: str, action_description_for_log: str
    ) -> bool:
        if self.is_dry_run:
            self.logger(
                f"[DryRun] {action_description_for_log} würde in '{os.path.basename(file_path)}' gespeichert."
            )
            return True

        try:
            with open(file_path, "wb") as f_out:
                frontmatter.dump(post, f_out, encoding="utf-8")
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
        if self.precondition_logic:
            if not self.precondition_logic(post, self.params):
                base_name = os.path.basename(file_path)
                return False, f"Vorbedingung nicht erfüllt für {base_name}"
        return self.execute_on_file_logic(post, file_path)
