# frontmatter_tool_project/app/styles/cyberpunk_theme.py


def get_cyberpunk_stylesheet() -> str:
    """
    Gibt das benutzerdefinierte Stylesheet für das Cyberpunk-Design als String zurück.
    """
    # Hier den kompletten String deines Stylesheets einfügen
    # Ich kürze es hier ab, du nimmst deinen vollständigen String
    return """
        QMainWindow, QDialog {
            background-color: hsl(230, 9%, 13%); /* --color-black (Workspace BG) */
            color: hsl(191, 54%, 64%); /* --color-cyan-530 (BODY TEXT!!) */
            font-family: 'Inter';
            font-size: 14px;
        }

        QWidget {
            background-color: hsl(230, 9%, 13%);
            color: hsl(191, 54%, 64%);
        }

        QGroupBox {
            font-weight: bold;
            border: 1px solid hsl(225, 12%, 20%);
            border-radius: 4px;
            margin-top: 15px;
            padding: 10px;
            background-color: hsl(231, 9%, 15%);
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 5px 0 5px;
            color: hsl(220, 23%, 95%);
            background-color: hsl(231, 9%, 15%);
        }

        QLabel {
            color: hsl(224, 37%, 80%);
            background-color: transparent;
            padding: 2px;
        }

        QLineEdit, QTextEdit {
            background-color: hsl(230, 8%, 10%);
            color: hsl(191, 54%, 64%);
            border: 1px solid hsl(225, 11%, 30%);
            border-radius: 3px;
            padding: 5px;
            font-size: 13px;
        }

        QLineEdit::placeholder {
            color: hsl(191, 30%, 50%);
        }

        QLineEdit:focus, QTextEdit:focus {
            border: 1px solid hsl(59, 71%, 68%);
        }

        QTextEdit {
            font-family: 'Dank Mono', 'Fira Code', Courier, monospace;
            font-size: 13px;
        }

        QPushButton {
            background-color: hsl(225, 18%, 25%);
            color: hsl(220, 23%, 95%);
            border: 1px solid hsl(225, 11%, 36%);
            padding: 4px 10px;
            border-radius: 3px;
            font-weight: normal;
            font-size: 13px;
            min-height: 24px;
        }

        QPushButton:hover {
            background-color: hsl(225, 11%, 36%);
            border: 1px solid hsl(225, 15%, 61%);
        }

        QPushButton:pressed {
            background-color: hsl(230, 8%, 10%);
        }

        QPushButton#logClearButton {
            background-color: #fb464c;
            color: white;
            font-weight: normal;
            font-size: 13px;
        }
        QPushButton#logClearButton:hover {
            background-color: hsl(3, 93%, 60%);
        }
        QPushButton#logClearButton:pressed {
            background-color: hsl(3, 80%, 50%);
        }

        QCheckBox {
            font-size: 13px;
            color: hsl(224, 37%, 80%);
            spacing: 8px;
            padding: 3px 0px;
        }

        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 1px solid hsl(225, 11%, 36%);
            border-radius: 3px;
            background-color: hsl(230, 8%, 10%);
        }

        QCheckBox::indicator:hover {
            border: 1px solid hsl(225, 15%, 61%);
        }

        QCheckBox::indicator:checked {
            background-color: hsl(255, 100%, 86%);
        }
        QCheckBox::indicator:checked:hover {
            background-color: hsl(255, 100%, 90%);
        }

        QScrollBar:vertical {
            border: none;
            background: hsl(231, 9%, 15%);
            width: 10px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: hsl(225, 14%, 55%);
            min-height: 25px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical:hover {
            background: hsl(224, 17%, 68%);
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
            height: 0px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }

        QScrollBar:horizontal {
            border: none;
            background: hsl(231, 9%, 15%);
            height: 10px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:horizontal {
            background: hsl(225, 14%, 55%);
            min-width: 25px;
            border-radius: 5px;
        }
        QScrollBar::handle:horizontal:hover {
            background: hsl(224, 17%, 68%);
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            border: none;
            background: none;
            width: 0px;
        }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
    """
