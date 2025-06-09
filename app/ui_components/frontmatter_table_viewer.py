"""
Tabellenbasierter Frontmatter-Viewer für das Frontmatter Tool.
Erlaubt die Anzeige und Bearbeitung von Frontmatter als Tabelle.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
)

FRONTMATTER_TYPES = [
    "Text",
    "Liste",
    "Zahl",
    "Checkbox",
    "Datum",
    "Datum und Uhrzeit",
]


class FrontmatterTableViewer(QTableWidget):
    def __init__(self, parent=None):
        """
        Initialisiert den Tabellen-Viewer für Frontmatter.
        """
        super().__init__(parent)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Typ", "Key", "Value"])
        self.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked
        )
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setShowGrid(True)
        self.setMinimumHeight(120)
        self.setSortingEnabled(False)
        self.setWordWrap(False)
        self.setColumnWidth(0, 120)
        self.setColumnWidth(1, 120)
        self.setColumnWidth(2, 300)

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
                val, typ = value, "Text"
            type_combo = QComboBox()
            type_combo.addItems(FRONTMATTER_TYPES)
            if typ in FRONTMATTER_TYPES:
                type_combo.setCurrentText(typ)
            else:
                type_combo.setCurrentText("Text")
            self.setCellWidget(row, 0, type_combo)
            key_item = QTableWidgetItem(str(key))
            value_item = QTableWidgetItem(str(val))
            value_item.setFlags(value_item.flags() | Qt.ItemIsEditable)
            self.setItem(row, 1, key_item)
            self.setItem(row, 2, value_item)

    def get_metadata(self) -> dict:
        """
        Gibt die aktuellen Metadaten aus der Tabelle zurück.
        """
        data = {}
        for row in range(self.rowCount()):
            type_widget = self.cellWidget(row, 0)
            typ = type_widget.currentText() if type_widget else "Text"
            key = self.item(row, 1).text() if self.item(row, 1) else ""
            value = self.item(row, 2).text() if self.item(row, 2) else ""
            data[key] = (value, typ)
        return data

    def clear_viewer(self):
        """
        Löscht die Tabelle.
        """
        self.setRowCount(0)
