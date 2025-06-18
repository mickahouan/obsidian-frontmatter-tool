## Remarque concernant la langue

La langue de l'application peut désormais être modifiée à tout moment via le menu **Language** (allemand, anglais ou français). Il n'est plus nécessaire de modifier `main.py` manuellement.

## Jalons réalisés (Milestone 1 : socle et fonctionnalité de base)

* **Structure de base de l'interface (PySide6) :**
  * [x] Fenêtre principale (`QMainWindow`)
  * [x] Barre de menu (basique, extensible)
  * [x] Barre d'état (basique, extensible)
  * [x] Dialogue de sélection de répertoire et affichage
  * [x] Champs de saisie globaux pour Clé/Valeur/Nouvelle Clé
  * [x] Champs de saisie pour les préconditions
  * [x] Options (dry run, appliquer précondition)
  * [x] Matrice de boutons pour actions par lot
  * [x] Fenêtre de log (`QTextEdit`) avec fonction de suppression
  * [x] Gestion basique de la mise en page avec `QGroupBox` et classes de layout
  * [x] Feuille de style cyberpunk appliquée
* **Modularisation de la base de code :**
  * [x] Structure de projet avec répertoire `app` (core, ui_components, styles)
  * [x] `main.py` comme point de départ
  * [x] Feuille de style externalisée
  * [x] Fonctions auxiliaires (`utils.py`) externalisées
* **Explorateur de fichiers et affichage du frontmatter :**
  * [x] `FileExplorer` (`QTreeView` avec `QFileSystemModel`) implémenté et intégré
  * [x] `FrontmatterViewer` (`QTextEdit`) implémenté et intégré
  * [x] Affichage du frontmatter du fichier sélectionné
  * [x] Menu contextuel dans `FileExplorer` pour les actions sur un seul fichier (basique)
* **Actions sur un seul fichier (via menu contextuel et dialogues) :**
  * [x] "Single: Write key/value..." avec son propre dialogue (`KeyValueDialog`) et conversion des valeurs séparées par des virgules en listes
  * [x] "Single: Delete key..." avec son propre dialogue (`KeyDialog`)
  * [x] "Single: Delete file"
  * [x] Logique de sauvegarde correcte (mode `wb`) pour les actions individuelles
* **Moteur d'actions par lot (modularisé) :**
  * [x] Classe `BaseAction` comme base
  * [x] `_iterate_files_with_action` comme boucle de traitement centrale dans `main_window.py`
  * [x] Traitement des préconditions UI dans `_iterate_files_with_action`
  * [x] Fonctionnalité dry run pour les actions par lot (pilotée via `BaseAction`)
  * [x] Logique de sauvegarde correcte (mode `wb`) dans `BaseAction._save_changes`
* **Classes d'action par lot implémentées :**
  * [x] `DeleteKeyAction`
  * [x] `WriteKeyValueAction` avec conversion des valeurs séparées par virgules en listes lors de l'écriture
  * [x] `RenameKeyAction`
  * [x] `CheckKeyExistsAction`
  * [x] `CheckKeyMissingAction`
  * [x] `CheckKeyValueMatchAction` avec implémentation de base de la logique `value_matches` pour les valeurs de recherche séparées par virgules
  * [x] `DeleteFilesByKeyValueAction` avec implémentation de base de la logique `value_matches` pour les valeurs de recherche séparées par virgules et confirmation de sécurité dans le gestionnaire de `main_window.py`
* **Gestion des erreurs :**
  * [x] Interception de `yaml.YAMLError` pour l'analyse du frontmatter
  * [x] Gestion générale des exceptions pour les erreurs inattendues

* * *

## Liste de choses à faire (classée par importance/proposition)

### Phase 1 : Stabilisation et finalisation de la logique de base

* [x] Toutes les fonctions principales et tests terminés (voir ci-dessus)

### Phase 2 : Améliorations UI/UX

* [x] Optimisation de la mise en page (affinage)
* [x] Option pour `value_matches` : "Tous les éléments doivent correspondre" vs. "Au moins un élément doit correspondre"
* [x] Visionneuse de frontmatter éditable (vue liste avec sélection du type, sauvegarde, reconnaissance du type)
* [ ] Étendre la barre de menu
* [ ] Utilisation de la barre d'état
* [x] Sortie de log visuelle/formatée : couleurs, emojis, styles de police selon le type de log
* [ ] Fonctions de confort pour le Table Viewer (ajout/suppression de ligne, menu contextuel, validation, auto-save)
* [ ] Autres raffinements de l'UI et icônes
* [x] Changement de langue à l'exécution via le menu **Language** (allemand/anglais)

### Phase 3 : Fonctions avancées et robustesse

* [ ] Barre de progression pour les actions par lot
* [ ] Exécution asynchrone (threading)
* [ ] Système basé sur des règles / constructeur de flux de travail

* * *

*Statut : 12.06.2025 – Changement de langue via le menu implémenté. Les points 4/5/7/8 de la phase 2 et la phase 3 restent à réaliser.*
