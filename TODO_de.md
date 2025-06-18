## Hinweis zur Sprache

Die Sprache der Anwendung kann jetzt jederzeit über das Menü **Language** gewechselt werden (Deutsch/Englisch/Französisch). Ein manueller Eingriff in `main.py` ist nicht mehr nötig.

## Milestone 1: Grundgerüst und Kernfunktionalität (Abgeschlossen)

* **GUI-Grundstruktur (PySide6):**
  * [X] Hauptfenster (`QMainWindow`)
  * [X] Menüleiste (Basis, noch erweiterbar)
  * [X] Statusleiste (Basis, noch erweiterbar)
  * [X] Verzeichnisauswahl-Dialog und Anzeige
  * [X] Globale Eingabefelder für Key/Value/Neuer Key
  * [X] Eingabefelder für Vorbedingungen
  * [X] Optionen (Dry Run, Vorbedingung anwenden)
  * [X] Button-Matrix für Batch-Aktionen
  * [X] Protokollfenster (`QTextEdit`) mit Löschfunktion
  * [X] Grundlegendes Layout-Management mit `QGroupBox` und Layout-Klassen
  * [X] Cyberpunk-Stylesheet angewendet
* **Modularisierung der Codebasis:**
  * [X] Projektstruktur mit `app`-Verzeichnis (core, ui_components, styles)
  * [X] `main.py` als Startpunkt
  * [X] Stylesheet ausgelagert
  * [X] Hilfsfunktionen (`utils.py`) ausgelagert
* **Datei-Explorer und Frontmatter-Anzeige:**
  * [X] `FileExplorer` (`QTreeView` mit `QFileSystemModel`) implementiert und integriert
  * [X] `FrontmatterViewer` (`QTextEdit`) implementiert und integriert
  * [X] Anzeige des Frontmatters der ausgewählten Datei
  * [X] Kontextmenü im `FileExplorer` für Einzeldatei-Aktionen (Basis)
* **Einzeldatei-Aktionen (via Kontextmenü und Dialoge):**
  * [X] "Einzel: Key/Value schreiben..." mit eigenem Dialog (`KeyValueDialog`)
    * [X] Umwandlung kommaseparierter Werte in Listen beim Schreiben
  * [X] "Einzel: Key löschen..." mit eigenem Dialog (`KeyDialog`)
  * [X] "Einzel: Datei löschen"
  * [X] Korrekte Speicherlogik (`wb`-Modus) für Einzelaktionen
* **Batch-Aktions-Engine (Modularisiert):**
  * [X] `BaseAction`-Klasse als Grundlage
  * [X] `_iterate_files_with_action` als zentrale Verarbeitungsschleife in `main_window.py`
  * [X] Verarbeitung von UI-Vorbedingungen in `_iterate_files_with_action`
  * [X] Dry-Run-Funktionalität für Batch-Aktionen (gesteuert über `BaseAction`)
  * [X] Korrekte Speicherlogik (`wb`-Modus) in `BaseAction._save_changes`
* **Implementierte Batch-Aktionsklassen:**
  * [X] `DeleteKeyAction`
  * [X] `WriteKeyValueAction`
    * [X] Umwandlung kommaseparierter Werte in Listen beim Schreiben
  * [X] `RenameKeyAction`
  * [X] `CheckKeyExistsAction`
  * [X] `CheckKeyMissingAction`
  * [X] `CheckKeyValueMatchAction`
    * [X] Grundlegende Implementierung der `value_matches` Logik für kommaseparierte Suchwerte
  * [X] `DeleteFilesByKeyValueAction`
    * [X] Grundlegende Implementierung der `value_matches` Logik für kommaseparierte Suchwerte
    * [X] Sicherheitsabfrage im Handler in `main_window.py`
* **Fehlerbehandlung:**
  * [X] Abfangen von `yaml.YAMLError` bei Frontmatter-Parsing
  * [X] Allgemeines `Exception`-Handling für unerwartete Fehler

---

## To-Do-Liste (Gestaffelt nach Wichtigkeit/Vorschlag)

### Phase 1: Stabilisierung und Vervollständigung der Kernlogik

* [X] Alle Kernfunktionen und Tests abgeschlossen (siehe oben)

### Phase 2: UI/UX-Verbesserungen

1. [X] Layout-Optimierung (Feinschliff)
2. [X] Option für `value_matches`: "Alle Elemente müssen matchen" vs. "Mindestens ein Element muss matchen"
3. [X] Editierbarer Frontmatter-Viewer (List-View mit Typauswahl, Speichern, Typ-Erkennung)
4. [ ] Menüleiste erweitern
5. [ ] Statusleiste nutzen
6. [X] Visuelle/formatierte Log-Ausgabe: Farben, Emojis, Font-Styles je nach Log-Typ
7. [ ] Komfortfunktionen für Table-Viewer (Zeile hinzufügen/löschen, Kontextmenü, Validierung, Auto-Save)
8. [ ] Weitere UI-Feinschliffe und Icons
9. [X] Sprachumschaltung zur Laufzeit über Menü **Language** (Deutsch/Englisch)

### Phase 3: Fortgeschrittene Funktionen und Robustheit

1. [ ] Fortschrittsanzeige für Batch-Aktionen
2. [ ] Asynchrone Ausführung (Threading)
3. [ ] Regelbasiertes System / Workflow-Builder

### Phase 4: Internationalisierung
1. [X] Mehrsprachige Unterstützung (Deutsch, Englisch)
2. [X] Sprachwechsel zur Laufzeit über Menü

---

*Stand: 12.06.2025 – Sprachumschaltung im Menü umgesetzt. Phase 2, Punkt 4/5/7/8 und Phase 3 sind als nächstes umzusetzen.*
