# frontmatter_tool_project/app/ui_components/frontmatter_viewer.py
from PySide6.QtWidgets import QTextEdit
import frontmatter
import yaml # Stelle sicher, dass PyYAML installiert ist: pip install PyYAML
import os # Für os.path.basename

# Importiere aus dem core.utils Paket
from ..core.utils import is_supported_file


class FrontmatterViewer(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        # Du kannst die Schriftart hier setzen oder es dem globalen Stylesheet überlassen
        # self.setFont(QFont("Dank Mono", 13))

    def display_frontmatter(self, file_path: str, logger_func=None):
        """
        Lädt und zeigt das Frontmatter einer Datei an.
        :param file_path: Pfad zur Datei.
        :param logger_func: Optionale Funktion zum Loggen von Nachrichten.
        """
        if not file_path or not os.path.isfile(file_path) or not is_supported_file(file_path):
            self.clear_viewer()
            if logger_func and file_path: # Nur loggen, wenn ein Pfad versucht wurde
                logger_func(f"Info: Keine Frontmatter-Anzeige für '{os.path.basename(file_path)}' (nicht unterstützt oder kein File).")
            return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)

            if not post.metadata:
                self.setText(f"# Kein Frontmatter in {os.path.basename(file_path)} gefunden.")
                if logger_func:
                    logger_func(f"Info: Kein Frontmatter in {os.path.basename(file_path)} gefunden.")
                return

            yaml_frontmatter = yaml.dump(
                post.metadata, sort_keys=False, allow_unicode=True, indent=2, Dumper=yaml.SafeDumper
            )
            self.setText(yaml_frontmatter)
            if logger_func:
                logger_func(f"Frontmatter für {os.path.basename(file_path)} geladen.")
        except yaml.YAMLError as ye:
            self.setText(f"# Fehler beim Formatieren des Frontmatters (YAML Error):\n{ye}")
            if logger_func:
                logger_func(f"FEHLER beim Formatieren des Frontmatters für {file_path} (YAML Error): {ye}")
        except Exception as e:
            self.setText(f"# Unbekannter Fehler beim Laden des Frontmatters:\n{e}")
            if logger_func:
                logger_func(f"FEHLER beim Laden des Frontmatters für {file_path}: {e}")

    def clear_viewer(self):
        """Löscht den Inhalt des Viewers."""
        self.clear()
