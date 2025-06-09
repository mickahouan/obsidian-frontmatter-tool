"""
Dateioperationen für das Frontmatter Tool.
Enthält Hilfsfunktionen zum Lesen, Schreiben und Bearbeiten von frontmatter.Post Objekten.
"""

# app/core/file_operations.py
import frontmatter


def read_post(file_path):
    """Liest eine Datei und gibt das frontmatter.Post Objekt zurück."""
    with open(file_path, "r", encoding="utf-8") as f:
        return frontmatter.load(f)


def write_post(post, file_path):
    """Schreibt ein frontmatter.Post Objekt zurück in eine Datei."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(post))


def set_key_value_in_post(post, key, value):
    """Setzt ein Key-Value-Paar im Post-Objekt. Gibt True zurück, wenn eine Änderung erfolgte."""
    original_value = post.metadata.get(key)
    if str(original_value) != str(value):
        post.metadata[key] = value
        return True
    return False


def delete_key_from_post(post, key):
    """Löscht einen Key aus dem Post-Objekt. Gibt True zurück, wenn der Key existierte."""
    if key in post.metadata:
        del post.metadata[key]
        return True
    return False


# ... weitere Operationen ...
