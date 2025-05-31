# frontmatter_tool_project/main.py
import sys
from PySide6.QtWidgets import QApplication
from app.main_window import FrontmatterTool

def start_app():
    """
    Initializes and starts the FrontmatterTool application.

    This function creates a QApplication instance, initializes the main window
    (FrontmatterTool), displays it, and starts the application's event loop.

    Raises:
        SystemExit: If the application is closed, sys.exit() is called to exit the program.
    """
    app = QApplication(sys.argv)
    window = FrontmatterTool()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    start_app()
