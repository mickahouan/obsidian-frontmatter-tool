# frontmatter_tool_project/app/ui_components/dialogs.py
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)


class KeyValueDialog(QDialog):
    def __init__(
        self,
        parent=None,
        window_title="Eingabe",
        key_label="Key:",
        value_label="Value:",
        initial_key="",
        initial_value="",
    ):
        super().__init__(parent)
        self.setWindowTitle(window_title)
        self.setMinimumWidth(350)

        self.main_layout = QVBoxLayout(self)

        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel(key_label))
        self.key_input = QLineEdit(self)
        self.key_input.setText(initial_key)
        key_layout.addWidget(self.key_input)
        self.main_layout.addLayout(key_layout)

        value_layout = QHBoxLayout()
        value_layout.addWidget(QLabel(value_label))
        self.value_input = QLineEdit(self)
        self.value_input.setText(initial_value)
        value_layout.addWidget(self.value_input)
        self.main_layout.addLayout(value_layout)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(self.button_box)

        if parent and hasattr(parent, "styleSheet") and callable(parent.styleSheet):
            self.setStyleSheet(parent.styleSheet())

    def get_values(self) -> tuple[str, str] | None:
        """Gibt die eingegebenen Werte zurück, wenn der Dialog akzeptiert wurde."""
        if self.result() == QDialog.DialogCode.Accepted:
            return self.key_input.text().strip(), self.value_input.text().strip()
        return None


class KeyDialog(QDialog):
    def __init__(
        self, parent=None, window_title="Eingabe", key_label="Key:", initial_key=""
    ):
        super().__init__(parent)
        self.setWindowTitle(window_title)
        self.setMinimumWidth(300)

        self.main_layout = QVBoxLayout(self)

        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel(key_label))
        self.key_input = QLineEdit(self)
        self.key_input.setText(initial_key)
        key_layout.addWidget(self.key_input)
        self.main_layout.addLayout(key_layout)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(self.button_box)

        if parent and hasattr(parent, "styleSheet") and callable(parent.styleSheet):
            self.setStyleSheet(parent.styleSheet())

    def get_key(self) -> str | None:
        if self.result() == QDialog.DialogCode.Accepted:
            return self.key_input.text().strip()
        return None


class RenameKeyDialog(QDialog):
    def __init__(
        self,
        parent=None,
        window_title="Key umbenennen",
        old_key_label="Alter Key:",
        new_key_label="Neuer Key:",
        initial_old_key="",
        initial_new_key="",
    ):
        super().__init__(parent)
        self.setWindowTitle(window_title)
        self.setMinimumWidth(350)

        self.main_layout = QVBoxLayout(self)

        old_key_layout = QHBoxLayout()
        old_key_layout.addWidget(QLabel(old_key_label))
        self.old_key_input = QLineEdit(self)
        self.old_key_input.setText(initial_old_key)
        old_key_layout.addWidget(self.old_key_input)
        self.main_layout.addLayout(old_key_layout)

        new_key_layout = QHBoxLayout()
        new_key_layout.addWidget(QLabel(new_key_label))
        self.new_key_input = QLineEdit(self)
        self.new_key_input.setText(initial_new_key)
        new_key_layout.addWidget(self.new_key_input)
        self.main_layout.addLayout(new_key_layout)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(self.button_box)

        if parent and hasattr(parent, "styleSheet") and callable(parent.styleSheet):
            self.setStyleSheet(parent.styleSheet())

    def get_keys(self) -> tuple[str, str] | None:
        if self.result() == QDialog.DialogCode.Accepted:
            return self.old_key_input.text().strip(), self.new_key_input.text().strip()
        return None
