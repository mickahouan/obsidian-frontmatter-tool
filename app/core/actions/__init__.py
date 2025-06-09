"""
Initialisiert das actions-Paket für Batch- und Einzelaktionen.
"""

# frontmatter_tool_project/app/core/actions/__init__.py
from .base_action import BaseAction
from .check_key_exists_action import CheckKeyExistsAction  # Hinzufügen
from .check_key_missing_action import CheckKeyMissingAction
from .check_key_value_match_action import CheckKeyValueMatchAction
from .delete_files_by_kv_action import DeleteFilesByKeyValueAction
from .delete_key_action import DeleteKeyAction
from .rename_key_action import RenameKeyAction
from .write_kv_action import WriteKeyValueAction

__all__ = [
    "BaseAction",
    "DeleteKeyAction",
    "WriteKeyValueAction",
    "RenameKeyAction",
    "CheckKeyExistsAction",
    "CheckKeyMissingAction",
    "CheckKeyValueMatchAction",
    "DeleteFilesByKeyValueAction",
]
