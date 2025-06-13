# frontmatter_tool_project/main.py
import sys

from PySide6.QtCore import QCoreApplication, QTranslator
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from app.main_window import FrontmatterTool
from app.ui_components.frontmatter_table_viewer import FrontmatterTableViewer


def start_app():
    """
    Initializes and starts the FrontmatterTool application.

    This function creates a QApplication instance, initializes the main window
    (FrontmatterTool), displays it, and starts the application's event loop.

    Raises:
        SystemExit: If the application is closed, sys.exit() is called to exit the program.
    """
    app = QApplication(sys.argv)
    # Sprachwahl: 'de' für Deutsch, 'en' für Englisch
    language = "en"  # <--- hier Sprache ändern: 'de' oder 'en'
    translator = QTranslator()
    if language == "de":
        translator.load("translations/de.qm")
    elif language == "en":
        translator.load("translations/en.qm")
    app.installTranslator(translator)
    window = FrontmatterTool(language=language, app_translator=translator)
    window.show()
    sys.exit(app.exec())


def show_table_demo():
    app = QApplication(sys.argv)
    language = "en"  # <--- hier Sprache ändern: 'de' oder 'en'
    translator = QTranslator()
    if language == "de":
        translator.load("translations_de.qm")
    elif language == "en":
        translator.load("translations_en.qm")
    app.installTranslator(translator)
    win = QMainWindow()
    win.setWindowTitle(
        QCoreApplication.translate(
            "FrontmatterTableViewer", "Frontmatter TableViewer Demo"
        )
    )
    central = QWidget()
    layout = QVBoxLayout(central)
    table = FrontmatterTableViewer()
    layout.addWidget(table)
    win.setCentralWidget(central)
    # Beispiel-Daten (Key: (Value, Typ))
    demo_data = {
        "title": ("Mein Titel", "Text"),
        "tags": ("tag1, tag2", "Liste"),
        "done": ("false", "Checkbox"),
        "created": ("2024-06-09", "Datum"),
        "reviewed": ("2024-06-09 12:00", "Datum und Uhrzeit"),
        "counter": ("42", "Zahl"),
    }
    table.display_frontmatter(demo_data)
    win.resize(600, 300)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    start_app()
    show_table_demo()
