# frontmatter_tool_project/app/core/utils.py

SUPPORTED_EXTENSIONS = ["*.md", "*.txt", "*.html", "*.yaml", "*.yml"]


def is_supported_file(filename: str) -> bool:
    """
    Prüft, ob die Datei eine unterstützte Erweiterung hat.
    """
    if not filename:  # Sicherstellen, dass filename nicht None oder leer ist
        return False
    return any(filename.lower().endswith(ext[1:]) for ext in SUPPORTED_EXTENSIONS)
