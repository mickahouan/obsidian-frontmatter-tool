"""
Tabellenbasierter Frontmatter-Viewer für das Frontmatter Tool.
Erlaubt die Anzeige und Bearbeitung von Frontmatter als Tabelle.
"""

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QMenu,
    QAction,
    QTableWidget,
    QTableWidgetItem,
)

FRONTMATTER_TYPES = [
    QCoreApplication.translate("FrontmatterTableViewer", "Text"),
    QCoreApplication.translate("FrontmatterTableViewer", "Liste"),
    QCoreApplication.translate("FrontmatterTableViewer", "Zahl"),
    QCoreApplication.translate("FrontmatterTableViewer", "Checkbox"),
    QCoreApplication.translate("FrontmatterTableViewer", "Datum"),
    QCoreApplication.translate("FrontmatterTableViewer", "Datum und Uhrzeit"),
]


class FrontmatterTableViewer(QTableWidget):
    def __init__(self, parent=None):
        """
        Initialisiert den Tabellen-Viewer für Frontmatter.
        """
        super().__init__(parent)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(
            [
                QCoreApplication.translate("FrontmatterTableViewer", "Typ"),
                QCoreApplication.translate("FrontmatterTableViewer", "Key"),
                QCoreApplication.translate("FrontmatterTableViewer", "Value"),
            ]
        )
        self.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked
            | QAbstractItemView.EditTrigger.SelectedClicked
        )
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setShowGrid(True)
        self.setMinimumHeight(120)
        self.setSortingEnabled(False)
        self.setWordWrap(False)
        self.setColumnWidth(0, 120)
        self.setColumnWidth(1, 120)
        self.setColumnWidth(2, 300)

        # Kontextmenü für Zeilen hinzufügen/löschen
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def display_frontmatter(self, metadata: dict):
        """
        Zeigt das Frontmatter als Tabelle an.
        Erwartet ein Dict wie {key: value} oder {key: (value, typ)}
        """
        self.setRowCount(0)
        if not metadata:
            return
        for row, (key, value) in enumerate(metadata.items()):
            self.insertRow(row)
            # Typ-Handling
            if isinstance(value, tuple) and len(value) == 2:
                val, typ = value
            else:
                val, typ = (
                    value,
                    QCoreApplication.translate("FrontmatterTableViewer", "Text"),
                )
            type_combo = QComboBox()
            type_combo.addItems(FRONTMATTER_TYPES)
            if typ in FRONTMATTER_TYPES:
                type_combo.setCurrentText(typ)
            else:
                type_combo.setCurrentText(
                    QCoreApplication.translate("FrontmatterTableViewer", "Text")
                )
            self.setCellWidget(row, 0, type_combo)
            key_item = QTableWidgetItem(str(key))
            value_item = QTableWidgetItem(str(val))
            value_item.setFlags(value_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.setItem(row, 1, key_item)
            self.setItem(row, 2, value_item)

    def get_metadata(self) -> dict:
        """
        Gibt die aktuellen Metadaten aus der Tabelle zurück.
        """
        data = {}
        for row in range(self.rowCount()):
            type_widget = self.cellWidget(row, 0)
            typ = (
                type_widget.currentText()
                if isinstance(type_widget, QComboBox)
                else QCoreApplication.translate("FrontmatterTableViewer", "Text")
            )
            key_item = self.item(row, 1)
            key = key_item.text() if key_item is not None else ""
            value_item = self.item(row, 2)
            value = value_item.text() if value_item is not None else ""
            data[key] = (value, typ)
        return data

    def clear_viewer(self):
        """
        Löscht die Tabelle.
        """
        self.setRowCount(0)

    # Neue Komfortfunktionen ----------------------------------------------
    def _show_context_menu(self, pos):
        menu = QMenu(self)
        add_action = QAction(
            QCoreApplication.translate("FrontmatterTableViewer", "Zeile hinzufügen"),
            self,
        )
        del_action = QAction(
            QCoreApplication.translate("FrontmatterTableViewer", "Zeile löschen"),
            self,
        )
        add_action.triggered.connect(self.add_row)
        del_action.triggered.connect(self.delete_selected_row)
        menu.addAction(add_action)
        if self.currentRow() >= 0:
            menu.addAction(del_action)
        else:
            del_action.setEnabled(False)
            menu.addAction(del_action)
        menu.exec(self.viewport().mapToGlobal(pos))

    def add_row(self):
        row = self.rowCount()
        self.insertRow(row)
        type_combo = QComboBox()
        type_combo.addItems(FRONTMATTER_TYPES)
        self.setCellWidget(row, 0, type_combo)
        self.setItem(row, 1, QTableWidgetItem(""))
        self.setItem(row, 2, QTableWidgetItem(""))

    def delete_selected_row(self):
        row = self.currentRow()
        if row >= 0:
            self.removeRow(row)
