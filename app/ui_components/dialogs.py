# frontmatter_tool_project/app/ui_components/dialogs.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QDialogButtonBox
)

class KeyValueDialog(QDialog):
    def __init__(self, parent=None, window_title="Eingabe", key_label="Key:", value_label="Value:", initial_key="", initial_value=""):
        super().__init__(parent)
        self.setWindowTitle(window_title)
        self.setMinimumWidth(350)

        self.layout = QVBoxLayout(self)

        # Key Eingabe
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel(key_label))
        self.key_input = QLineEdit(self)
        self.key_input.setText(initial_key)
        key_layout.addWidget(self.key_input)
        self.layout.addLayout(key_layout)

        # Value Eingabe
        value_layout = QHBoxLayout()
        value_layout.addWidget(QLabel(value_label))
        self.value_input = QLineEdit(self)
        self.value_input.setText(initial_value)
        value_layout.addWidget(self.value_input)
        self.layout.addLayout(value_layout)

        # Standard-Buttons (OK, Abbrechen)
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        self.button_box.accepted.connect(self.accept) # Verbindet OK mit self.accept()
        self.button_box.rejected.connect(self.reject) # Verbindet Abbrechen mit self.reject()
        self.layout.addWidget(self.button_box)

        # Stylesheet des Parents übernehmen, falls vorhanden und gewünscht
        if parent and hasattr(parent, 'styleSheet') and callable(parent.styleSheet):
            self.setStyleSheet(parent.styleSheet())


    def get_values(self) -> tuple[str, str] | None:
        """Gibt die eingegebenen Werte zurück, wenn der Dialog akzeptiert wurde."""
        if self.result() == QDialog.DialogCode.Accepted: # Prüfen, ob OK geklickt wurde
            return self.key_input.text().strip(), self.value_input.text().strip()
        return None # Oder eine Exception werfen, je nach Präferenz

class KeyDialog(QDialog):
    def __init__(
        self, parent=None, window_title="Eingabe", key_label="Key:", initial_key=""
    ):
        super().__init__(parent)
        self.setWindowTitle(window_title)
        self.setMinimumWidth(300)

        self.layout = QVBoxLayout(self)

        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel(key_label))
        self.key_input = QLineEdit(self)
        self.key_input.setText(initial_key)
        key_layout.addWidget(self.key_input)
        self.layout.addLayout(key_layout)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        if parent and hasattr(parent, "styleSheet") and callable(parent.styleSheet):
            self.setStyleSheet(parent.styleSheet())

    def get_key(self) -> str | None:
        if self.result() == QDialog.DialogCode.Accepted:
            return self.key_input.text().strip()
        return None
