## Milestone 1: Basic framework and core functionality (Completed)

* **GUI basic structure (PySide6):**
  * [x] Main window (QMainWindow)
  * [x] Menu bar (basic, still expandable)
  * [x] Status bar (basic, still expandable)
  * [x] Directory selection dialog and display
  * [x] Global input fields for Key/Value/New Key
  * [x] Input fields for preconditions
  * [x] Options (dry run, apply precondition)
  * [x] Button matrix for batch actions
  * [x] Log window (QTextEdit) with delete function
  * [x] Basic layout management with QGroupBox and layout classes
  * [x] Cyberpunk stylesheet applied

* **Modularization of the code base:**
  * [x] Project structure with app directory (core, ui_components, styles)
  * [x] main.py as starting point
  * [x] Stylesheet outsourced
  * [x] Auxiliary functions (utils.py) outsourced

* **File explorer and frontmatter display:**
  * [x] FileExplorer (QTreeView with QFileSystemModel) implemented and integrated
  * [x] FrontmatterViewer (QTextEdit) implemented and integrated
  * [x] Display of the front mat of the selected file
  * [x] Context menu in FileExplorer for single file actions (basic)

* **Single file actions (via context menu and dialogs):**
  * [x] "Single: Write key/value..." with its own dialog (KeyValueDialog)Conversion of comma-separated values in lists when writing
  * [x] "Single: Delete key..." with its own dialog (KeyDialog)
  * [x] "Single: Delete file"
  * [x] Correct storage logic (wb mode) for individual actions

* **Batch action engine (modularized):**
  * [x] BaseAction class as the basis
  * [x] _iterate_files_with_action as a central processing loop in main_window.py
  * [x] Processing of UI preconditions in _iterate_files_with_action
  * [x] Dry run functionality for batch actions (controlled via BaseAction)
  * [x] Correct storage logic (wb mode) in BaseAction._save_changes

* **Implemented batch action classes:**
  * [x] DeleteKeyAction
  * [x] WriteKeyValueActionConversion of comma-separated values in lists when writing
  * [x] RenameKeyAction
  * [x] CheckKeyExistsAction
  * [x] CheckKeyMissingAction
  * [x] CheckKeyValueMatchActionBasic implementation of the value_matches logic for comma-separated search values
  * [x] DeleteFilesByKeyValueActionBasic implementation of the value_matches logic for comma-separated search valuesSecurity query in the handler in main_window.py

* **Error handling:**
  * [x] Interception of yaml.YAMLError for frontmatter parsing
  * [x] General exception handling for unexpected errors

* * *

## To-do list (graded according to importance/suggestion)

### Phase 1: Stabilization and completion of the core logic

* [x] All core functions and tests completed (see above)

### Phase 2: UI/UX improvements

* [x] Layout optimization (fine-tuning)
* [x] Option for value_matches: "All elements must match" vs. "At least one element must match"
* [x] Editable frontmatter viewer (list view with type selection, saving, type recognition)
* [ ] Extend menu bar
* [ ] Using the status bar
* [x] Visual/formatted log output: colors, emojis, font styles depending on log type
* [ ] Convenience functions for Table Viewer (add/delete row, context menu, validation, auto-save)
* [ ] Further UI refinements and icons

### Phase 3: Advanced functions and robustness

* [ ] Progress bar for batch actions
* [ ] Asynchronous execution (threading)
* [ ] Rule-based system / workflow builder

* * *

*Status: 09.06.2025 - Phase 2, points 4/5/7/8 and phase 3 are to be implemented next.*
