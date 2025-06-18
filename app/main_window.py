"""
Hauptfenster und zentrale Logik für das Frontmatter Tool.
Bietet eine grafische Oberfläche zur Massenbearbeitung von YAML-Frontmatter in Markdown-Dateien.
"""

import os

import frontmatter
import yaml
from PySide6.QtCore import QCoreApplication, QDir, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    # QAction,
    QApplication,
    QCheckBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.core.actions import (
    CheckKeyExistsAction,
    CheckKeyMissingAction,
    CheckKeyValueMatchAction,
    DeleteFilesByKeyValueAction,
    DeleteKeyAction,
    RenameKeyAction,
    WriteKeyValueAction,
)
from .core.actions.base_action import BaseAction
from .core.utils import is_supported_file, value_matches
from .styles.cyberpunk_theme import get_cyberpunk_stylesheet
from .ui_components.dialogs import KeyDialog, KeyValueDialog, RenameKeyDialog
from .ui_components.file_explorer import FileExplorer
from .ui_components.frontmatter_table_viewer import FrontmatterTableViewer


class FrontmatterTool(QMainWindow):
    """
    Hauptklasse für das Frontmatter Tool.
    Stellt die Benutzeroberfläche bereit und implementiert die zentrale Logik für die Bearbeitung von Frontmatter in Markdown-Dateien.
    """

    def __init__(self, language="fr", app_translator=None):
        """
        Initialisiert das Hauptfenster und die UI-Komponenten.
        """
        super().__init__()
        self.dryrun_checkbox = None
        self.language = language
        self.translator = app_translator
        self.setWindowTitle(
            QCoreApplication.translate(
                "MainWindow", "Frontmatter Tool (PySide6 - Modular v4)"
            )
        )
        self.setGeometry(100, 100, 950, 750)
        self.directory = ""

        self.init_ui()
        self.setStyleSheet(get_cyberpunk_stylesheet())
        self.status = self.statusBar()
        self._init_menu()

    def _init_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu(QCoreApplication.translate("MainWindow", "Datei"))
        open_action = QAction(QCoreApplication.translate("MainWindow", "Verzeichnis öffnen"), self)
        quit_action = QAction(QCoreApplication.translate("MainWindow", "Beenden"), self)
        open_action.triggered.connect(self.select_directory)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

        lang_menu = QMenu(QCoreApplication.translate("MainWindow", "Sprache"), self)
        action_de = QAction("Deutsch", self)
        action_en = QAction("English", self)
        action_fr = QAction("Français", self)
        action_de.setCheckable(True)
        action_en.setCheckable(True)
        action_fr.setCheckable(True)
        action_de.setChecked(self.language == "de")
        action_en.setChecked(self.language == "en")
        action_fr.setChecked(self.language == "fr")
        lang_menu.addAction(action_de)
        lang_menu.addAction(action_en)
        lang_menu.addAction(action_fr)
        menubar.addMenu(lang_menu)

        def set_lang_de():
            self._change_language("de")

        def set_lang_en():
            self._change_language("en")

        def set_lang_fr():
            self._change_language("fr")

        action_de.triggered.connect(set_lang_de) # type: ignore
        action_en.triggered.connect(set_lang_en) # type: ignore
        action_fr.triggered.connect(set_lang_fr) # type: ignore
        self._lang_actions = {"de": action_de, "en": action_en, "fr": action_fr}

    def _change_language(self, lang):
        if lang == self.language:
            return
        from PySide6.QtCore import QCoreApplication, QTranslator

        if self.translator is None:
            self.translator = QTranslator()
        if lang == "de":
            self.translator.load("translations/de.qm")
        elif lang == "fr":
            self.translator.load("translations/fr.qm")
        else:
            self.translator.load("translations/en.qm")
        app = QCoreApplication.instance()
        if app is not None:
            app.installTranslator(self.translator)
        self.language = lang
        # Menü-Checkboxen aktualisieren
        for lang_key, act in self._lang_actions.items():
            act.setChecked(lang_key == lang)
        # UI-Elemente neu übersetzen, aber nur wenn UI schon initialisiert ist
        if getattr(self, "dryrun_checkbox", None) is not None:
            self._retranslate_ui()

    def _retranslate_ui(self):
        # Übersetzt alle UI-Elemente neu (nur die wichtigsten)
        self.setWindowTitle(
            QCoreApplication.translate(
                "MainWindow", "Frontmatter Tool (PySide6 - Modular v4)"
            )
        )
        self.dir_label.setText(
            QCoreApplication.translate("MainWindow", "Kein Verzeichnis ausgewählt")
        )
        self.save_fm_btn.setText(
            QCoreApplication.translate("MainWindow", "Frontmatter speichern")
        )
        if self.dryrun_checkbox is not None:
            self.dryrun_checkbox.setText(
                QCoreApplication.translate("MainWindow", "Dry Run")
            )
        self.only_if_key_value_checkbox.setText(
            QCoreApplication.translate("MainWindow", "Vorbedingung anwenden")
        )
        self.match_all_checkbox.setText(
            QCoreApplication.translate("MainWindow", "Alle Elemente müssen matchen")
        )
        self.key_label.setText(QCoreApplication.translate("MainWindow", "Key:"))
        self.value_label.setText(QCoreApplication.translate("MainWindow", "Value:"))
        self.newkey_label.setText(
            QCoreApplication.translate("MainWindow", "Neuer Key:")
        )
        self.precond_label.setText(
            QCoreApplication.translate("MainWindow", "Vorbedingung:")
        )
        self.key_input.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Key/Alter Key")
        )
        self.value_input.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Value (optional)")
        )
        self.newkey_input.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Neuer Key (für Umbenennen)")
        )
        self.precondition_key_input.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Vorbedingung Key")
        )
        self.precondition_value_input.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Vorbedingung Value")
        )
        self.log_clear_btn.setText(
            QCoreApplication.translate("MainWindow", "Protokoll löschen")
        )
        # Buttons in Batch-Operationen etc. können bei Bedarf ergänzt werden

    def init_ui(self):
        """
        Erstellt und arrangiert alle UI-Elemente des Hauptfensters.
        """
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        top_level_layout = QVBoxLayout(main_widget)
        top_level_layout.setContentsMargins(8, 8, 8, 8)
        top_level_layout.setSpacing(6)

        dir_row = QHBoxLayout()
        dir_btn = QPushButton(
            QCoreApplication.translate("MainWindow", "Verzeichnis auswählen")
        )
        dir_btn.clicked.connect(self.select_directory) # type: ignore
        self.dir_label = QLabel(
            QCoreApplication.translate("MainWindow", "Kein Verzeichnis ausgewählt")
        )
        self.dir_label.setStyleSheet("font-style: italic;")
        dir_row.addWidget(dir_btn)
        dir_row.addWidget(self.dir_label, 1)
        top_level_layout.addLayout(dir_row)

        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.tree_view = FileExplorer(parent_window=self)
        self.tree_view.setMinimumWidth(180)
        main_splitter.addWidget(self.tree_view)

        right_panel_widget = QWidget()
        right_panel_layout = QVBoxLayout(right_panel_widget)
        right_panel_layout.setContentsMargins(0, 0, 0, 0)
        right_panel_layout.setSpacing(6)
        right_panel_widget.setMinimumWidth(350)
        sp_right = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sp_right.setHorizontalStretch(2)
        right_panel_widget.setSizePolicy(sp_right)

        fm_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.frontmatter_display = FrontmatterTableViewer(self)
        self.frontmatter_display.setMinimumHeight(120)
        fm_splitter.addWidget(self.frontmatter_display)
        self.frontmatter_raw = QTextEdit(self)
        self.frontmatter_raw.setReadOnly(True)
        self.frontmatter_raw.setMinimumWidth(320)
        fm_splitter.addWidget(self.frontmatter_raw)
        fm_splitter.setSizes([500, 320])
        right_panel_layout.addWidget(fm_splitter, 1)
        self.save_fm_btn = QPushButton(
            QCoreApplication.translate("MainWindow", "Frontmatter speichern")
        )
        self.save_fm_btn.clicked.connect(self.save_frontmatter_table)
        right_panel_layout.addWidget(self.save_fm_btn)

        options_row = QHBoxLayout()
        self.dryrun_checkbox = QCheckBox(
            QCoreApplication.translate("MainWindow", "Dry Run")
        )
        self.dryrun_checkbox.setChecked(True)
        self.only_if_key_value_checkbox = QCheckBox(
            QCoreApplication.translate("MainWindow", "Vorbedingung anwenden")
        )
        self.only_if_key_value_checkbox.setChecked(False)
        options_row.addWidget(self.dryrun_checkbox)
        options_row.addWidget(self.only_if_key_value_checkbox)
        options_row.addStretch()
        right_panel_layout.addLayout(options_row)

        self.match_all_checkbox = QCheckBox(
            QCoreApplication.translate("MainWindow", "Alle Elemente müssen matchen")
        )
        self.match_all_checkbox.setChecked(False)
        options_row.addWidget(self.match_all_checkbox)

        param_row = QHBoxLayout()
        self.key_label = QLabel(QCoreApplication.translate("MainWindow", "Key:"))
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Key/Alter Key")
        )
        self.value_label = QLabel(QCoreApplication.translate("MainWindow", "Value:"))
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Value (optional)")
        )
        self.newkey_label = QLabel(
            QCoreApplication.translate("MainWindow", "Neuer Key:")
        )
        self.newkey_input = QLineEdit()
        self.newkey_input.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Neuer Key (für Umbenennen)")
        )
        self.precond_label = QLabel(
            QCoreApplication.translate("MainWindow", "Vorbedingung:")
        )
        self.precondition_key_input = QLineEdit()
        self.precondition_key_input.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Vorbedingung Key")
        )
        self.precondition_value_input = QLineEdit()
        self.precondition_value_input.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Vorbedingung Value")
        )
        param_row.addWidget(self.key_label)
        param_row.addWidget(self.key_input)
        param_row.addWidget(self.value_label)
        param_row.addWidget(self.value_input)
        param_row.addWidget(self.newkey_label)
        param_row.addWidget(self.newkey_input)
        param_row.addWidget(self.precond_label)
        param_row.addWidget(self.precondition_key_input)
        param_row.addWidget(self.precondition_value_input)
        right_panel_layout.addLayout(param_row)

        self.newkey_label.setVisible(False)
        self.newkey_input.setVisible(False)
        self.precond_label.setVisible(self.only_if_key_value_checkbox.isChecked())
        self.precondition_key_input.setVisible(
            self.only_if_key_value_checkbox.isChecked()
        )
        self.precondition_value_input.setVisible(
            self.only_if_key_value_checkbox.isChecked()
        )

        def update_precond_fields_enabled_state():
            enabled = self.only_if_key_value_checkbox.isChecked()
            self.precond_label.setVisible(enabled)
            self.precondition_key_input.setVisible(enabled)
            self.precondition_value_input.setVisible(enabled)
            self.precondition_key_input.setEnabled(enabled)
            self.precondition_value_input.setEnabled(enabled)

        self.only_if_key_value_checkbox.toggled.connect(
            update_precond_fields_enabled_state
        )
        update_precond_fields_enabled_state()

        batch_row1 = QHBoxLayout()
        btn_batch_write = QPushButton(
            QCoreApplication.translate("MainWindow", "Batch: Key/Value schreiben")
        )
        btn_batch_remove = QPushButton(
            QCoreApplication.translate("MainWindow", "Batch: Key löschen")
        )
        btn_batch_rename = QPushButton(
            QCoreApplication.translate("MainWindow", "Batch: Key umbenennen")
        )
        batch_row1.addWidget(btn_batch_write)
        batch_row1.addWidget(btn_batch_remove)
        batch_row1.addWidget(btn_batch_rename)
        right_panel_layout.addLayout(batch_row1)
        batch_row2 = QHBoxLayout()
        btn_batch_check_exists = QPushButton(
            QCoreApplication.translate("MainWindow", "Batch: Key prüfen")
        )
        btn_batch_check_missing = QPushButton(
            QCoreApplication.translate("MainWindow", "Batch: Key fehlt prüfen")
        )
        btn_batch_check_value = QPushButton(
            QCoreApplication.translate("MainWindow", "Batch: Key/Value prüfen")
        )
        btn_batch_delete_files = QPushButton(
            QCoreApplication.translate("MainWindow", "Batch: Dateien löschen (K/V)")
        )
        batch_row2.addWidget(btn_batch_check_exists)
        batch_row2.addWidget(btn_batch_check_missing)
        batch_row2.addWidget(btn_batch_check_value)
        batch_row2.addWidget(btn_batch_delete_files)
        right_panel_layout.addLayout(batch_row2)

        def show_newkey_field(show: bool):
            """Zeigt oder versteckt das Eingabefeld für den neuen Key (bei Umbenennen)."""
            self.newkey_label.setVisible(show)
            self.newkey_input.setVisible(show)

        show_newkey_field(False)

        def batch_write_clicked():
            """Handler für Batch: Key/Value schreiben."""
            show_newkey_field(False)
            self.write_key_value()

        def batch_remove_clicked():
            """Handler für Batch: Key löschen."""
            show_newkey_field(False)
            self.remove_key()

        def batch_rename_clicked():
            """Handler für Batch: Key umbenennen."""
            show_newkey_field(True)
            self.rename_key()

        def batch_check_exists_clicked():
            """Handler für Batch: Key prüfen."""
            show_newkey_field(False)
            self.check_key_exists()

        def batch_check_missing_clicked():
            """Handler für Batch: Key fehlt prüfen."""
            show_newkey_field(False)
            self.check_key_missing()

        def batch_check_value_clicked():
            """Handler für Batch: Key/Value prüfen."""
            show_newkey_field(False)
            self.check_key_value_match()

        def batch_delete_files_clicked():
            """Handler für Batch: Dateien löschen (K/V)."""
            show_newkey_field(False)
            self.delete_files_by_key_value()

        btn_batch_write.clicked.connect(batch_write_clicked)
        btn_batch_remove.clicked.connect(batch_remove_clicked)
        btn_batch_rename.clicked.connect(batch_rename_clicked)
        btn_batch_check_exists.clicked.connect(batch_check_exists_clicked)
        btn_batch_check_missing.clicked.connect(batch_check_missing_clicked)
        btn_batch_check_value.clicked.connect(batch_check_value_clicked)
        btn_batch_delete_files.clicked.connect(batch_delete_files_clicked)

        main_splitter.addWidget(right_panel_widget)
        main_splitter.setSizes([200, 550])
        top_level_layout.addWidget(main_splitter, 1)

        log_row = QHBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setMinimumHeight(80)
        self.log_text.setReadOnly(True)
        self.log_clear_btn = QPushButton(
            QCoreApplication.translate("MainWindow", "Protokoll löschen")
        )
        self.log_clear_btn.setObjectName("logClearButton")
        self.log_clear_btn.clicked.connect(self.clear_log)
        log_row.addWidget(self.log_text, 1)
        log_row.addWidget(self.log_clear_btn)
        top_level_layout.addLayout(log_row)

    def on_file_selected_from_explorer(self, file_path: str | None, is_dir: bool):
        """
        Wird aufgerufen, wenn eine Datei oder ein Ordner im Datei-Explorer ausgewählt wird.
        Zeigt das Frontmatter an oder gibt eine Logmeldung aus.
        """
        if file_path and not is_dir and is_supported_file(file_path):
            self.display_frontmatter_table(file_path)
        else:
            self.frontmatter_display.clear_viewer()
            if file_path and is_dir:
                self.log_message(
                    QCoreApplication.translate(
                        "MainWindow", "Ordner ausgewählt: {folder}"
                    ).format(folder=os.path.basename(file_path))
                )
            elif file_path:
                self.log_message(
                    QCoreApplication.translate(
                        "MainWindow",
                        "Nicht unterstützte Datei/Element ausgewählt: {file}",
                    ).format(file=os.path.basename(file_path))
                )
            elif not file_path:
                self.log_message(
                    QCoreApplication.translate(
                        "MainWindow", "Auswahl im Datei-Explorer aufgehoben."
                    )
                )

    def display_frontmatter_table(self, file_path: str):
        """
        Zeigt das Frontmatter einer Datei in der Tabelle und im Raw-View an.
        """
        import re

        import frontmatter
        import yaml

        self._current_frontmatter_file = file_path
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw = f.read()
                post = frontmatter.loads(raw)
            fm_block = self._extract_frontmatter_block(raw)
            self.frontmatter_raw.setPlainText(fm_block)
            if not post.metadata:
                self.frontmatter_display.clear_viewer()
                self.frontmatter_display.display_frontmatter({})
                self.log_message(
                    QCoreApplication.translate(
                        "MainWindow", "Info: Kein Frontmatter in {file} gefunden."
                    ).format(file=os.path.basename(file_path)),
                    level="warn",
                )
                return
            meta = {}
            for k, v in post.metadata.items():
                if isinstance(v, list):
                    typ = "Liste"
                elif isinstance(v, bool):
                    typ = "Checkbox"
                elif isinstance(v, int) or (isinstance(v, str) and v.isdigit()):
                    typ = "Zahl"
                elif isinstance(v, str):
                    if re.match(r"^\d{4}-\d{2}-\d{2}$", v):
                        typ = "Datum"
                    elif re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}", v):
                        typ = "Datum und Uhrzeit"
                    else:
                        typ = "Text"
                else:
                    typ = "Text"
                meta[k] = (v, typ)
            self.frontmatter_display.display_frontmatter(meta)
        except yaml.YAMLError as ye:
            self.frontmatter_display.clear_viewer()
            self.frontmatter_raw.clear()
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow", "FEHLER: Ungültiges YAML in {file}: {error}"
                ).format(file=os.path.basename(file_path), error=ye),
                level="error",
            )
        except Exception as e:
            self.frontmatter_display.clear_viewer()
            self.frontmatter_raw.clear()
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow", "FEHLER beim Anzeigen von Frontmatter: {error}"
                ).format(error=e),
                level="error",
            )

    def _extract_frontmatter_block(self, raw: str) -> str:
        """
        Extrahiert den ersten --- ... --- Block (YAML Frontmatter) aus dem Text.
        """
        import re

        m = re.search(r"^---\s*\n(.*?\n)---", raw, re.DOTALL | re.MULTILINE)
        if m:
            return f"---\n{m.group(1)}---"
        return ""

    def save_frontmatter_table(self):
        """
        Speichert die Änderungen aus der Frontmatter-Tabelle zurück in die Datei.
        """
        import ast

        import frontmatter

        file_path = getattr(self, "_current_frontmatter_file", None)
        if not file_path:
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow", "Kein Frontmatter-File ausgewählt."
                )
            )
            return
        meta = self.frontmatter_display.get_metadata()
        new_meta = {}
        for k, (v, typ) in meta.items():
            if typ == "Liste":
                try:
                    parsed = ast.literal_eval(v)
                    if isinstance(parsed, list):
                        new_meta[k] = parsed
                    else:
                        new_meta[k] = [str(parsed)]
                except Exception:
                    if "," in v:
                        new_meta[k] = [s.strip() for s in v.split(",") if s.strip()]
                    else:
                        new_meta[k] = [v.strip()] if v.strip() else []
            elif typ == "Zahl":
                try:
                    new_meta[k] = int(v)
                except Exception:
                    new_meta[k] = v
            elif typ == "Checkbox":
                new_meta[k] = v.lower() in ("true", "1", "yes", "x", "checked")
            elif typ == "Datum" or typ == "Datum und Uhrzeit":
                new_meta[k] = v  # Als String speichern
            else:
                new_meta[k] = v
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)
            post.metadata = new_meta
            with open(file_path, "wb") as f:
                frontmatter.dump(post, f, encoding="utf-8")
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow", "Frontmatter gespeichert für {file}."
                ).format(file=os.path.basename(file_path)),
                level="success",
            )
            self.display_frontmatter_table(file_path)
        except Exception as e:
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow", "FEHLER beim Speichern des Frontmatters: {error}"
                ).format(error=e),
                level="error",
            )

    def select_directory(self):
        """
        Öffnet einen Dialog zur Auswahl des Arbeitsverzeichnisses.
        """
        dir_path = QFileDialog.getExistingDirectory(
            self,
            QCoreApplication.translate("MainWindow", "Arbeitsverzeichnis auswählen"),
            self.directory or QDir.homePath(),
        )
        if dir_path:
            self.directory = dir_path
            self.dir_label.setText(dir_path)
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow", "Arbeitsverzeichnis gesetzt: {dir_path}"
                ).format(dir_path=dir_path)
            )
            self.tree_view.set_root_directory(dir_path)
            self.frontmatter_display.clear_viewer()

    def log_message(self, msg: str, level: str = "info"):
        """
        Fügt eine formatierte Log-Nachricht ins Protokoll ein.
        level: info, warn, error, success
        """
        emoji = {
            "info": "ℹ️",
            "warn": "⚠️",
            "error": "❌",
            "success": "✅",
        }.get(level, "ℹ️")
        color = {
            "info": "#7fd7ff",
            "warn": "#ffd966",
            "error": "#fb464c",
            "success": "#b6f77c",
        }.get(level, "#7fd7ff")
        style = {
            "info": "font-weight:normal;",
            "warn": "font-weight:bold;",
            "error": "font-weight:bold;",
            "success": "font-weight:bold;",
        }.get(level, "font-weight:normal;")
        html = f'<span style="color:{color};{style}">{emoji} {msg}</span>'
        self.log_text.append(html)
        if hasattr(self, "status"):
            self.status.showMessage(msg, 5000)
        QApplication.processEvents()

    def clear_log(self):
        """
        Löscht das Protokoll.
        """
        self.log_text.clear()

    def handle_single_file_delete(self, file_path: str):
        """
        Löscht eine einzelne Datei nach Bestätigung (oder im DryRun-Modus nur simuliert).
        """
        if not (file_path and os.path.isfile(file_path)):
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow",
                    "Fehler: Datei '{file_path}' nicht gefunden für Löschaktion.",
                ).format(file_path=file_path),
                level="error",
            )
            return
        dryrun = self.dryrun_checkbox.isChecked() if self.dryrun_checkbox is not None else False
        base_name = os.path.basename(file_path)
        if dryrun:
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow", "[DryRun] Einzel: Datei '{file}' würde gelöscht."
                ).format(file=base_name),
                level="warn",
            )
            return
        reply = QMessageBox.question(
            self,
            QCoreApplication.translate("MainWindow", "Datei löschen bestätigen"),
            QCoreApplication.translate(
                "MainWindow", "Soll die Datei '{filename}' wirklich gelöscht werden?"
            ).format(filename=base_name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(file_path)
                self.log_message(
                    QCoreApplication.translate(
                        "MainWindow", "Einzel: Datei '{file}' ({path}) gelöscht."
                    ).format(file=base_name, path=file_path),
                    level="success",
                )
                self.frontmatter_display.clear_viewer()
            except Exception as e:
                self.log_message(
                    QCoreApplication.translate(
                        "MainWindow", "FEHLER beim Löschen der Datei '{file}': {error}"
                    ).format(file=base_name, error=e),
                    level="error",
                )
        else:
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow", "Einzel: Löschen der Datei '{file}' abgebrochen."
                ).format(file=base_name),
                level="warn",
            )

    def handle_single_file_write_kv(self, file_path: str):
        """
        Öffnet einen Dialog zum Schreiben eines Key/Value-Paares in eine einzelne Datei.
        """
        if not (
            file_path and os.path.isfile(file_path) and is_supported_file(file_path)
        ):
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow",
                    "Fehler: Datei '{file_path}' nicht unterstützt oder nicht gefunden für Key/Value schreiben.",
                ).format(file_path=file_path),
                level="error",
            )
            return

        base_name = os.path.basename(file_path)
        dialog = KeyValueDialog(
            self,
            window_title=QCoreApplication.translate(
                "MainWindow", "Key/Value für '{filename}' schreiben"
            ).format(filename=base_name),
            key_label=QCoreApplication.translate("MainWindow", "Ziel-Key:"),
            value_label=QCoreApplication.translate("MainWindow", "Neuer Wert:"),
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            dialog_values = dialog.get_values()  # Werte aus dem Dialog holen
            if dialog_values:
                key_from_dialog, raw_value_from_dialog = dialog_values
                if not key_from_dialog:
                    QMessageBox.warning(
                        self,
                        QCoreApplication.translate("MainWindow", "Eingabefehler"),
                        QCoreApplication.translate(
                            "MainWindow", "Einzel: Key darf im Dialog nicht leer sein."
                        ),
                    )
                    self.log_message(
                        f"FEHLER: Einzel: Key/Value schreiben für '{base_name}' abgebrochen - Key im Dialog war leer.",
                        level="error",
                    )
                    return

                final_value_to_write: object
                if (
                    isinstance(raw_value_from_dialog, str)
                    and "," in raw_value_from_dialog
                ):
                    final_value_to_write = [
                        s.strip() for s in raw_value_from_dialog.split(",") if s.strip()
                    ]
                else:
                    final_value_to_write = raw_value_from_dialog

                dryrun = self.dryrun_checkbox.isChecked() if self.dryrun_checkbox is not None else False
                try:
                    with open(file_path, "r", encoding="utf-8") as f_in:
                        post = frontmatter.load(f_in)

                    original_value_in_post = post.metadata.get(
                        key_from_dialog
                    )  # Wert aus der Datei holen

                    changed = False
                    if type(original_value_in_post) is not type(final_value_to_write):
                        changed = True
                    elif isinstance(final_value_to_write, list):
                        original_list = (
                            original_value_in_post
                            if isinstance(original_value_in_post, list)
                            else []
                        )
                        if sorted(original_list) != sorted(final_value_to_write):
                            changed = True
                    elif str(original_value_in_post) != str(final_value_to_write):
                        changed = True

                    action_description = f"Key '{key_from_dialog}' auf Wert '{final_value_to_write}' setzen"

                    if changed:
                        if dryrun:
                            self.log_message(
                                f"[DryRun] Einzel: In '{base_name}': {action_description} (Wert war: '{original_value_in_post}').",
                                level="warn",
                            )
                        else:
                            post.metadata[key_from_dialog] = final_value_to_write
                            try:
                                with open(file_path, "wb") as f_out:
                                    frontmatter.dump(post, f_out, encoding="utf-8")
                                self.log_message(
                                    f"Einzel: In '{base_name}': {action_description} (Wert war: '{original_value_in_post}').",
                                    level="success",
                                )
                                self.display_frontmatter_table(file_path)
                            except Exception as save_e:
                                self.log_message(
                                    f"FEHLER beim Speichern (Einzel-Schreiben) von '{base_name}': {save_e}",
                                    level="error",
                                )
                    else:
                        self.log_message(
                            f"Info: Einzel: In '{base_name}': Key '{key_from_dialog}' hat bereits Wert '{original_value_in_post}'. Keine Änderung.",
                            level="warn",
                        )
                except yaml.YAMLError as ye:
                    self.log_message(
                        f"FEHLER: Ungültiges YAML (Einzel-Schreiben) in '{base_name}': {ye}",
                        level="error",
                    )
                except Exception as e:
                    self.log_message(
                        f"FEHLER beim Einzel-Schreiben von Key/Value in '{base_name}': {e}",
                        level="error",
                    )
        else:
            self.log_message(
                f"Einzel: Key/Value schreiben für '{base_name}' abgebrochen (Dialog geschlossen).",
                level="warn",
            )

    def handle_single_file_remove_key(self, file_path: str):
        """
        Öffnet einen Dialog zum Entfernen eines Keys aus einer einzelnen Datei.
        """
        if not (
            file_path and os.path.isfile(file_path) and is_supported_file(file_path)
        ):
            self.log_message(
                f"Fehler: Datei '{file_path}' nicht unterstützt oder nicht gefunden für Key entfernen.",
                level="error",
            )
            return

        base_name = os.path.basename(file_path)
        dialog = KeyDialog(  # Neuer KeyDialog wird verwendet
            self,
            window_title=QCoreApplication.translate(
                "MainWindow", "Key aus '{filename}' entfernen"
            ).format(filename=base_name),
            key_label=QCoreApplication.translate("MainWindow", "Zu löschender Key:"),
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            key_to_delete = dialog.get_key()  # Key aus dem Dialog holen
            if not key_to_delete:  # Prüfen, ob ein Key eingegeben wurde
                QMessageBox.warning(
                    self,
                    QCoreApplication.translate("MainWindow", "Eingabefehler"),
                    QCoreApplication.translate(
                        "MainWindow", "Einzel: Key darf im Dialog nicht leer sein."
                    ),
                )
                self.log_message(
                    f"FEHLER: Einzel: Key entfernen für '{base_name}' abgebrochen - Key im Dialog war leer.",
                    level="error",
                )
                return
            dryrun = self.dryrun_checkbox.isChecked() if self.dryrun_checkbox is not None else False
            try:
                with open(file_path, "r", encoding="utf-8") as f_in:
                    post = frontmatter.load(f_in)

                if key_to_delete in post.metadata:
                    original_value = post.metadata[key_to_delete]
                    if dryrun:
                        self.log_message(
                            f"[DryRun] Einzel: In '{base_name}': Key '{key_to_delete}' (Wert: '{original_value}') würde gelöscht.",
                            level="warn",
                        )
                    else:
                        del post.metadata[key_to_delete]
                        try:
                            with open(file_path, "wb") as f_out:
                                frontmatter.dump(post, f_out, encoding="utf-8")
                            self.log_message(
                                f"Einzel: In '{base_name}': Key '{key_to_delete}' gelöscht. (Wert war: '{original_value}')",
                                level="success",
                            )
                            self.display_frontmatter_table(file_path)
                        except Exception as save_e:
                            self.log_message(
                                f"FEHLER beim Speichern (Einzel-Löschen) von '{base_name}': {save_e}",
                                level="error",
                            )
                else:
                    self.log_message(
                        f"Info: Einzel: In '{base_name}': Key '{key_to_delete}' nicht gefunden. Keine Änderung.",
                        level="warn",
                    )
            except yaml.YAMLError as ye:
                self.log_message(
                    f"FEHLER: Ungültiges YAML (Einzel-Löschen) in '{base_name}': {ye}",
                    level="error",
                )
            except Exception as e:
                self.log_message(
                    f"FEHLER beim Einzel-Löschen von Key '{key_to_delete}' in '{base_name}': {e}",
                    level="error",
                )
        else:
            self.log_message(
                f"Einzel: Key entfernen für '{base_name}' abgebrochen (Dialog geschlossen).",
                level="warn",
            )

    def set_directory_from_tree(self, dir_path: str):
        """
        Setzt das Arbeitsverzeichnis über die TreeView-Auswahl.
        """
        if os.path.isdir(dir_path):
            self.directory = dir_path
            self.dir_label.setText(dir_path)
            self.log_message(
                f"Arbeitsverzeichnis auf '{os.path.basename(dir_path)}' gesetzt (via TreeView)."
            )
            self.tree_view.set_root_directory(dir_path)
            self.frontmatter_display.clear_viewer()

    def get_files(self):
        """
        Gibt eine Liste aller unterstützten Dateien im aktuellen Arbeitsverzeichnis zurück.
        """
        if not self.directory:
            self.log_message("BATCH: Kein Arbeitsverzeichnis ausgewählt!")
            return []
        file_list = []
        for root, _, files_in_dir in os.walk(self.directory):
            for f_name in files_in_dir:
                if is_supported_file(f_name):
                    file_list.append(os.path.join(root, f_name))
        return file_list

    def _iterate_files_with_action(self, action_instance: BaseAction):
        """
        Führt eine Batch-Aktion auf allen passenden Dateien im Arbeitsverzeichnis aus.
        """
        effective_action_name = action_instance.get_description()
        files_to_process = self.get_files()
        if not files_to_process:
            self.log_message(
                f"{effective_action_name}: Keine passenden Dateien gefunden."
            )
            return

        modified_count = 0
        self.log_message(f"--- Starte {effective_action_name} ---")
        if action_instance.is_dry_run:
            self.log_message(f"[DRY RUN MODUS AKTIV FÜR {effective_action_name}]")

        only_if_key_value = self.only_if_key_value_checkbox.isChecked()
        precondition_key_ui = self.precondition_key_input.text().strip()
        precondition_value_ui = self.precondition_value_input.text().strip()

        for file_path in files_to_process:
            base_name = os.path.basename(file_path)
            try:
                with open(file_path, "r", encoding="utf-8") as f_handle:
                    post = frontmatter.load(f_handle)

                if only_if_key_value:
                    cond_key_to_check = precondition_key_ui
                    cond_value_to_check = precondition_value_ui
                    match_all = self.match_all_checkbox.isChecked()
                    if not cond_key_to_check:
                        pass
                    elif cond_key_to_check not in post.metadata:
                        continue
                    elif not value_matches(
                        post.metadata[cond_key_to_check],
                        cond_value_to_check,
                        match_all_in_list=match_all,
                    ):
                        continue

                made_change, _ = action_instance.process_file(post, file_path)

                if made_change:
                    modified_count += 1
            except yaml.YAMLError as ye:
                self.log_message(
                    f"FEHLER: Ungültiges YAML ({effective_action_name}) in {base_name}: {ye}"
                )
            except Exception as e:
                self.log_message(
                    f"FEHLER ({effective_action_name}) bei {base_name}: {e}"
                )

        self.log_message(
            f"--- {effective_action_name} beendet. {modified_count} Dateien betroffen. ---"
        )

    def remove_key(self):
        """
        Batch-Handler: Entfernt einen Key aus allen passenden Dateien.
        """
        key_to_delete = self.key_input.text().strip()
        if not key_to_delete:
            QMessageBox.warning(
                self,
                QCoreApplication.translate("MainWindow", "Eingabefehler"),
                QCoreApplication.translate(
                    "MainWindow", "Batch Key entfernen: Bitte Key angeben."
                ),
            )
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow", "Batch Key entfernen: Key muss angegeben werden!"
                )
            )
            return
        params = {"key": key_to_delete}
        is_dry_run = self.dryrun_checkbox.isChecked() if self.dryrun_checkbox is not None else False
        action = DeleteKeyAction(
            logger_func=self.log_message, params=params, dry_run=is_dry_run
        )
        self._iterate_files_with_action(action_instance=action)

    def write_key_value(self):
        """
        Batch-Handler: Schreibt ein Key/Value-Paar in alle passenden Dateien.
        """
        key_to_write = self.key_input.text().strip()
        value_to_write = self.value_input.text().strip()

        if not key_to_write:
            QMessageBox.warning(
                self,
                QCoreApplication.translate("MainWindow", "Eingabefehler"),
                QCoreApplication.translate(
                    "MainWindow", "Batch Key/Value schreiben: Bitte Key angeben."
                ),
            )
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow",
                    "Batch Key/Value schreiben: Key muss angegeben werden!",
                )
            )
            return

        params = {"key": key_to_write, "value": value_to_write}
        is_dry_run = self.dryrun_checkbox.isChecked() if self.dryrun_checkbox is not None else False

        action = WriteKeyValueAction(
            logger_func=self.log_message, params=params, dry_run=is_dry_run
        )

        self._iterate_files_with_action(action_instance=action)

    def rename_key(self):
        """
        Batch-Handler: Bennent einen Key in allen passenden Dateien um.
        """
        old_key_name = self.key_input.text().strip()
        new_key_name = self.newkey_input.text().strip()

        if not old_key_name:
            QMessageBox.warning(
                self,
                QCoreApplication.translate("MainWindow", "Eingabefehler"),
                QCoreApplication.translate(
                    "MainWindow",
                    "Batch Key umbenennen: Bitte 'Alten Key' (im Feld 'Key/Alter Key') angeben.",
                ),
            )
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow", "Batch Key umbenennen: 'Alter Key' fehlt!"
                )
            )
            return
        if not new_key_name:
            QMessageBox.warning(
                self,
                QCoreApplication.translate("MainWindow", "Eingabefehler"),
                QCoreApplication.translate(
                    "MainWindow", "Batch Key umbenennen: Bitte 'Neuen Key' angeben."
                ),
            )
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow", "Batch Key umbenennen: 'Neuer Key' fehlt!"
                )
            )
            return

        if old_key_name == new_key_name:
            QMessageBox.information(
                self,
                QCoreApplication.translate("MainWindow", "Info"),
                QCoreApplication.translate(
                    "MainWindow",
                    "Batch Key umbenennen: Alter und neuer Key sind identisch. Keine Aktion notwendig.",
                ),
            )
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow",
                    "Batch Key umbenennen: Alter und neuer Key sind identisch.",
                )
            )
            return

        params = {"old_key": old_key_name, "new_key": new_key_name}
        is_dry_run = self.dryrun_checkbox.isChecked() if self.dryrun_checkbox is not None else False

        action_instance = RenameKeyAction(
            logger_func=self.log_message, params=params, dry_run=is_dry_run
        )

        self._iterate_files_with_action(action_instance=action_instance)

    def delete_files_by_key_value(self):
        """
        Batch-Handler: Löscht alle Dateien, die ein bestimmtes Key/Value-Paar enthalten.
        """
        key_to_match = self.key_input.text().strip()
        value_to_match = self.value_input.text().strip()
        is_dry_run = self.dryrun_checkbox.isChecked() if self.dryrun_checkbox is not None else False

        if not key_to_match or not value_to_match:
            QMessageBox.warning(
                self,
                QCoreApplication.translate("MainWindow", "Eingabefehler"),
                QCoreApplication.translate(
                    "MainWindow",
                    "Batch Dateien löschen: Key und Value müssen angegeben werden!",
                ),
            )
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow", "Batch Dateien löschen: Key und Value fehlen!"
                )
            )
            return

        if not is_dry_run:
            reply = QMessageBox.question(
                self,
                QCoreApplication.translate("MainWindow", "Löschen bestätigen (Batch)"),
                QCoreApplication.translate(
                    "MainWindow",
                    "Sind Sie sicher, dass Sie alle Dateien löschen wollen, \nderen Frontmatter '{key}: {value}' enthält?\nDiese Aktion kann nicht rückgängig gemacht werden!",
                ).format(key=key_to_match, value=value_to_match),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.No:
                self.log_message(
                    QCoreApplication.translate(
                        "MainWindow", "Batch Löschvorgang abgebrochen."
                    )
                )
                return

        params = {"key": key_to_match, "value": value_to_match}

        action_instance = DeleteFilesByKeyValueAction(
            logger_func=self.log_message,
            params=params,
            dry_run=is_dry_run,
        )

        self._iterate_files_with_action(action_instance=action_instance)

    def check_key_exists(self):
        """
        Batch-Handler: Prüft, ob ein Key in den Dateien existiert.
        """
        key_to_check = self.key_input.text().strip()
        if not key_to_check:
            QMessageBox.warning(
                self,
                QCoreApplication.translate("MainWindow", "Eingabefehler"),
                QCoreApplication.translate(
                    "MainWindow", "Batch Key prüfen: Key muss angegeben werden!"
                ),
            )
            self.log_message(
                QCoreApplication.translate("MainWindow", "Batch Key prüfen: Key fehlt!")
            )
            return

        params = {"key": key_to_check}
        is_dry_run = self.dryrun_checkbox.isChecked() if self.dryrun_checkbox is not None else False

        action_instance = CheckKeyExistsAction(
            logger_func=self.log_message, params=params, dry_run=is_dry_run
        )
        self._iterate_files_with_action(action_instance=action_instance)

    def check_key_missing(self):
        """
        Batch-Handler: Prüft, ob ein Key in den Dateien fehlt.
        """
        key_to_check = self.key_input.text().strip()
        if not key_to_check:
            QMessageBox.warning(
                self,
                QCoreApplication.translate("MainWindow", "Eingabefehler"),
                QCoreApplication.translate(
                    "MainWindow", "Batch Key fehlt prüfen: Key muss angegeben werden!"
                ),
            )
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow", "Batch Key fehlt prüfen: Key fehlt!"
                )
            )
            return

        params = {"key": key_to_check}
        is_dry_run = self.dryrun_checkbox.isChecked() if self.dryrun_checkbox is not None else False

        action_instance = CheckKeyMissingAction(
            logger_func=self.log_message, params=params, dry_run=is_dry_run
        )
        self._iterate_files_with_action(action_instance=action_instance)

    def check_key_value_match(self):
        """
        Batch-Handler: Prüft, ob ein Key einen bestimmten Wert hat.
        """
        key_to_check = self.key_input.text().strip()
        value_to_match = self.value_input.text().strip()

        if not key_to_check:
            QMessageBox.warning(
                self,
                QCoreApplication.translate("MainWindow", "Eingabefehler"),
                QCoreApplication.translate(
                    "MainWindow", "Batch Key/Value prüfen: Key muss angegeben werden!"
                ),
            )
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow", "Batch Key/Value prüfen: Key fehlt!"
                )
            )
            return
        if not value_to_match:
            QMessageBox.warning(
                self,
                QCoreApplication.translate("MainWindow", "Eingabefehler"),
                QCoreApplication.translate(
                    "MainWindow", "Batch Key/Value prüfen: Value muss angegeben werden!"
                ),
            )
            self.log_message(
                QCoreApplication.translate(
                    "MainWindow", "Batch Key/Value prüfen: Value fehlt!"
                )
            )
            return

        params = {"key": key_to_check, "value": value_to_match}
        is_dry_run = self.dryrun_checkbox.isChecked() if self.dryrun_checkbox is not None else False

        action_instance = CheckKeyValueMatchAction(
            logger_func=self.log_message, params=params, dry_run=is_dry_run
        )
        self._iterate_files_with_action(action_instance=action_instance)

    def _placeholder_batch_operation(self, action_name):
        """
        Platzhalter für noch nicht umgestellte Batch-Operationen.
        """
        QMessageBox.information(
            self,
            QCoreApplication.translate("MainWindow", "Noch nicht implementiert"),
            QCoreApplication.translate(
                "MainWindow",
                "Die Batch-Aktion '{action}' muss noch auf die neue Aktionsklassen-Struktur umgestellt werden.",
            ).format(action=action_name),
        )
        self.log_message(
            QCoreApplication.translate(
                "MainWindow",
                "Batch-Aktion '{action}' ist noch nicht auf die neue Struktur umgestellt.",
            ).format(action=action_name)
        )

    def handle_single_file_rename_key(self, file_path: str):
        """
        Öffnet einen Dialog zum Umbenennen eines Keys in einer einzelnen Datei.
        """
        if not (
            file_path and os.path.isfile(file_path) and is_supported_file(file_path)
        ):
            self.log_message(
                f"Fehler: Datei '{file_path}' nicht unterstützt oder nicht gefunden für Key umbenennen."
            )
            return
        base_name = os.path.basename(file_path)
        dialog = RenameKeyDialog(
            self,
            window_title=QCoreApplication.translate(
                "MainWindow", "Key umbenennen in '{filename}'"
            ).format(filename=base_name),
            old_key_label=QCoreApplication.translate("MainWindow", "Alter Key:"),
            new_key_label=QCoreApplication.translate("MainWindow", "Neuer Key:"),
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            keys = dialog.get_keys()
            if keys:
                old_key, new_key = keys
                if not old_key or not new_key:
                    QMessageBox.warning(
                        self,
                        QCoreApplication.translate("MainWindow", "Eingabefehler"),
                        QCoreApplication.translate(
                            "MainWindow", "Beide Felder müssen ausgefüllt sein."
                        ),
                    )
                    self.log_message(
                        f"FEHLER: Einzel: Key umbenennen für '{base_name}' abgebrochen - Key im Dialog war leer.",
                        level="error",
                    )
                    return
                if old_key == new_key:
                    QMessageBox.information(
                        self,
                        QCoreApplication.translate("MainWindow", "Info"),
                        QCoreApplication.translate(
                            "MainWindow",
                            "Alter und neuer Key sind identisch. Keine Änderung.",
                        ),
                    )
                    self.log_message(
                        f"Info: Einzel: In '{base_name}': Alter und neuer Key identisch. Keine Änderung.",
                        level="warn",
                    )
                    return
                dryrun = self.dryrun_checkbox.isChecked() if self.dryrun_checkbox is not None else False
                try:
                    with open(file_path, "r", encoding="utf-8") as f_in:
                        post = frontmatter.load(f_in)
                    if old_key not in post.metadata:
                        self.log_message(
                            f"Info: Einzel: In '{base_name}': Alter Key '{old_key}' nicht gefunden. Keine Änderung.",
                            level="warn",
                        )
                        return
                    value_to_move = post.metadata[old_key]
                    if dryrun:
                        self.log_message(
                            f"[DryRun] Einzel: In '{base_name}': Key '{old_key}' würde zu '{new_key}' umbenannt (Wert: '{value_to_move}').",
                            level="warn",
                        )
                    else:
                        del post.metadata[old_key]
                        post.metadata[new_key] = value_to_move
                        try:
                            with open(file_path, "wb") as f_out:
                                frontmatter.dump(post, f_out, encoding="utf-8")
                            self.log_message(
                                f"Einzel: In '{base_name}': Key '{old_key}' zu '{new_key}' umbenannt (Wert: '{value_to_move}').",
                                level="success",
                            )
                            self.display_frontmatter_table(file_path)
                        except Exception as save_e:
                            self.log_message(
                                f"FEHLER beim Speichern (Einzel-Umbenennen) von '{base_name}': {save_e}",
                                level="error",
                            )
                except yaml.YAMLError as ye:
                    self.log_message(
                        f"FEHLER: Ungültiges YAML (Einzel-Umbenennen) in '{base_name}': {ye}",
                        level="error",
                    )
                except Exception as e:
                    self.log_message(
                        f"FEHLER beim Einzel-Umbenennen von Key in '{base_name}': {e}",
                        level="error",
                    )
        else:
            self.log_message(
                f"Einzel: Key umbenennen für '{base_name}' abgebrochen (Dialog geschlossen).",
                level="warn",
            )
