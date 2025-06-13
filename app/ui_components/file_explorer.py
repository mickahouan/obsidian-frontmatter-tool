"""
Datei-Explorer-Komponente für das Frontmatter Tool.
Bietet eine Baumansicht für das Dateisystem und Kontextmenü für Einzeldatei-Aktionen.
"""

import os
from typing import TYPE_CHECKING

from PySide6.QtCore import QCoreApplication, QDir, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileSystemModel, QMenu, QTreeView

from ..core.utils import SUPPORTED_EXTENSIONS, is_supported_file

if TYPE_CHECKING:
    from ..main_window import FrontmatterTool


class FileExplorer(QTreeView):
    def __init__(self, parent_window: "FrontmatterTool"):
        """
        Initialisiert den Datei-Explorer.
        """
        super().__init__(parent_window)
        from PySide6.QtWidgets import QSizePolicy

        self.parent_window: "FrontmatterTool" = parent_window
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        self.file_model.setNameFilters(SUPPORTED_EXTENSIONS)
        self.file_model.setNameFilterDisables(False)
        self.setModel(self.file_model)
        self.setMinimumWidth(250)
        self.setHeaderHidden(True)
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        sp_left = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        sp_left.setHorizontalStretch(1)
        self.setSizePolicy(sp_left)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        if self.selectionModel() is not None:
            self.selectionModel().selectionChanged.connect(self._on_selection_changed)
        else:
            if self.parent_window and hasattr(self.parent_window, "log_message"):
                self.parent_window.log_message(
                    "WARNUNG: FileExplorer selectionModel ist None bei Initialisierung."
                )

    def set_root_directory(self, dir_path: str):
        """
        Setzt das Wurzelverzeichnis für den Explorer.
        """
        if dir_path and os.path.isdir(dir_path):
            self.file_model.setRootPath(dir_path)
            self.setRootIndex(self.file_model.index(dir_path))
            root_idx_for_log = self.rootIndex()
            num_rows = self.file_model.rowCount(root_idx_for_log)
            if self.parent_window and hasattr(self.parent_window, "log_message"):
                self.parent_window.log_message(
                    f"FileExplorer: Root gesetzt auf '{dir_path}'. View-Root-Index gültig: {root_idx_for_log.isValid()}. Model hat {num_rows} Zeilen am View-Root."
                )
        else:
            current_fallback_path = (
                self.file_model.rootPath()
                if self.file_model.rootPath()
                else QDir.homePath()
            )
            self.setRootIndex(self.file_model.index(current_fallback_path))
            if self.parent_window and hasattr(self.parent_window, "log_message"):
                self.parent_window.log_message(
                    f"WARNUNG: Ungültiger Pfad für FileExplorer: {dir_path}. Root nicht geändert oder auf Home."
                )

    def _on_selection_changed(self, selected, deselected):
        """
        Reagiert auf Änderungen der Dateiauswahl und informiert das Hauptfenster.
        """
        if self.parent_window and hasattr(
            self.parent_window, "on_file_selected_from_explorer"
        ):
            indexes = selected.indexes()
            file_path = None
            is_dir = False
            if indexes:
                index = indexes[0]
                file_path = self.file_model.filePath(index)
                is_dir = self.file_model.isDir(index)
            self.parent_window.on_file_selected_from_explorer(file_path, is_dir)

    def _show_context_menu(self, position):
        """
        Zeigt das Kontextmenü für Einzeldatei-Aktionen an.
        """
        indexes = self.selectedIndexes()
        if not indexes:
            return
        index = indexes[0]
        file_path = self.file_model.filePath(index)
        is_dir = self.file_model.isDir(index)
        menu = QMenu(self)
        if self.parent_window:
            if not is_dir and is_supported_file(file_path):
                write_kv_action = QAction(QCoreApplication.translate("FileExplorer", "Einzel: Key/Value schreiben..."), self)
                write_kv_action.triggered.connect(
                    lambda checked=False,
                    fp=file_path: self.parent_window.handle_single_file_write_kv(fp)
                )
                menu.addAction(write_kv_action)
                remove_key_action = QAction(QCoreApplication.translate("FileExplorer", "Einzel: Key löschen..."), self)
                remove_key_action.triggered.connect(
                    lambda checked=False,
                    fp=file_path: self.parent_window.handle_single_file_remove_key(fp)
                )
                menu.addAction(remove_key_action)
                rename_key_action = QAction(QCoreApplication.translate("FileExplorer", "Einzel: Key umbenennen..."), self)
                rename_key_action.triggered.connect(
                    lambda checked=False,
                    fp=file_path: self.parent_window.handle_single_file_rename_key(fp)
                )
                menu.addAction(rename_key_action)
                menu.addSeparator()
                delete_file_action = QAction(QCoreApplication.translate("FileExplorer", "Einzel: Datei löschen"), self)
                delete_file_action.triggered.connect(
                    lambda checked=False,
                    fp=file_path: self.parent_window.handle_single_file_delete(fp)
                )
                menu.addAction(delete_file_action)
            elif is_dir:
                open_folder_action = QAction(
                    f"'{os.path.basename(file_path)}' {QCoreApplication.translate('FileExplorer', 'als Arbeitsverzeichnis')}", self
                )
                open_folder_action.triggered.connect(
                    lambda checked=False,
                    dp=file_path: self.parent_window.set_directory_from_tree(dp)
                )
                menu.addAction(open_folder_action)
            else:
                no_action = QAction(QCoreApplication.translate("FileExplorer", "Keine Aktionen verfügbar"), self)
                no_action.setEnabled(False)
                menu.addAction(no_action)
            if not menu.isEmpty():
                menu.exec(self.viewport().mapToGlobal(position))
