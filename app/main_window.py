import os

import frontmatter
import yaml
from PySide6.QtCore import QDir, Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from .core.actions import (
    CheckKeyExistsAction,
    CheckKeyMissingAction,
    CheckKeyValueMatchAction,
    DeleteFilesByKeyValueAction,
    DeleteKeyAction,
    RenameKeyAction,
    WriteKeyValueAction,
)
from .core.actions.base_action import BaseAction
from .core.utils import is_supported_file
from .styles.cyberpunk_theme import get_cyberpunk_stylesheet
from .ui_components.file_explorer import FileExplorer
from .ui_components.frontmatter_viewer import FrontmatterViewer
from .ui_components.dialogs import KeyValueDialog, KeyDialog

class FrontmatterTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Frontmatter Tool (PySide6 - Modular v4)")
        self.setGeometry(100, 100, 950, 750)
        self.directory = ""

        self.init_ui()
        self.setStyleSheet(get_cyberpunk_stylesheet())

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        top_level_layout = QVBoxLayout(main_widget)
        top_level_layout.setContentsMargins(10, 10, 10, 10)
        top_level_layout.setSpacing(8)

        dir_group = QGroupBox("Arbeitsverzeichnis")
        dir_layout = QHBoxLayout()
        self.dir_label = QLabel("Kein Verzeichnis ausgewählt")
        self.dir_label.setStyleSheet("font-style: italic;")
        dir_btn = QPushButton("Verzeichnis auswählen")
        dir_btn.clicked.connect(self.select_directory)
        dir_layout.addWidget(dir_btn)
        dir_layout.addWidget(self.dir_label, 1)
        dir_group.setLayout(dir_layout)
        top_level_layout.addWidget(dir_group)

        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        self.tree_view = FileExplorer(parent_window=self)
        main_splitter.addWidget(self.tree_view)

        right_panel_widget = QWidget()
        sp_right = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sp_right.setHorizontalStretch(2)
        right_panel_widget.setSizePolicy(sp_right)
        right_panel_main_layout = QVBoxLayout(right_panel_widget)
        right_panel_main_layout.setContentsMargins(0, 0, 0, 0)
        right_panel_main_layout.setSpacing(8)

        fm_display_group = QGroupBox("Frontmatter der ausgewählten Datei")
        fm_display_layout = QVBoxLayout()
        self.frontmatter_display = FrontmatterViewer(self)
        fm_display_layout.addWidget(self.frontmatter_display)
        fm_display_group.setLayout(fm_display_layout)
        right_panel_main_layout.addWidget(fm_display_group, 1)

        param_group = QGroupBox("Globale Parameter für Batch-Aktionen")
        param_fields_layout = QVBoxLayout()
        key_value_row_layout = QHBoxLayout()
        key_value_row_layout.addWidget(QLabel("Key/Alter Key:"))
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("z.B. status / old_tag")
        key_value_row_layout.addWidget(self.key_input)
        key_value_row_layout.addWidget(QLabel("Value:"))
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Value (optional)")
        key_value_row_layout.addWidget(self.value_input)
        param_fields_layout.addLayout(key_value_row_layout)
        new_key_row_layout = QHBoxLayout()
        new_key_row_layout.addWidget(QLabel("Neuer Key:"))
        self.newkey_input = QLineEdit()
        self.newkey_input.setPlaceholderText("Neuer Key (für Umbenennen)")
        new_key_row_layout.addWidget(self.newkey_input)
        param_fields_layout.addLayout(new_key_row_layout)
        param_group.setLayout(param_fields_layout)
        right_panel_main_layout.addWidget(param_group)

        precond_group = QGroupBox("Vorbedingung für Batch-Aktionen (optional)")
        precond_layout = QHBoxLayout()
        self.precondition_key_input = QLineEdit()
        self.precondition_key_input.setPlaceholderText("Vorbedingung Key")
        self.precondition_value_input = QLineEdit()
        self.precondition_value_input.setPlaceholderText("Vorbedingung Value")
        precond_layout.addWidget(self.precondition_key_input)
        precond_layout.addWidget(self.precondition_value_input)
        precond_group.setLayout(precond_layout)
        right_panel_main_layout.addWidget(precond_group)

        options_group = QGroupBox("Globale Optionen")
        options_layout = QHBoxLayout()
        self.dryrun_checkbox = QCheckBox("Dry Run (Batch & Einzel)")
        self.dryrun_checkbox.setChecked(True)
        self.only_if_key_value_checkbox = QCheckBox("Vorbedingung für Batch anwenden")
        self.only_if_key_value_checkbox.setChecked(False)

        def update_precond_fields_enabled_state():
            enabled = self.only_if_key_value_checkbox.isChecked()
            self.precondition_key_input.setEnabled(enabled)
            self.precondition_value_input.setEnabled(enabled)

        self.only_if_key_value_checkbox.toggled.connect(
            update_precond_fields_enabled_state
        )
        update_precond_fields_enabled_state()
        options_layout.addWidget(self.dryrun_checkbox)
        options_layout.addWidget(self.only_if_key_value_checkbox)
        options_layout.addStretch()
        options_group.setLayout(options_layout)
        right_panel_main_layout.addWidget(options_group)

        batch_actions_group = QGroupBox(
            "Globale Batch-Aktionen (auf alle Dateien im Verzeichnis)"
        )
        batch_actions_main_layout = QVBoxLayout()
        actions_layout_row1 = QHBoxLayout()
        btn_batch_write = QPushButton("Batch: Key/Value schreiben")
        btn_batch_remove = QPushButton("Batch: Key löschen")
        btn_batch_rename = QPushButton("Batch: Key umbenennen")
        actions_layout_row1.addWidget(btn_batch_write)
        actions_layout_row1.addWidget(btn_batch_remove)
        actions_layout_row1.addWidget(btn_batch_rename)
        batch_actions_main_layout.addLayout(actions_layout_row1)
        actions_layout_row2 = QHBoxLayout()
        btn_batch_check_exists = QPushButton("Batch: Key prüfen")
        btn_batch_check_missing = QPushButton("Batch: Key fehlt prüfen")
        btn_batch_check_value = QPushButton("Batch: Key/Value prüfen")
        btn_batch_delete_files = QPushButton("Batch: Dateien löschen (K/V)")
        actions_layout_row2.addWidget(btn_batch_check_exists)
        actions_layout_row2.addWidget(btn_batch_check_missing)
        actions_layout_row2.addWidget(btn_batch_check_value)
        actions_layout_row2.addWidget(btn_batch_delete_files)
        batch_actions_main_layout.addLayout(actions_layout_row2)
        batch_actions_group.setLayout(batch_actions_main_layout)
        right_panel_main_layout.addWidget(batch_actions_group)

        btn_batch_delete_files.clicked.connect(self.delete_files_by_key_value)
        btn_batch_write.clicked.connect(self.write_key_value)
        btn_batch_remove.clicked.connect(self.remove_key)
        btn_batch_rename.clicked.connect(self.rename_key)
        btn_batch_check_exists.clicked.connect(self.check_key_exists)
        btn_batch_check_missing.clicked.connect(self.check_key_missing)
        btn_batch_check_value.clicked.connect(self.check_key_value_match)

        main_splitter.addWidget(right_panel_widget)
        main_splitter.setSizes([250, 550])
        top_level_layout.addWidget(main_splitter, 1)

        log_group = QGroupBox("Protokoll")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_clear_btn = QPushButton("Protokoll löschen")
        self.log_clear_btn.setObjectName("logClearButton")
        self.log_clear_btn.clicked.connect(self.clear_log)
        log_layout.addWidget(self.log_text)
        log_layout.addWidget(self.log_clear_btn, alignment=Qt.AlignmentFlag.AlignRight)
        log_group.setLayout(log_layout)
        top_level_layout.addWidget(log_group, 0)

    def on_file_selected_from_explorer(self, file_path: str | None, is_dir: bool):
        if file_path and not is_dir and is_supported_file(file_path):
            self.frontmatter_display.display_frontmatter(file_path, self.log_message)
        else:
            self.frontmatter_display.clear_viewer()
            if file_path and is_dir:
                self.log_message(f"Ordner ausgewählt: {os.path.basename(file_path)}")
            elif file_path:
                self.log_message(
                    f"Nicht unterstützte Datei/Element ausgewählt: {os.path.basename(file_path)}"
                )
            elif not file_path:
                self.log_message("Auswahl im Datei-Explorer aufgehoben.")

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "Arbeitsverzeichnis auswählen", self.directory or QDir.homePath()
        )
        if dir_path:
            self.directory = dir_path
            self.dir_label.setText(dir_path)
            self.log_message(f"Arbeitsverzeichnis gesetzt: {dir_path}")
            self.tree_view.set_root_directory(dir_path)
            self.frontmatter_display.clear_viewer()

    def log_message(self, msg: str):
        self.log_text.append(msg)
        QApplication.processEvents()

    def clear_log(self):
        self.log_text.clear()

    def handle_single_file_delete(self, file_path: str):
        if not (file_path and os.path.isfile(file_path)):
            self.log_message(
                f"Fehler: Datei '{file_path}' nicht gefunden für Löschaktion."
            )
            return
        dryrun = self.dryrun_checkbox.isChecked()
        base_name = os.path.basename(file_path)
        if dryrun:
            self.log_message(f"[DryRun] Einzel: Datei '{base_name}' würde gelöscht.")
            return
        reply = QMessageBox.question(
            self,
            "Datei löschen bestätigen",
            f"Soll die Datei '{base_name}' wirklich gelöscht werden?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(file_path)
                self.log_message(f"Einzel: Datei '{base_name}' ({file_path}) gelöscht.")
                self.frontmatter_display.clear_viewer()
            except Exception as e:
                self.log_message(f"Fehler beim Löschen der Datei '{base_name}': {e}")
        else:
            self.log_message(f"Einzel: Löschen der Datei '{base_name}' abgebrochen.")

    def handle_single_file_write_kv(self, file_path: str):
        if not (
            file_path and os.path.isfile(file_path) and is_supported_file(file_path)
        ):
            self.log_message(
                f"Fehler: Datei '{file_path}' nicht unterstützt oder nicht gefunden für Key/Value schreiben."
            )
            return

        base_name = os.path.basename(file_path)
        dialog = KeyValueDialog(
            self,
            window_title=f"Key/Value für '{base_name}' schreiben",
            key_label="Ziel-Key:", # Klarere Beschriftung
            value_label="Neuer Wert:"
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.get_values()
            if values:
                key, value = values

                if not key:
                    QMessageBox.warning(self, "Eingabefehler", "Einzel: Key darf im Dialog nicht leer sein.")
                    self.log_message(f"Einzel: Key/Value schreiben für '{base_name}' abgebrochen - Key im Dialog war leer.")
                    return

                dryrun = self.dryrun_checkbox.isChecked()
                try:
                    with open(file_path, "r", encoding="utf-8") as f_in:
                        post = frontmatter.load(f_in)
                    original_value = post.metadata.get(key)
                    action_description = f"Key '{key}' auf Wert '{value}' setzen"

                    if str(original_value) != str(value):
                        if dryrun:
                            self.log_message(f"[DryRun] Einzel: In '{base_name}': {action_description} (Wert war: '{original_value}').")
                        else:
                            post.metadata[key] = value
                            try:
                                with open(file_path, 'wb') as f_out:
                                    frontmatter.dump(post, f_out, encoding='utf-8')
                                self.log_message(f"Einzel: In '{base_name}': {action_description} (Wert war: '{original_value}').")
                                self.frontmatter_display.display_frontmatter(file_path, self.log_message)
                            except Exception as save_e:
                                self.log_message(f"FEHLER beim Speichern (Einzel-Schreiben) von '{base_name}': {save_e}")
                    else:
                        self.log_message(f"Einzel: In '{base_name}': Key '{key}' hat bereits Wert '{value}'. Nichts geändert.")
                except yaml.YAMLError as ye:
                    self.log_message(f"FEHLER: Ungültiges YAML (Einzel-Schreiben) in '{base_name}': {ye}")
                except Exception as e:
                    self.log_message(f"Fehler beim Einzel-Schreiben von Key/Value in '{base_name}': {e}")
            # else-Block für "keine Werte vom Dialog" ist hier weniger relevant, da get_values() None nur bei Reject zurückgibt
        else:
            self.log_message(f"Einzel: Key/Value schreiben für '{base_name}' abgebrochen (Dialog geschlossen).")

    def handle_single_file_remove_key(self, file_path: str):
        if not (file_path and os.path.isfile(file_path) and is_supported_file(file_path)):
            self.log_message(f"Fehler: Datei '{file_path}' nicht unterstützt oder nicht gefunden für Key entfernen.")
            return

        base_name = os.path.basename(file_path)
        dialog = KeyDialog( # Neuer KeyDialog wird verwendet
            self,
            window_title=f"Key aus '{base_name}' entfernen",
            key_label="Zu löschender Key:"
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            key_to_delete = dialog.get_key() # Key aus dem Dialog holen

            if not key_to_delete: # Prüfen, ob ein Key eingegeben wurde
                QMessageBox.warning(self, "Eingabefehler", "Einzel: Key darf im Dialog nicht leer sein.")
                self.log_message(f"Einzel: Key entfernen für '{base_name}' abgebrochen - Key im Dialog war leer.")
                return

            dryrun = self.dryrun_checkbox.isChecked()
            try:
                # Ladeoperation MUSS hier innerhalb des try-Blocks sein
                with open(file_path, "r", encoding="utf-8") as f_in:
                    post = frontmatter.load(f_in)

                if key_to_delete in post.metadata:
                    original_value = post.metadata[key_to_delete]
                    if dryrun:
                        self.log_message(f"[DryRun] Einzel: In '{base_name}': Key '{key_to_delete}' (Wert: '{original_value}') würde gelöscht.")
                    else:
                        del post.metadata[key_to_delete]
                        try:
                            with open(file_path, "wb") as f_out:
                                frontmatter.dump(post, f_out, encoding="utf-8")
                            self.log_message(f"Einzel: In '{base_name}': Key '{key_to_delete}' gelöscht.")
                            self.frontmatter_display.display_frontmatter(file_path, self.log_message)
                        except Exception as save_e:
                            self.log_message(f"FEHLER beim Speichern (Einzel-Löschen) von '{base_name}': {save_e}")
                else:
                    self.log_message(f"Einzel: In '{base_name}': Key '{key_to_delete}' nicht gefunden. Nichts gelöscht.")

            except yaml.YAMLError as ye:
                self.log_message(f"FEHLER: Ungültiges YAML (Einzel-Löschen) in '{base_name}': {ye}")
            except Exception as e:
                self.log_message(f"Fehler beim Einzel-Löschen von Key '{key_to_delete}' in '{base_name}': {e}")
        else:
            self.log_message(f"Einzel: Key entfernen für '{base_name}' abgebrochen (Dialog geschlossen).")

    def set_directory_from_tree(self, dir_path: str):
        if os.path.isdir(dir_path):
            self.directory = dir_path
            self.dir_label.setText(dir_path)
            self.log_message(
                f"Arbeitsverzeichnis auf '{os.path.basename(dir_path)}' gesetzt (via TreeView)."
            )
            self.tree_view.set_root_directory(dir_path)
            self.frontmatter_display.clear_viewer()

    def get_files(self):
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
                    if not cond_key_to_check:
                        pass
                    elif not (
                        cond_key_to_check in post.metadata
                        and str(post.metadata[cond_key_to_check])
                        == str(cond_value_to_check)
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
        key_to_delete = self.key_input.text().strip()
        if not key_to_delete:
            QMessageBox.warning(
                self, "Eingabefehler", "Batch Key entfernen: Bitte Key angeben."
            )
            self.log_message("Batch Key entfernen: Key muss angegeben werden!")
            return
        params = {"key": key_to_delete}
        is_dry_run = self.dryrun_checkbox.isChecked()
        action = DeleteKeyAction(
            logger_func=self.log_message, params=params, dry_run=is_dry_run
        )
        self._iterate_files_with_action(action_instance=action)

    def write_key_value(self):
        key_to_write = self.key_input.text().strip()
        value_to_write = self.value_input.text().strip()

        if not key_to_write:
            QMessageBox.warning(
                self, "Eingabefehler", "Batch Key/Value schreiben: Bitte Key angeben."
            )
            self.log_message("Batch Key/Value schreiben: Key muss angegeben werden!")
            return

        params = {"key": key_to_write, "value": value_to_write}
        is_dry_run = self.dryrun_checkbox.isChecked()

        action = WriteKeyValueAction(
            logger_func=self.log_message, params=params, dry_run=is_dry_run
        )

        self._iterate_files_with_action(action_instance=action)

    def rename_key(self):
        old_key_name = self.key_input.text().strip()
        new_key_name = self.newkey_input.text().strip()

        if not old_key_name:
            QMessageBox.warning(
                self,
                "Eingabefehler",
                "Batch Key umbenennen: Bitte 'Alten Key' (im Feld 'Key/Alter Key') angeben.",
            )
            self.log_message("Batch Key umbenennen: 'Alter Key' fehlt!")
            return
        if not new_key_name:
            QMessageBox.warning(
                self,
                "Eingabefehler",
                "Batch Key umbenennen: Bitte 'Neuen Key' angeben.",
            )
            self.log_message("Batch Key umbenennen: 'Neuer Key' fehlt!")
            return

        if old_key_name == new_key_name:
            QMessageBox.information(
                self,
                "Info",
                "Batch Key umbenennen: Alter und neuer Key sind identisch. Keine Aktion notwendig.",
            )
            self.log_message(
                "Batch Key umbenennen: Alter und neuer Key sind identisch."
            )
            return

        params = {"old_key": old_key_name, "new_key": new_key_name}
        is_dry_run = self.dryrun_checkbox.isChecked()

        action_instance = RenameKeyAction(
            logger_func=self.log_message, params=params, dry_run=is_dry_run
        )

        self._iterate_files_with_action(action_instance=action_instance)

    def delete_files_by_key_value(self):
        key_to_match = self.key_input.text().strip()
        value_to_match = self.value_input.text().strip()
        is_dry_run = self.dryrun_checkbox.isChecked()

        if not key_to_match or not value_to_match:
            QMessageBox.warning(
                self,
                "Eingabefehler",
                "Batch Dateien löschen: Key und Value müssen angegeben werden!",
            )
            self.log_message("Batch Dateien löschen: Key und Value fehlen!")
            return

        if not is_dry_run:
            reply = QMessageBox.question(
                self,
                "Löschen bestätigen (Batch)",
                f"Sind Sie sicher, dass Sie alle Dateien löschen wollen, \n"
                f"deren Frontmatter '{key_to_match}: {value_to_match}' enthält?\n"
                f"Diese Aktion kann nicht rückgängig gemacht werden!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.No:
                self.log_message("Batch Löschvorgang abgebrochen.")
                return

        params = {"key": key_to_match, "value": value_to_match}

        action_instance = DeleteFilesByKeyValueAction(
            logger_func=self.log_message,
            params=params,
            dry_run=is_dry_run,
        )

        self._iterate_files_with_action(action_instance=action_instance)

    def check_key_exists(self):
        key_to_check = self.key_input.text().strip()
        if not key_to_check:
            QMessageBox.warning(
                self, "Eingabefehler", "Batch Key prüfen: Key muss angegeben werden!"
            )
            self.log_message("Batch Key prüfen: Key fehlt!")
            return

        params = {"key": key_to_check}
        is_dry_run = self.dryrun_checkbox.isChecked()

        action_instance = CheckKeyExistsAction(
            logger_func=self.log_message, params=params, dry_run=is_dry_run
        )
        self._iterate_files_with_action(action_instance=action_instance)

    def check_key_missing(self):
        key_to_check = self.key_input.text().strip()
        if not key_to_check:
            QMessageBox.warning(
                self,
                "Eingabefehler",
                "Batch Key fehlt prüfen: Key muss angegeben werden!",
            )
            self.log_message("Batch Key fehlt prüfen: Key fehlt!")
            return

        params = {"key": key_to_check}
        is_dry_run = self.dryrun_checkbox.isChecked()

        action_instance = CheckKeyMissingAction(
            logger_func=self.log_message, params=params, dry_run=is_dry_run
        )
        self._iterate_files_with_action(action_instance=action_instance)

    def check_key_value_match(self):
        key_to_check = self.key_input.text().strip()
        value_to_match = self.value_input.text().strip()

        if not key_to_check:
            QMessageBox.warning(
                self,
                "Eingabefehler",
                "Batch Key/Value prüfen: Key muss angegeben werden!",
            )
            self.log_message("Batch Key/Value prüfen: Key fehlt!")
            return
        if not value_to_match:
            QMessageBox.warning(
                self,
                "Eingabefehler",
                "Batch Key/Value prüfen: Value muss angegeben werden!",
            )
            self.log_message("Batch Key/Value prüfen: Value fehlt!")
            return

        params = {"key": key_to_check, "value": value_to_match}
        is_dry_run = self.dryrun_checkbox.isChecked()

        action_instance = CheckKeyValueMatchAction(
            logger_func=self.log_message, params=params, dry_run=is_dry_run
        )
        self._iterate_files_with_action(action_instance=action_instance)

    def _placeholder_batch_operation(self, action_name):
        QMessageBox.information(
            self,
            "Noch nicht implementiert",
            f"Die Batch-Aktion '{action_name}' muss noch auf die neue Aktionsklassen-Struktur umgestellt werden.",
        )
        self.log_message(
            f"Batch-Aktion '{action_name}' ist noch nicht auf die neue Struktur umgestellt."
        )
