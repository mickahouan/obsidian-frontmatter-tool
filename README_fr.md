# Obsidian Frontmatter Tool

Un outil de bureau puissant et modulaire (PySide6) pour l'édition, l'analyse et la gestion en masse du frontmatter YAML dans les fichiers Markdown – inspiré d'Obsidian, mais utilisable de manière autonome.

![Screenshot](image-en.png)

*Traductions : [Deutsch](README_de.md) | [English](README.md)*

## Fonctionnalités

* **Explorateur de fichiers** avec menu contextuel pour les actions sur les fichiers individuels (écrire clé/valeur, supprimer la clé, renommer la clé, supprimer le fichier)
* **Visionneuse de frontmatter modifiable** (vue en liste) :
  * Sélection du type par clé (texte, liste, nombre, case à cocher, date)
  * Enregistrement direct des modifications
  * Détection et conversion automatiques du type
  * Vue divisée : tableau (modifiable) et vue YAML (lecture seule)
* **Actions par lot** pour de nombreux fichiers :
  * Écrire clé/valeur, supprimer la clé, renommer la clé
  * Vérifier clé/valeur, supprimer des fichiers selon des critères
  * Préconditions flexibles (logique `value_matches` incluse)
  * Mode simulation (dry-run) pour des tests en toute sécurité
* **Zone de log** avec sortie colorée et formatée (y compris emojis)
* **Thème cyberpunk** (sombre, moderne, personnalisable)
* **Gestion robuste des erreurs** (YAML, opérations sur les fichiers)
* **Code modulaire et testable** (tests unitaires pour les fonctions principales)

## Installation

1. **Installer Python 3.12+**

2. Cloner le dépôt :

```zsh
git clone <repo-url>
cd frontmatter_tool_project
```

3. Installer les dépendances (recommandé : venv) :

```zsh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# ou avec Poetry :
poetry install
```

## Démarrer

```zsh
python main.py
```

## Changer la langue

L'interface utilisateur est réglée par défaut sur le français.

Vous pouvez changer la langue à tout moment pendant l'exécution du programme via le menu **Language** (dans la barre de menu) entre français, anglais et allemand.

L'édition manuelle du fichier `main.py` n'est plus nécessaire.

Si vous venez de cloner le projet, générez la traduction française avec :

```zsh
pyside6-lrelease translations/fr.ts -qm translations/fr.qm
```

## Exécuter les tests

```zsh
pytest tests/
```

## Structure du projet (extrait)

```text
main.py
app/
  main_window.py         # Fenêtre principale & logique UI
  core/
    actions/            # Actions par lot et individuelles (modulaires)
    utils.py            # value_matches etc.
  ui_components/        # Dialogues, vue table, explorateur
  styles/               # Thème cyberpunk
TODO.md                 # Tâches & jalons
```

## Notes

* L'outil travaille directement sur les fichiers Markdown possédant un frontmatter YAML (par ex. issus d'Obsidian).
* Les listes, nombres, cases à cocher et valeurs de date sont automatiquement reconnus et correctement enregistrés.
* La sortie de log est colorée et met visuellement en évidence les erreurs, avertissements, informations et réussites.
* Des fonctions de confort comme ajouter/supprimer une ligne, validation, etc. sont prévues (voir TODO.md).

## Licence

MIT

---

**Développé avec ❤️ pour la communauté Obsidian et Markdown.**
